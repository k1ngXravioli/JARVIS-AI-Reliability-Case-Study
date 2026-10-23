# JARVIS AI — Voice Session Reliability & Debugging Case Study

**Project:** Independent exploration and debugging of an existing open-source AI assistant  
**Focus:** Python, audio streaming, asynchronous processing, session continuity, application reliability, and responsible security engineering  

> **Original project:** This case study examines the MARK XXXIX voice assistant developed by **FatihMakes** ([upstream project](https://github.com/FatihMakes/Mark-XXXIX)). The original application's architecture, features and interface are credited to its developer.

## Why I investigated it

I enjoy exploring open-source Python software and understanding how larger applications work. While experimenting with this JARVIS-inspired voice assistant, I encountered two reliability issues:

1. After certain voice interactions, an audible signal was followed by a loss of conversational context, requiring the conversation to be repeated.
2. The assistant sometimes crashed or became unstable during more demanding processing or automation sessions.

The investigation traces the application's generative-AI connection, microphone streaming, transcription handling, audio playback and asynchronous tasks.


## What I examined

| Component | Role in the system | Why it matters |
| --- | --- | --- |
| Live API connection | Streams voice interactions to and from an AI model | A new session may not preserve the earlier conversation |
| Session resumption | Can restore earlier session state after reconnection | Relevant to missing context |
| Audio input queue | Buffers microphone samples prior to sending | Queue capacity and processing delays can affect reliability |
| Audio output queue | Buffers AI audio ready for playback | Backlogs can increase memory pressure |
| Transcription buffers | Collect partial transcripts before showing complete turns | Partial speech may be lost if interrupted |
| PyQt6 interface | Displays the assistant's conversation and state | Useful for distinguishing GUI log behaviour from AI context |

## Technical findings

The following findings describe behaviour visible in the inspected `main.py` and `ui.py`.

### A. Reconnection without a retained session handle

- `main.py` configures session resumption, but the supplied receive loop does not visibly capture and store the latest `session_resumption_update.new_handle`.
- The `run()` loop creates a fresh connection following an exception without supplying a saved resumption handle.
- **Reliability implication:** Some reconnects may restart the AI context instead of resuming the conversation.

### B. Audio queue overflow risk

- `out_queue` is created with `maxsize=10`.
- Microphone callbacks schedule a `put_nowait` into that queue; if it is already full, `asyncio.QueueFull` can be raised.
- **Reliability implication:** If sending audio is slower than capture, this may contribute to error messages or intermittent audio failures.

### C. In-memory transcript buffers

- The receive loop joins input/output transcription fragments when a turn completes and then clears those buffers.
- Incomplete fragments can be lost if the receive loop ends unexpectedly; this is different from the model's session memory.

See [INVESTIGATION.md](INVESTIGATION.md) for the technical analysis.

## Skills developed

- Reading and tracing unfamiliar Python source code
- Asynchronous programming and streaming data concepts
- Understanding queues, callbacks and concurrency issues
- Recognising risks in error handling and session lifecycle management
- Documenting observations, hypotheses, tests and limitations
- Considering the reliability and privacy of assistants with access to desktop tools

## Source comparison

The inspected `main.py` and `ui.py` were compared against a public [MARK XXXIX reference snapshot](https://github.com/FatihMakes/Mark-XXXIX-OR). The comparison documents **transcription cleanup**, **end-of-turn playback state handling**, additional interface/tool changes, and **remaining unresolved risks** involving session resumption and queue pressure.

Read the [detailed source comparison](SOURCE_COMPARISON.md) for code-level differences and their implications. The analysis distinguishes functional differences from runtime fault resolution.

## How to explore the code safely

This repository does **not** redistribute the original assistant or any user-specific configuration files. Its [local diagnostic helper](tools/inspect_source.py) only reads a source file and prints a checklist of code features to examine. It does **not** run JARVIS or connect to any external API:

```bash
python3 tools/inspect_source.py /path/to/main.py
```

Do not upload API keys, voice recordings, raw transcripts, private files or session tokens.

## References

- Original project: https://github.com/FatihMakes/Mark-XXXIX
- Google Gemini Live API session management: https://ai.google.dev/gemini-api/docs/live-api/session-management
- Python `asyncio.Queue` reference: https://docs.python.org/3/library/asyncio-queue.html