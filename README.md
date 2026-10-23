# JARVIS AI — Voice Session Reliability & Debugging Case Study

**Project:** Independent exploration and debugging of an existing open-source AI assistant  
**Focus:** Python, audio streaming, asynchronous processing, session continuity, application reliability, and responsible security engineering  
**Status:** Investigation documented; final fixes and performance improvements **not independently verified**

> **Attribution:** This case study examines the **MARK XXXIX** voice assistant originally developed by **FatihMakes**. The project's own README points to https://github.com/FatihMakes/Mark-XXXIX and identifies its licence as **CC BY-NC 4.0**. All credit for the original application, its interface, tools, and architecture belongs to the original author. This repository contains **my analysis and learning notes**, not a claim that I created MARK XXXIX.

## Why I investigated it

I enjoy exploring open-source Python software and understanding how larger applications work. While experimenting with this JARVIS-inspired voice assistant, I encountered two reliability issues:

1. After certain voice interactions, an audible signal was followed by a loss of conversational context, requiring the conversation to be repeated.
2. The assistant sometimes crashed or became unstable during more demanding processing or automation sessions.

I explored how the application connects to its generative-AI service, streams microphone audio, handles the user-facing transcript, and processes automated tasks. I experimented with modifications intended to make the experience more stable.

**Important:** These are my reported observations. I still need to add exact before/after source-code changes and test logs to prove which modifications improved the program. I do not claim a permanent fix or a measured performance gain.

## What I examined

| Component | Role in the system | Why it matters |
| --- | --- | --- |
| Live API connection | Streams voice interactions to and from an AI model | A new session may not preserve the earlier conversation |
| Session resumption | Can restore earlier session state after reconnection | Relevant to missing context |
| Audio input queue | Buffers microphone samples prior to sending | Queue capacity and processing delays can affect reliability |
| Audio output queue | Buffers AI audio ready for playback | Backlogs can increase memory pressure |
| Transcription buffers | Collect partial transcripts before showing complete turns | Partial speech may be lost if interrupted |
| PyQt6 interface | Displays the assistant's conversation and state | Useful for distinguishing GUI log behaviour from AI context |

## Preliminary technical findings

These findings are based on the **specific `main.py` and `ui.py` files I provided for review**, not proof that these are the causes of the issues on every machine.

### A. Reconnection without a retained session handle

- `main.py` configures session resumption, but the supplied receive loop does not visibly capture and store the latest `session_resumption_update.new_handle`.
- The `run()` loop creates a fresh connection following an exception without supplying a saved resumption handle.
- **Hypothesis:** Some reconnects may restart the AI context instead of resuming the conversation.
- **Needed:** Observe a real disconnection, record a redacted event log, and compare behaviour before and after a resumption change.

### B. Audio queue overflow risk

- `out_queue` is created with `maxsize=10`.
- Microphone callbacks schedule a `put_nowait` into that queue; if it is already full, `asyncio.QueueFull` can be raised.
- **Hypothesis:** If sending audio is slower than capture, this may contribute to error messages or intermittent audio failures.
- **Needed:** Capture exception types and queue sizes in a controlled test and decide how dropped/backpressured input should be handled.

### C. In-memory transcript buffers

- The receive loop joins input/output transcription fragments when a turn completes and then clears those buffers.
- Incomplete fragments can be lost if the receive loop ends unexpectedly; this is different from the model's session memory.
- **Needed:** Check whether the visible interface log resets, the AI forgets earlier messages, or both.

See [INVESTIGATION.md](INVESTIGATION.md) for details and [TEST_PLAN.md](TEST_PLAN.md) for a repeatable test approach.

## Skills developed

- Reading and tracing unfamiliar Python source code
- Asynchronous programming and streaming data concepts
- Understanding queues, callbacks and concurrency issues
- Recognising risks in error handling and session lifecycle management
- Documenting observations, hypotheses, tests and limitations
- Considering the reliability and privacy of assistants with access to desktop tools

## Evidence I still need to add

- [ ] A redacted screenshot or example of the original problem
- [ ] Names of the exact files/functions **I personally modified**
- [ ] Before/after snippets or a diff of those changes
- [ ] Results of repeated voice-interaction tests
- [ ] Confirmation of what improved and what still needs fixing

## How to explore the code safely

This repository does **not** redistribute the original assistant or any user-specific configuration files. Its [local diagnostic helper](tools/inspect_source.py) only reads a source file and prints a checklist of code features to examine. It does **not** run JARVIS or connect to any external API:

```bash
python3 tools/inspect_source.py /path/to/main.py
```

Do not upload API keys, voice recordings, raw transcripts, private files or session tokens.

## Development note

The original software analysis and reported experiments are mine; these portfolio documents and the optional source-inspection helper were drafted with AI assistance. The helper and findings should not be represented as fixes I independently programmed or production-tested.

## References

- Original project: https://github.com/FatihMakes/Mark-XXXIX
- Google Gemini Live API session management: https://ai.google.dev/gemini-api/docs/live-api/session-management
- Python `asyncio.Queue` reference: https://docs.python.org/3/library/asyncio-queue.html