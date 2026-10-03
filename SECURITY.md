# Security and data handling

Keep secrets, API credentials, learner records and confidential client material out of this repository. The optional content agent reads `OPENAI_API_KEY` from the environment; do not put credentials in source files, requests or generated artifacts.

Use only synthetic or permission-cleared examples. The agent’s local approval flow is not team authentication or shared-drive access control. Before using a model with non-public content, confirm the data is approved for that service and configured retention.

For a security-sensitive concern, contact the repository owner privately through GitHub. Do not include secret values or personal data in a public issue.
