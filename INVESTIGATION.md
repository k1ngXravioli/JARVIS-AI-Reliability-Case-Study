# Investigation notes — source review and reproducible hypotheses

This document distinguishes **user observations**, **source-code findings**, and **untested hypotheses**. Line numbers refer to the version of `main.py` and `ui.py` shared for review; they may change in later commits or upstream releases.

## Reported symptoms (from my testing)

### Issue 1: Voice interaction loses conversational continuity

- **Observed:** After a spoken input, an audible signal sometimes occurred; afterwards I had to repeat earlier information for the conversation to continue.
- **Not yet known:** Whether the UI transcript itself disappeared, whether the model's short-term conversational context was lost, or both.
- **Do not infer:** The sound alone does not establish whether the API disconnected, the GUI reset, or an audio-processing error occurred.

### Issue 2: Crashes during demanding activity

- **Observed:** Under heavier workloads, the program sometimes crashed or stopped responding.
- **Not yet known:** Exact exceptions, memory utilisation, CPU utilisation, audio device status, or whether an API service limit was involved.

## Evidence from the uploaded source

| File and approximate lines | Directly visible behaviour | Reason to investigate |
| --- | --- | --- |
| `main.py` ~552–560 | `LiveConnectConfig` enables `session_resumption=SessionResumptionConfig()` | Enabling resumption is only the first step |
| `main.py` ~740–786 | `_receive_audio()` processes transcriptions, completed turns and tool calls | No visible branch storing `session_resumption_update.new_handle` |
| `main.py` ~827–864 | `run()` reconnects after errors and rebuilds session/queues | No visible prior handle passed to the new connection |
| `main.py` ~843–847 | Creates an unbounded audio playback queue and an audio send queue with `maxsize=10` | Potential resource pressure and producer/consumer imbalance |
| `main.py` ~711–719 | Mic callback schedules `out_queue.put_nowait()` | On a full bounded queue, `QueueFull` may be raised |
| `main.py` ~762–774 | Transcription fragments are displayed at `turn_complete`, then cleared | Incomplete fragments need careful handling on errors |
| `ui.py` ~593–640 | UI log has a queued, character-by-character rendering implementation | Distinguish rendering backlog from conversation context |

### Potential direction 1: Session resumption

Official Gemini Live API documentation describes retaining `session_resumption_update.new_handle` and passing that handle to a subsequent connection. The uploaded `main.py` requests session resumption but does not visibly implement that retained-handle flow. The code could therefore fail to retain conversation state after certain reconnects. **This is a hypothesis until validated against actual failure logs.**

**Investigation checklist:**
- Observe a non-sensitive session boundary and whether a reconnect event occurred.
- Record whether the service supplied a resumable handle, without publishing the handle itself.
- Test whether a resumed session recalls a harmless prior fact, with and without a reconnect.
- Record limitations such as expired resumption handles.

### Potential direction 2: Audio queue backpressure

A microphone produces samples continuously, while the send operation depends on the network and remote service. With `out_queue = asyncio.Queue(maxsize=10)` and a scheduled `put_nowait`, slow consumption can fill the queue. The queue is small enough that this possibility warrants examination. It is **not** evidence that the queue actually overflowed during the reported crashes.

**Investigation checklist:**
- Record `QueueFull` occurrences, drop counts and queue high-water mark without recording microphone audio.
- Check whether the producer is allowed to outpace the consumer under simulated slow network conditions.
- Explore a deliberate overflow policy in a test environment rather than silently accepting failures.
- Check that callbacks never block or perform slow disk/network operations.

### Potential direction 3: Transcript rendering versus conversational memory

The receive code buffers transcribed fragments and writes completed turns to the interface. That is separate from the AI provider's conversation state. During a disconnection, either or both may be affected. The phrase **"transcript reset"** is therefore tracked as an observation, not a proven root cause.

## Evidence needed before saying I fixed the problems

| Question | Answer / link to proof |
| --- | --- |
| Which original version or commit did I test? | **TO ADD** |
| Which files did I change personally? | **TO ADD** |
| What were the exact changes? | **TO ADD** |
| What were the error messages? | **TO ADD — redact sensitive data** |
| How many test runs before and after? | **TO ADD** |
| Did context loss stop or merely become less frequent? | **TO ADD** |
| Did crashes stop or merely become less frequent? | **TO ADD** |

## Scope and attribution

The program's original source, its features and user interface were created by the upstream developer. This document records an independent investigation, not authorship of the full voice assistant. It is not a verified security vulnerability report or penetration-test finding.