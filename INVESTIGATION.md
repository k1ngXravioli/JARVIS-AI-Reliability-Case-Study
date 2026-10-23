# Technical investigation — voice reliability and asynchronous processing

This analysis traces user-reported reliability symptoms to relevant areas of a Python voice-assistant codebase. Approximate line references refer to the inspected `main.py` and `ui.py` snapshots.

## Reported symptoms

### Issue 1: Voice interaction loses conversational continuity

- **Observed:** After a spoken input, an audible signal sometimes occurred; afterwards I had to repeat earlier information for the conversation to continue.
- **Technical distinction:** UI transcript rendering and model conversational context are separate layers. An audible signal does not independently establish a reconnection or reset.

### Issue 2: Crashes during demanding activity

- **Observed:** Under heavier workloads, the program sometimes crashed or stopped responding.
- **Technical distinction:** Queue pressure, playback backlog, API disconnections and UI responsiveness each require separate assessment; the reported symptom alone does not identify a single cause.

## Source-level findings

| File and approximate lines | Directly visible behaviour | Reason to investigate |
| --- | --- | --- |
| `main.py` ~552–560 | `LiveConnectConfig` enables `session_resumption=SessionResumptionConfig()` | Enabling resumption is only the first step |
| `main.py` ~740–786 | `_receive_audio()` processes transcriptions, completed turns and tool calls | No visible branch storing `session_resumption_update.new_handle` |
| `main.py` ~827–864 | `run()` reconnects after errors and rebuilds session/queues | No visible prior handle passed to the new connection |
| `main.py` ~843–847 | Creates an unbounded audio playback queue and an audio send queue with `maxsize=10` | Potential resource pressure and producer/consumer imbalance |
| `main.py` ~711–719 | Mic callback schedules `out_queue.put_nowait()` | On a full bounded queue, `QueueFull` may be raised |
| `main.py` ~762–774 | Transcription fragments are displayed at `turn_complete`, then cleared | Incomplete fragments need careful handling on errors |
| `ui.py` ~593–640 | UI log has a queued, character-by-character rendering implementation | Distinguish rendering backlog from conversation context |

### Session resumption

Official Gemini Live API documentation describes retaining `session_resumption_update.new_handle` and passing that handle to a subsequent connection. The uploaded `main.py` requests session resumption but does not visibly implement that retained-handle flow. A subsequent connection may therefore start without retained session context. This is a source-level risk, rather than a confirmed explanation of each observed reset.

### Audio queue backpressure

A microphone produces samples continuously, while the send operation depends on the network and remote service. With `out_queue = asyncio.Queue(maxsize=10)` and a scheduled `put_nowait`, slow consumption can fill the queue. A full bounded queue raises `asyncio.QueueFull` when written to with `put_nowait()`. The source presents a possible exception path; the reported crashes have not been tied to a recorded `QueueFull` event.

### Transcript rendering versus conversational memory

The receive code buffers transcribed fragments and writes completed turns to the interface. That is separate from the AI provider's conversation state. During a disconnection, either or both may be affected. The phrase **"transcript reset"** is therefore tracked as an observation, not a proven root cause.

## Scope and attribution

The original application and user interface are credited to FatihMakes. This is a technical source-review case study, not a claim of having developed the full assistant or discovered an exploitable security vulnerability.