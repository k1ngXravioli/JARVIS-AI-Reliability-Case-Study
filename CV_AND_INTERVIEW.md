# CV and interview wording

## Current CV-ready wording (conservative)

**Open-source AI Assistant — Python Reliability Investigation**

- Analysed an existing Python voice-assistant project, tracing real-time audio streaming, asynchronous tasks, API integration and conversation-handling components.
- Investigated intermittent loss of conversational context and instability under heavier workloads; experimented with code changes intended to improve reliability and continuity.
- Explored failure handling, queue behaviour and session lifecycle management, documenting potential causes and practical testing approaches.

> Use only the first two bullets if CV space is tight. These statements reflect the reported experience and code examined, but they do not claim independently verified fixes.

## Example interview answer (editable, not a script to memorise)

"I like to learn by reading open-source Python projects. When I tested a voice assistant, I noticed that some interactions interrupted the conversation and other sessions became unstable. Rather than treating it just as a user-interface problem, I examined its audio streaming, queue handling and session logic. I explored changes to make it more robust, and then learned why it's important to distinguish a plausible cause from a proven fix. My next step is to document my actual edits and run controlled before-and-after tests."

## How to make this stronger

1. Identify the exact Python methods that **you** changed.
2. Save a clean, minimal diff showing only **your** work.
3. Record repeatable tests on harmless data.
4. State what improved, what did not improve and what you would do next.
5. Link the case-study repository from your CV (once it is published).

## Claims to avoid without evidence

- "Designed or developed the entire JARVIS AI assistant."
- "Fixed all audio, memory, and performance bugs."
- "Optimised the application by 50%."
- "Discovered a security vulnerability" (unless it has been demonstrably verified).