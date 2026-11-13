# Read-only health check of ~/.agents and the agents that read it.
# Weekly routine: just -f ~/projects/rd-agents/justfile agents-check --json
agents-check *ARGS:
    @"{{justfile_directory()}}/scripts/agents-check" {{ARGS}}
