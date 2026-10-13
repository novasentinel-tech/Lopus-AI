# Lopus-AI Architecture

This document will evolve together with the implementation.

## Initial boundaries

The project is divided into a few independent areas:

- **core** — runtime and orchestration primitives.
- **models** — model providers and model selection.
- **memory** — context and persistent memory experiments.
- **tools** — executable capabilities exposed to the runtime.
- **agents** — higher-level autonomous behaviors.
- **interfaces** — ways for a user or another application to interact with Lopus.

No final architecture is assumed at this stage. Decisions should be recorded here as the corresponding modules are implemented.
