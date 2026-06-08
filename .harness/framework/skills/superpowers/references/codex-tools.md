# Codex Tools Mapping

This document maps Claude Code tool names to their OpenAI Codex equivalents for platform adaptation.

## Tool Name Mapping

| Claude Code Tool | Codex Equivalent | Notes |
|-----------------|------------------|-------|
| `Read` | `read_file` | Read file contents |
| `Write` | `write_file` | Create or overwrite files |
| `Edit` | `edit_file` | Make targeted string replacements |
| `Glob` | `find_files` | Pattern-based file search |
| `Grep` | `search_files` | Content search with regex support |
| `Bash` | `execute_command` | Run shell commands |
| `AskUserQuestion` | `ask_user` | Interactive user prompts |
| `TodoWrite` | `update_todo` | Task tracking |
| `Agent` | `spawn_agent` | Launch subagents |
| `Skill` | `activate_skill` | Invoke skills (platform-specific) |
| `EnterPlanMode` | `start_planning` | Begin planning phase |
| `ExitPlanMode` | `finish_planning` | End planning phase |
| `EnterWorktree` | `create_worktree` | Isolated git worktree |
| `ExitWorktree` | `leave_worktree` | Exit worktree session |
| `CronCreate` | `schedule_task` | Create scheduled task |
| `CronDelete` | `cancel_scheduled_task` | Cancel scheduled task |
| `CronList` | `list_scheduled_tasks` | List all scheduled tasks |
| `TaskOutput` | `get_task_result` | Retrieve background task output |
| `TaskStop` | `stop_task` | Terminate running task |
| `WebSearch` | `web_search` | Search the web |
| `NotebookEdit` | `edit_notebook` | Edit Jupyter notebooks |

## Behavioral Differences

### Agent/Subagent Model
- **Claude Code**: Uses `Agent` tool with `subagent_type` parameter
- **Codex**: Uses `spawn_agent` with similar agent type selection

### Skill Invocation
- **Claude Code**: `Skill` tool reads skill files directly
- **Codex**: `activate_skill` loads skill metadata and content on demand
- **Gemini CLI**: Automatic tool mapping via GEMINI.md

### File Operations
- **Claude Code**: `Read` returns line-numbered content
- **Codex**: `read_file` returns raw content, line numbers optional

### Command Execution
- **Claude Code**: `Bash` with sandboxed execution
- **Codex**: `execute_command` with similar sandboxing

## Platform Detection

Skills can detect the current platform using environment variables or file existence:

```bash
# Claude Code
if [ -n "$CLAUDE_CODE_SESSION" ]; then
    # Claude Code specific logic
fi

# Codex
if [ -n "$CODEX_SESSION" ]; then
    # Codex specific logic
fi

# Gemini CLI
if [ -n "$GEMINI_CLI_SESSION" ]; then
    # Gemini CLI specific logic
fi
```

## Compatibility Layer

When writing cross-platform skills, use the Claude Code tool names as the canonical interface. The platform adaptation layer handles translation automatically.
