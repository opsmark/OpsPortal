# Original synthetic faculty workflow — editable source-grounded draft proof

**Artifact:** [Download exact seven-file ZIP](https://media.base44.com/files/public/6a89094776dbb07b37c5ae96/0799c0ec3_OPS_Faculty_Workflow_Synthetic_Proof_v1.zip) · SHA-256 `1cf27d1c568fd902d6433beca0e5d42f232b71620f116d29d178b1c57e6a6c75`

**Purpose:** A bounded, self-directed technical demonstration for a potential faculty document-workflow buyer. **Not** a commissioned project, classroom adoption, published research, or evidence of a paid customer.

A fictional supply-chain case in `source_packet.json` (explicit source fact IDs F01–F04 and unknowns U01–U03) drives the included offline script to create **four editable PowerPoint student slides**, **a separate editable one-page Word instructor note**, a SHA-256 manifest and a standalone verifier. The result is labeled **DRAFT_PENDING_FACULTY_APPROVAL** throughout. The 96% carrier performance is clearly a forecast, not an observed outcome; missing business facts remain marked unknown.

**Verification completed October 31, 2026:** Actual PPTX/DOCX were inspected after rendering; final source-reference and arithmetic test passed; public ZIP fetched HTTP 200, 69,448 bytes, `application/zip`, exact SHA-256 match, seven expected members, ZIP CRC PASS.

**Limits, important for evaluating fit:** This is a deterministic script using structured synthetic input; it is **not** a RAG/embeddings system, not a secure faculty file intake, not integrated with university identity/provider systems, not a tested license or production deployment, and not a guarantee of teaching quality or faculty acceptance. No client/real student/private research data was ingested. Python code runs locally and depends on `python-pptx` and `python-docx`.

A production system would need a separately agreed discovery/architecture phase covering rights, sensitive-data policies, verified source registries/retrieval, approved hosted/local model routes, tests for unsupported claims, faculty review, editable exports, and secure owner handoff. No protected customer workflow is offered through this ZIP.


## Workflow boundary diagram

**Solid first path is demonstrated only with fictional structured source data.** All remaining gates are **proposed for discovery and buyer acceptance**; the ZIP does not implement institutional authentication, private file transfer, embeddings, or an approval UI.

```mermaid
flowchart TD
    A["Authorized source facts — synthetic F01–F04"] --> B["Deterministic fact & unknown registry"]
    B --> C["Consistency and source-ID checks"]
    C --> D["Editable student PPTX draft"]
    C --> E["Editable instructor DOCX draft"]
    D --> F{"Faculty review — not implemented as an app"}
    E --> F
    F -->|Reject / corrections| B
    F -->|Explicit approval| G["Potential final release — not implemented"]
    H["Future confidential files"] --> I{"Rights, privacy and secure-intake approval"}
    I -->|Not approved| J["Do not ingest"]
    I -->|Approved only| K["Future controlled document parsing and retrieval"]
    K -.-> B
```

**Decision boundaries:** The current code creates drafts and verifies source references; it cannot finalize a faculty judgment. A production owner must determine data residency, role-based access, third-party processor permissions, retrieval quality and supported export fidelity before admitting private material. An editable output is not evidence of accurate scholarship; all citations, claims, teaching quality and intellectual-property rights require review.

**Acceptance checks for a proposed paid pilot:** (1) one rights-cleared representative input, (2) exact source-to-claim traceability, (3) source-neutral handling of unknowns, (4) editable PPTX/DOCX, (5) student/instructor content separation, (6) explicit faculty approval before final status, (7) measured human time and revision effort, and (8) owner-accepted data-retention and handoff rules. Only checks (2)–(5) have bounded synthetic evidence today; (1) is satisfied by an invented dataset rather than client rights clearance, and (6) is a visible draft-state hold rather than a functioning approval workflow.


## Request a bounded discovery conversation

For a real faculty, teaching, research or document-workflow problem, [send a description-only scope enquiry](mailto:rass991@gmail.com?subject=Faculty%20workflow%20scope%20enquiry%20-%20synthetic%20demo&body=Hello%2C%20I%20reviewed%20the%20fictional%20faculty%20workflow%20example.%0AThis%20is%20a%20scope%20enquiry%2C%20not%20an%20order%20or%20acceptance.%0AMy%20role%20and%20institution%20type%20%28optional%29%3A%0AWhich%20ONE%20workflow%20needs%20a%20first%20prototype%3F%0AInput%20document%20types%20%28describe%20only%2C%20no%20attachments%29%3A%0AApproximate%20quantity%2Fpages%20and%20template%20requirements%3A%0ARequired%20editing%2Foutput%20formats%3A%0ASource%20citation%2C%20faculty%20review%2C%20and%20privacy%20requirements%3A%0ADesired%20timeline%20and%20budget%20range%3A%0AWould%20a%20paid%20sanitized%20discovery%20stage%20be%20acceptable%3F%0APlease%20do%20not%20send%20student%2C%20unpublished%2C%20confidential%20or%20personal%20source%20files%20until%20a%20secure%20method%20and%20written%20scope%20have%20been%20agreed.). Describe **one** initial workflow, allowable input types, output requirements, privacy constraints and approximate timing. **Do not attach student data, unpublished research, credentials or confidential documents.** This is an enquiry for an owner-reviewed discovery discussion, not a fixed-price listing, an accepted order or an assurance of capacity. A secure intake and proposal must be agreed before any real source transfer or paid work.

**Current commercial status:** Example only; application, quote, buyer review, contract, payment and revenue **not established**. Public readability does not imply a project-wide open-source license or permission to process confidential material.
