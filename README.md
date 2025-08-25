# Claude Settings Repository

A comprehensive configuration repository for Claude Code with custom commands, agents, hooks, and MCP server integrations.

## 🗂️ Repository Structure

```
.claude/
├── agents/                    # Custom Claude agents
│   └── readwise-highlight-ingester.md
├── commands/                  # Custom slash commands
│   ├── follow-plan.md
│   ├── git-commit.md
│   ├── git-summary.md
│   ├── init-plan.md
│   └── multi-perspective-review.md
├── hooks/                     # Event hooks and logging
│   └── log-hooks.py
├── auto-plan-mode.md         # Auto-planning workflow configuration
└── settings.json             # Core Claude settings
.mcp.json                     # MCP server configurations
.env.example                  # Environment variables template
```

## 🚀 Quick Setup

1. **Clone and Configure**:
   ```bash
   # Copy environment template
   cp .env.example .env
   
   # Edit .env with your API keys
   vim .env
   ```

2. **Set Claude Project Directory**:
   ```bash
   export CLAUDE_PROJECT_DIR=/path/to/this/repo
   ```

3. **Initialize Required Directories**:
   ```bash
   mkdir -p .claude/hooks/logs .claude/cache .claude/tmp
   ```

## 🔧 Configuration

### Core Settings (`.claude/settings.json`)
- **Model**: Set to `sonnet` by default
- **Status Line**: Custom command showing current directory, git branch, and model

### MCP Servers (`.mcp.json`)
Configured integrations:
- **Playwright**: Browser automation
- **Context7**: AI context management
- **Zapier**: Google Calendar integration
- **Cloudflare**: Browser rendering and container sandboxing
- **Zen**: Advanced AI capabilities via OpenRouter

### Environment Variables
Required API keys (see `.env.example`):
- `ZAPIER_API_KEY`: For Google Calendar MCP integration
- `OPENROUTER_API_KEY`: For Zen MCP server

## 📋 Custom Commands

| Command | Description | Tools |
|---------|-------------|--------|
| `git-commit` | Intelligent commit message generation | `Bash(git:*)` |
| `git-summary` | Comprehensive repository status analysis | `Bash(git:*)` |
| `multi-perspective-review` | Multi-agent code review system | `Read` |
| `follow-plan` | Execute active project plans | `Read` |
| `init-plan` | Initialize planning structure | `Read` |

### Usage Examples
```bash
# Generate intelligent commit message
/git-commit

# Get comprehensive repo status
/git-summary

# Multi-perspective code review
/multi-perspective-review
```

## 🤖 Custom Agents

### Readwise Highlight Ingester
Specialized agent for processing Readwise Reader shared links:
- Extracts highlights and annotations
- Formats content as structured markdown
- Organizes in knowledge management system
- Maintains proper metadata and attribution

## 🪝 Hooks System

### Log Hooks (`log-hooks.py`)
Comprehensive logging system with:
- **Sensitive Data Redaction**: Automatically redacts API keys, tokens, passwords
- **Structured Logging**: JSONL format for easy parsing
- **Concurrent Safety**: File locking prevents corruption
- **Error Handling**: Graceful handling of malformed input

**Logged to**: `.claude/hooks/logs/hooks-log.jsonl`

## 🔒 Security Features

- Environment variable-based API key management
- Comprehensive sensitive data redaction in logs
- Proper `.gitignore` configuration for secrets
- No hardcoded credentials in version control

## 🛠️ Development

### Workflow Features
- **Auto-plan Mode**: Enforces planning before execution
- **Multi-perspective Reviews**: Parallel agent-based code analysis
- **Git Integration**: Smart commit messages and repository analysis

### Best Practices
- All API keys stored in environment variables
- Sensitive data automatically redacted from logs
- Consistent command structure with YAML frontmatter
- Modular agent and command organization

## 📊 Status Line

The custom status line displays:
- **Model**: Current Claude model (colored purple)
- **Directory**: Current working directory (colored blue)
- **Git Branch**: Active branch name in parentheses (colored green)

## 🤝 Contributing

When adding new commands or agents:
1. Follow the established YAML frontmatter format
2. Include appropriate `allowed-tools` restrictions
3. Add comprehensive descriptions and examples
4. Update this README with new additions

## 📝 License

[Add your preferred license here]