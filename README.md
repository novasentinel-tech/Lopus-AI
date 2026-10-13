# Lopus-AI

Lopus-AI is an experimental local-first AI project focused on building an autonomous digital coworker step by step.

> Current stage: initial project structure. Core modules are intentionally empty so they can be implemented and documented progressively.

## Goals

- Build the project publicly as a technical portfolio.
- Keep the architecture modular and understandable.
- Run the system locally as the project matures.
- Implement each capability incrementally instead of hiding complexity behind a finished framework.

## Initial structure

```text
Lopus-AI/
├── docs/                  # Architecture notes and technical decisions
├── examples/              # Small usage examples as modules become available
├── src/
│   └── lopus/
│       ├── agents/        # Autonomous agents and task-specific behaviors
│       ├── core/          # Main runtime, orchestration and shared primitives
│       ├── interfaces/    # CLI/API/UI adapters
│       ├── memory/        # Short/long-term memory experiments
│       ├── models/        # Local/cloud model adapters and routing
│       └── tools/         # Tools the runtime can execute
├── tests/                 # Automated tests
├── .env.example
├── .gitignore
└── pyproject.toml
```

## Development philosophy

The repository starts intentionally small. Each module will be designed, implemented and tested independently as Lopus evolves.

## License

See [LICENSE](LICENSE).
