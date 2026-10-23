# Reliability test plan

Purpose: collect **repeatable, non-sensitive evidence** for the conversation-continuity and stability problems. This is a template; **no live API/audio tests were run as part of creating these documents**.

## Before testing

- Use a harmless test conversation only. Do not include personal or confidential information.
- Use a test environment/account when possible.
- Keep API keys, session handles, voice recordings, and private transcripts out of GitHub.
- Record versions (Python, relevant dependencies, operating system, tested code commit).
- Keep copies of the unmodified original and the edited version for comparison.

## Manual test matrix

| Test | Steps | What to record | Before | After |
| --- | --- | --- | --- | --- |
| Short spoken turn | Ask one harmless question | Did it respond? Did the UI show a completed turn? | Not recorded | Not recorded |
| Repeated turns | Make 5 harmless follow-up requests | Did it retain the earlier test topic? | Not recorded | Not recorded |
| Natural pause | Wait between turns, then continue | Was context still available? | Not recorded | Not recorded |
| Reconnect event | Observe a naturally occurring reconnect or a deliberate controlled test disconnect | Reconnect messages and harmless context continuity | Not recorded | Not recorded |
| Busy workload | Run a **permitted, low-risk** app operation on dummy data | Crash, delay, resource use and error messages | Not recorded | Not recorded |
| Restart | Close and reopen the application | What is intentionally persisted? | Not recorded | Not recorded |

## Minimal run record

```text
Test date:
OS and version:
Python version:
Original project revision:
My edited revision:
Test scenario:
Observed result:
Exact error name (if any):
Reproducible? yes / no / uncertain
Improved after modification? yes / no / uncertain
Notes (redacted):
```

## What evidence would support a strong CV claim?

An accurate claim would show the specific component changed, a before/after reproduction, and a clear outcome. For example, a result such as **"reconnection retained the test conversation in 5 out of 5 controlled trials"** must only be written if that exact test was actually performed and recorded. Until then, say **"investigated and experimented with improvements"** rather than **"resolved"**.