# HALLUCINATIONS.md

## Misassumptions Made by the Agent

1. **Assumption: Sample size N is rounded *down***
   - The agent mistakenly applied `math.floor` to the computed sample size, producing a smaller N than required.
   - **Differential test detection:** The test suite compared the agent’s N against the ground‑truth value calculated with `math.ceil`. The discrepancy triggered a failure, revealing the rounding error.

2. **Assumption: Degrees of freedom (df) equals N**
   - The agent used `df = n_total` instead of the correct formula `df = n_total - 1` for a paired‑samples t‑test.
   - **Differential test detection:** The generated critical t‑value was off by one degree of freedom, causing the computed power to deviate from the reference implementation. The test harness flagged this mismatch.

Both issues were corrected by enforcing the proper mathematical rules defined in **LEDGER.md**.
