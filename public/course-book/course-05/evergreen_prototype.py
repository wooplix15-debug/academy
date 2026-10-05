from copy import deepcopy
from datetime import datetime, date
import json

ACTORS = {
    "OPS": "Operations", "DSP": "Dispatch",
    "T1": "Technician", "T2": "Technician", "FIN": "Finance"
}
CUSTOMERS = {"EVG-CUST-0101", "EVG-CUST-0102", "EVG-CUST-0103"}


def need(condition, message):
    if not condition:
        raise ValueError(message)


def instant(text):
    value = datetime.fromisoformat(text.replace("Z", "+00:00"))
    need(
        value.utcoffset() is not None
        and value.utcoffset().total_seconds() == 0,
        "UTC timestamp required"
    )
    return value


class Prototype:
    def __init__(self):
        self.jobs, self.private, self.events = {}, {}, []

    def request(self, action, actor, at, ref, **data):
        need(actor in ACTORS, "Unknown actor")
        now, role = instant(at), ACTORS[actor]
        before = self.jobs.get(ref, {})
        before_state = before.get("state")
        before_handoff = before.get("handoff")
        jobs, private = deepcopy(self.jobs), deepcopy(self.private)

        if action == "intake":
            need(role == "Operations", "Operations required")
            need(ref not in jobs, "Duplicate job reference")
            customer = data.get("customer_ref", "")
            need(not customer or customer in CUSTOMERS, "Unknown customer")
            jobs[ref] = {
                "customer_ref": customer, "received_at": at,
                "state": "Ready to assign" if customer else "Intake hold",
                "appointments": [], "current": None, "started_at": None,
                "completion": {}, "handoff": "Not ready",
                "invoice_released": False
            }
        else:
            need(ref in jobs, "Unknown job")
            j = jobs[ref]
            ap = (
                j["appointments"][j["current"]]
                if j["current"] is not None else None
            )

            if action in {"ack", "start", "complete", "correct", "cancel_ack"}:
                need(
                    role == "Technician" and ap is not None
                    and ap["technician"] == actor,
                    "Assigned technician required"
                )

            if action == "repair":
                need(role == "Operations", "Operations required")
                need(j["state"] == "Intake hold", "Intake hold required")
                need(data["customer_ref"] in CUSTOMERS,
                     "Verified customer required")
                j["customer_ref"] = data["customer_ref"]
                j["state"] = "Ready to assign"

            elif action == "plan":
                need(role == "Dispatch", "Dispatch required")
                need(j["state"] in {"Ready to assign", "Scheduled"},
                     "Job not ready for scheduling")
                need(data["technician"] in {"T1", "T2"},
                     "Recognised technician required")
                need(instant(data["start"]) < instant(data["end"]),
                     "Invalid appointment interval")
                need(
                    all(a["ref"] != data["appointment_ref"]
                        for job in jobs.values()
                        for a in job["appointments"]),
                    "Duplicate appointment reference"
                )
                confirmation = data.get("customer_confirmed_at")
                if confirmation:
                    need(instant(confirmation) <= now,
                         "Future confirmation evidence")
                if ap is not None and ap["technician"] != data["technician"]:
                    need(data.get("withdrawal_at"),
                         "Withdrawal evidence required")
                    need(instant(data["withdrawal_at"]) <= now,
                         "Future withdrawal evidence")
                if ap is not None:
                    ap["state"] = "Superseded"
                    ap["withdrawal_at"] = data.get("withdrawal_at")
                j["appointments"].append({
                    "ref": data["appointment_ref"],
                    "technician": data["technician"],
                    "start": data["start"], "end": data["end"],
                    "state": "Pending acknowledgement",
                    "customer_confirmed_at": confirmation,
                    "technician_ack_at": None, "cancel_ack_at": None
                })
                j["current"] = len(j["appointments"]) - 1
                j["state"] = "Scheduled"
                need(not data.get("fail_before_commit"),
                     "Simulated interruption")

            elif action == "confirm":
                need(
                    role == "Operations" and ap is not None
                    and ap["state"] == "Pending acknowledgement",
                    "Pending appointment and Operations required"
                )
                ap["customer_confirmed_at"] = at
                if ap["technician_ack_at"]:
                    ap["state"] = "Confirmed"

            elif action == "ack":
                need(ap["state"] == "Pending acknowledgement",
                     "Pending appointment required")
                ap["technician_ack_at"] = at
                if ap["customer_confirmed_at"]:
                    ap["state"] = "Confirmed"

            elif action == "start":
                need(j["state"] == "Scheduled"
                     and ap["state"] == "Confirmed",
                     "Confirmed appointment required")
                need(now >= instant(ap["start"]),
                     "Scheduled start not reached")
                j["state"], j["started_at"] = "Work in progress", at

            elif action in {"complete", "correct"}:
                if action == "complete":
                    need(j["state"] == "Work in progress",
                         "Work in progress required")
                else:
                    need(j["state"] == "Service completed"
                         and j["handoff"] == "Returned",
                         "Returned handoff required")
                need(data.get("summary", "").strip(),
                     "Completion summary required")
                completed = date.fromisoformat(data["completion_date"])
                need(
                    instant(j["started_at"]).date() <= completed <= now.date(),
                    "Invalid completion date"
                )
                j["completion"] = {
                    "date": data["completion_date"],
                    "summary": data["summary"]
                }
                j["state"] = "Service completed"
                j["handoff"], ap["state"] = "Ready for Finance", "Completed"

            elif action == "review":
                need(role == "Finance", "Finance required")
                need(j["handoff"] == "Ready for Finance",
                     "Qualified handoff required")
                need(data["outcome"] in {"Returned", "Review complete"},
                     "Invalid Finance outcome")
                if data["outcome"] == "Returned":
                    need(data.get("reason", "").strip(),
                         "Private return reason required")
                    private.setdefault(ref, []).append({
                        "actor": actor, "at": at, "reason": data["reason"]
                    })
                j["handoff"] = data["outcome"]

            elif action == "cancel":
                need(role == "Operations", "Operations required")
                need(
                    data.get("verified") is True
                    and data.get("requester") and data.get("reason"),
                    "Verified cancellation evidence required"
                )
                need(
                    j["state"] in {
                        "Ready to assign", "Scheduled",
                        "Work in progress", "Service completed"
                    },
                    "Cancellation/change not available"
                )
                j["change_request"] = {
                    "requester": data["requester"],
                    "reason": data["reason"], "at": at
                }
                if j["started_at"]:
                    j["state"] = "Change review"
                else:
                    j["state"] = "Cancelled"
                    if ap:
                        ap["state"] = "Cancelled"

            elif action == "cancel_ack":
                need(j["state"] == "Cancelled"
                     and ap["state"] == "Cancelled",
                     "Cancelled appointment required")
                ap["cancel_ack_at"] = at

            else:
                raise ValueError("Action not implemented")

        j = jobs[ref]
        self.jobs, self.private = jobs, private
        self.events.append({
            "job_ref": ref, "action": action, "actor": actor, "at": at,
            "before_state": before_state, "after_state": j["state"],
            "before_handoff": before_handoff, "after_handoff": j["handoff"]
        })
        return self.view(actor, ref)

    def view(self, actor, ref):
        need(actor in ACTORS and ref in self.jobs,
             "Known actor and job required")
        j, role = self.jobs[ref], ACTORS[actor]
        ap = (
            j["appointments"][j["current"]]
            if j["current"] is not None else None
        )
        if role == "Technician":
            need(ap is not None and ap["technician"] == actor,
                 "Assigned technician required")
        result = {
            "job_ref": ref, "customer_ref": j["customer_ref"],
            "job_state": j["state"],
            "technician": ap["technician"] if ap else None,
            "appointment_state": ap["state"] if ap else None
        }
        if role != "Technician":
            result.update(
                handoff_status=j["handoff"],
                finance_contact="finance@evergreen.example.com"
            )
        if role == "Finance":
            result.update(
                private_notes=deepcopy(self.private.get(ref, [])),
                model_invoice_released=j["invoice_released"]
            )
        return result


