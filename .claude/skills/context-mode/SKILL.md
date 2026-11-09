---
name: context-mode
description: Context window conservation for AI coding agents. Intercept and sandbox large tool outputs (logs, test runs, DOM trees, large diffs) to prevent context exhaustion and retain session continuity.
---

# Context Mode: Context Conservation & Sandboxed Execution

When processing high-volume outputs (massive logs, test results, large JSON payloads, git diffs > 500 lines, AST scans), dumping the raw text into the context window causes context bloat and degrades reasoning quality.

## Mandatory Rules for Heavy Outputs

1. **Execute Inline Scripts for Filtering**:
   - Instead of reading 10,000 lines of logs with raw tool calls, write a one-liner or quick script to filter and summarize:
     ```powershell
     # Powershell example: extract only error summaries
     Get-Content build.log | Select-String "ERROR|FAIL" | Select-Object -First 20
     ```
   - Return only the essential distilled output into the agent context.

2. **Delegate Heavy Bulk Reads to Subagents**:
   - When surveying dozens of documentation files or conducting broad audits, invoke a specialized subagent (`invoke_subagent`).
   - The subagent absorbs the large context window and reports back a concise summary.

3. **Session State Continuity Across Compaction**:
   - When conversations grow large and trigger automatic compaction/truncation, record critical session landmarks in `.scratch/` or handoff notes (`/handoff`).
   - Ground decisions on file artifacts rather than transient context window memory.

4. **Threshold Rule**:
   - Any raw tool output likely to exceed 100 lines must be bounded, piped, or summarized before outputting.
