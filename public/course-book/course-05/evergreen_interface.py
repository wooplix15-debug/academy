from copy import deepcopy
from datetime import date, datetime
import hashlib
import json

FIELDS = {
    "schema_version", "event_id", "job_ref", "customer_ref",
    "source_revision", "completed_on", "summary", "occurred_at"
}
JOBS = {
    "EVG-JOB-2001": "EVG-CUST-0101",
    "EVG-JOB-2002": "EVG-CUST-0102",
    "EVG-JOB-2003": "EVG-CUST-0103"
}
A = {
    "schema_version": "1.0", "event_id": "EVG-EVENT-001",
    "job_ref": "EVG-JOB-2001", "customer_ref": "EVG-CUST-0101",
    "source_revision": 1, "completed_on": "2027-01-28",
    "summary": "Replaced filter", "occurred_at": "2027-01-28T09:00:00Z"
}


def fingerprint(message):
    text = json.dumps(message, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


class Receiver:
    def __init__(self, version="V2"):
        self.version = version
        self.receipts, self.latest, self.review_items = {}, {}, []
        self.invoice_releases = 0

    def receive(self, message, identity="handoff_writer", fault=None):
        if identity != "handoff_writer":
            return {"outcome": "DENIED"}
        if not isinstance(message, dict) or set(message) != FIELDS:
            return {"outcome": "INVALID"}

        strings = FIELDS - {"source_revision"}
        if any(not isinstance(message[k], str) or not message[k].strip()
               for k in strings):
            return {"outcome": "INVALID"}
        if (message["schema_version"] != "1.0"
                or type(message["source_revision"]) is not int
                or message["source_revision"] < 1):
            return {"outcome": "INVALID"}
        if JOBS.get(message["job_ref"]) != message["customer_ref"]:
            return {"outcome": "INVALID"}

        try:
            occurred = datetime.fromisoformat(
                message["occurred_at"].replace("Z", "+00:00")
            )
            if (occurred.utcoffset() is None
                    or occurred.utcoffset().total_seconds() != 0
                    or date.fromisoformat(message["completed_on"])
                    > occurred.date()):
                return {"outcome": "INVALID"}
        except (TypeError, ValueError):
            return {"outcome": "INVALID"}

        key, digest = message["event_id"], fingerprint(message)
        existing = self.receipts.get(key)
        if existing:
            if existing["fingerprint"] != digest:
                return {"outcome": "COLLISION"}
            if self.version == "V1":
                self.review_items.append(key)  # Deliberate model defect
            return {
                "outcome": "DUPLICATE",
                "receipt_ref": existing["receipt_ref"],
                "finance_status": "Received"
            }

        current = self.latest.get(
            message["job_ref"], {}
        ).get("source_revision", 0)
        if message["source_revision"] <= current:
            return {"outcome": "STALE"}
        if fault == "before_commit":
            raise TimeoutError("Simulated timeout before commit")

        receipt = "SIM-RECEIPT-{:03d}".format(len(self.receipts) + 1)
        self.receipts[key] = {
            "fingerprint": digest, "receipt_ref": receipt,
            "job_ref": message["job_ref"]
        }
        self.latest[message["job_ref"]] = {
            "source_revision": message["source_revision"],
            "summary": message["summary"]
        }
        self.review_items.append(key)

        if fault == "after_commit":
            raise TimeoutError("Simulated acknowledgement loss after commit")
        return {
            "outcome": "ACCEPTED",
            "receipt_ref": receipt, "finance_status": "Received"
        }

    def lookup(self, event_id):
        receipt = self.receipts.get(event_id)
        return deepcopy(receipt) if receipt else None

    def public(self, event_id):
        receipt = self.receipts[event_id]
        return {
            "job_ref": receipt["job_ref"],
            "handoff_status": "Received",
            "finance_contact": "finance@evergreen.example.com"
        }


def replay_probe(version):
    receiver = Receiver(version)
    try:
        receiver.receive(A, fault="after_commit")
    except TimeoutError:
        pass
    # The fixture assumes receipt lookup is unavailable to the sender.
    retry = receiver.receive(A)
    return {
        "version": version, "retry": retry["outcome"],
        "stored_events": len(receiver.receipts),
        "review_items": len(receiver.review_items),
        "invoice_releases": receiver.invoice_releases
    }


if __name__ == "__main__":
    for version in ("V1", "V2"):
        print(json.dumps(replay_probe(version), sort_keys=True))
