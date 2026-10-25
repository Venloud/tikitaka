# route-sandbox

Disposable private repo for testing VANDAM ROUTE Phase 3 (push, draft PR, CI, Codex CI repairs). Not production.

Tests: `python3 -m unittest discover -s tests -t . -v`

## Existing Route + ECC + Vandam memory

This repository now has `tikitaka.py`, a thin entry point to the **existing** Vandam Route helper. It owns no second scheduler, task state, approval store or memory database. Keep the feature checkout beside `claudevandam`, or supply the explicit `VANDAM_ROOT` path. The companion Vandam memory feature branch is required for memory commands.

```sh
python3 tikitaka.py doctor
python3 tikitaka.py skills "verify regression checkpoints"
python3 tikitaka.py route init . "Describe the approved engineering task"
python3 tikitaka.py route ecc-plan RUN RUN/capabilities.json
python3 tikitaka.py route memory-recall RUN "checkpoint recovery"
python3 tikitaka.py memory serve --port 8765
```

The original helper enforces plan approval, worktrees, scope, independent review, commit/push permissions and repair limits. A missing Claude/Codex companion is a real blocker, never an excuse to self-approve or switch paid providers. New runs record only allowlisted technical daily events in Vandam; prompts, command arguments and transcripts are excluded. No publishing phase or automatic paid model call is added. Working memory remains in original Route `state.json`; the local graph reads it instead of duplicating live state.

An isolated test can set `VANDAM_ROUTE_RUNS_ROOT` to a scratch directory without changing HOME or the existing default run store. `VANDAM_MEMORY_ROOT` can direct test logs to a fixture; production usage should keep the canonical Vandam root. The original textutils and unittest suite are preserved.
