# Source comparison — uploaded JARVIS files vs. public MARK XXXIX reference

**Review date:** 23 October 2026  
**Uploaded material:** `main.py`, `ui.py`, requirements and README supplied for this case study  
**Public comparison point:** [FatihMakes/Mark-XXXIX-OR](https://github.com/FatihMakes/Mark-XXXIX-OR), default-branch `main.py` and `ui.py` as retrieved for this review.

> **Important distinction:** This is a comparison of two *available snapshots*, not a verified personal Git commit history. Because the uploaded files contain no commit metadata establishing who made the changes, the differences below **cannot be attributed to me individually** without earlier saved files, commits or other evidence. The comparison repo may also be a different upstream revision. Original MARK XXXIX code and application credit belongs to **FatihMakes**.

## 1. Differences visible in the uploaded `main.py`

### A. Input/output transcript sanitisation (uploaded `main.py`, around lines 66–71, 752–760)

The uploaded snapshot introduces a regular-expression based `_clean_transcript()` function. It removes fragments matching `<ctrlN>` (case-insensitively), strips non-printing control characters except selected whitespace, and trims the result. Both input and output transcription handling call it.

In the public comparison snapshot, the same transcriptions use a basic `.strip()`.

**What this appears to improve:** Cleaner text displayed in the transcript, without the unwanted control-marker tokens. The helper was checked in isolation: `<ctrl12>Hello\x00 world\n` becomes `Hello world`.

**What it does not prove:** It is **not a solution to model context loss** following a reconnection.

### B. Audio playback state transitions (uploaded `main.py`, around lines 494, 745–768, 803–817 and 847)

The uploaded snapshot adds a `_turn_done_event` used by the audio receiving and playback tasks. The playback loop now waits for audio with `asyncio.wait_for(..., timeout=0.1)`, checks whether the turn has completed and the playback queue is empty, then changes state from `SPEAKING` to `LISTENING`.

The comparison snapshot instead awaits each queue item directly and toggles speaking state in the receive loop at `turn_complete`.

**Why this matters:** The new separation is intended to keep the interface's speaking/listening indicator in step with remaining audio playback, avoiding an early state change before queued audio is consumed.

**Still unverified:** Whether this eliminates the reported beep, interruptions, playback glitches or runtime crashes in live sessions. Queue state and output-device buffering are not the same thing.

### C. Tool and configuration adjustments (other differences)

- The uploaded `main.py` expands the declared browser-control operations and adds a browser selection field. This is additional functionality, **not demonstrated evidence of a crash fix**.
- The uploaded `ui.py` removes the public snapshot's OpenRouter API-key setup field and requirement, leaving Gemini-key and OS setup. This changes configuration requirements; it is **not evidence of session-reliability improvement**.
- Some file-processing and shutdown code is rearranged, without evidence from the supplied files that this fixes the two reported faults.

## 2. Differences that may actually *reduce* functionality

The public comparison snapshot contains a background `_update_memory_async()` workflow and initiates it after completed user turns. That per-turn workflow is absent in the uploaded `main.py`. The uploaded file still exposes an explicit `save_memory` tool and reads previously stored memory into its system prompt.

**Implication:** Automatically extracting new long-term memory after each turn may no longer happen. That is a trade-off or potential regression, **not a proven improvement**. This should not be confused with resuming an interrupted Live API session: long-term stored memory and a session's conversational context are different.

## 3. The originally reported reliability issues are not yet demonstrated as fixed

| Issue | What the uploaded source shows | Status |
| --- | --- | --- |
| AI loses context after reconnect | Requests `SessionResumptionConfig()` but no handling of `session_resumption_update.new_handle` or retained handle in the next connection | **Still unaddressed in the inspected code** |
| Microphone send queue can overflow | `out_queue = asyncio.Queue(maxsize=10)` and scheduled `put_nowait(...)`; no visible `QueueFull` handling | **Possible failure path remains** |
| Playback queue can grow | `audio_in_queue = asyncio.Queue()` with no size cap | **Potential backlog/resource pressure remains** |
| Visible transcript contains control markers | New sanitisation function used in input and output paths | **Plausible improvement; helper checked in isolation** |
| UI speaking indicator changes before playback drains | Completion event and timeout-based playback wait appear in the uploaded snapshot | **Plausible improvement; real audio testing needed** |
| Crashes under heavy load | No error logs, memory measurements or reproduced heavy-load tests supplied | **Cause and resolution unknown** |

The audible beep described during user testing is a **symptom**, not reliable evidence of its root cause.

## 4. What was checked during this review

1. Compared the uploaded `main.py` to public `main.py` by line-level sequence matching.
2. Compared the uploaded `ui.py` to public `ui.py` by line-level sequence matching.
3. Examined the uploaded session-configuration, microphone callback, audio-receiving, audio-playback and reconnect methods.
4. Parsed `main.py` as Python AST and exercised `_clean_transcript()` in isolation using harmless text.
5. Checked for explicit handling of session-resumption updates and `asyncio.QueueFull` in the uploaded source.

**Not tested:** The full JARVIS application, network/API sessions, real microphone, live playback, crash frequency, or a controlled before/after workload.

## 5. Safe and accurate wording for portfolio or interview

> I investigated transcript and playback-state reliability in a Python-based open-source voice assistant. Comparing source snapshots highlighted additional transcript sanitisation and asynchronous end-of-turn playback handling, while revealing unresolved risks involving session resumption and audio queue backpressure. I documented hypotheses and distinguished code-level changes from fixes that still require runtime verification.

If an interviewer asks **which edits I personally authored**, I should only name changes I can confirm from my own work, commit history or saved copies. A snapshot comparison alone does not prove authorship.

## References

- [Public MARK XXXIX reference — main.py](https://github.com/FatihMakes/Mark-XXXIX-OR/blob/main/main.py)
- [Public MARK XXXIX reference — ui.py](https://github.com/FatihMakes/Mark-XXXIX-OR/blob/main/ui.py)
- [Investigation notes](INVESTIGATION.md)
- [Repeatable test plan](TEST_PLAN.md)