if __name__ == "__main__":
    p = Prototype()
    r = "EVG-JOB-1901"
    p.request("intake", "OPS", "2027-01-26T08:00:00Z", r,
              customer_ref="EVG-CUST-0101")
    p.request(
        "plan", "DSP", "2027-01-26T08:30:00Z", r,
        appointment_ref="EVG-APPT-8001", technician="T1",
        start="2027-01-26T09:00:00Z", end="2027-01-26T10:00:00Z",
        customer_confirmed_at="2027-01-26T08:20:00Z"
    )
    p.request("ack", "T1", "2027-01-26T08:35:00Z", r)
    p.request("start", "T1", "2027-01-26T09:00:00Z", r)
    try:
        p.request("complete", "T1", "2027-01-26T09:30:00Z", r,
                  completion_date="2027-01-26", summary="")
    except ValueError as error:
        print("Blocked:", error)
    p.request("complete", "T1", "2027-01-26T10:00:00Z", r,
              completion_date="2027-01-26", summary="Replaced filter")
    p.request("review", "FIN", "2027-01-26T10:10:00Z", r,
              outcome="Returned", reason="Contract-rate clarification required")
    p.request("correct", "T1", "2027-01-26T10:15:00Z", r,
              completion_date="2027-01-26",
              summary="Replaced filter and confirmed service details")
    p.request("review", "FIN", "2027-01-26T10:20:00Z", r,
              outcome="Review complete")
    print(json.dumps(p.view("DSP", r), sort_keys=True))
    print("Prior returns:", len(p.private[r]))
    print("Committed events:", len(p.events))
    print("Model invoice released:", p.jobs[r]["invoice_released"])
