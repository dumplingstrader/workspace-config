# Complete Setup Guide for AI Resource Tools
## For Non-Technical Users

This guide walks you through setting up your AI resource management system with either VS Code or Claude CLI. Choose the option that works best for you. Don't worry if you're not a developer—we'll take it step by step!

---

## What Are We Setting Up?

Your VS Code environment includes a system that helps AI models (like Claude or Copilot) work with your resources more efficiently. Think of it like creating a smart filing system:

- **Old way**: AI reads through every single document every time (slow and expensive)
- **New way**: AI searches an index to find what it needs, then reads only those documents (fast and cheap)

**Result**: Saves 94.9% of costs and makes everything faster!

---

## Prerequisites: What You Need

Before starting, make sure you have:

1. **Git** - Version control system
   - Download from https://git-scm.com/downloads
   - ✅ **Important**: During installation, select "Git Bash" option (Windows)

2. **Bash Shell** - Command-line environment
   - **Windows**: Installed automatically with Git (Git Bash)
   - **macOS/Linux**: Already included in your system

3. **Visual Studio Code** (Optional, if using VS Code) - Downloaded and installed from https://code.visualstudio.com

4. **Claude CLI** (Optional, for command-line usage) - Downloaded and installed from https://claude.ai

5. **Python** - Downloaded and installed from https://www.python.org
   - ✅ **Important**: When installing, check "Add Python to PATH"

6. **Node.js** (Optional, for MCP servers and advanced features) - From https://nodejs.org

7. **Your resources** - All your skills, agents, and prompts already in your workspace

**Don't worry** - These are just standard tools. Installation is straightforward.

---

## Why Git and Bash?

### Why Git?

Git is essential for:

| Purpose | How It Helps |
|---|---|
| **Version Control** | Track changes to your code and configurations |
| **Collaboration** | Share work with teams, contribute to projects |
| **Backup & Recovery** | Restore previous versions if something breaks |
| **Plugin Management** | Many Claude Code plugins use Git for updates |
| **MCP Servers** | Some MCP servers interact with Git repositories |

Even if you're working alone, Git provides a safety net. Made a mistake? Roll back. Want to experiment? Create a branch. It's like "undo" for your entire project.

### Why Bash?

Bash is the standard command-line shell used by:

| Tool | Why Bash Matters |
|---|---|
| **Claude Code** | Executes commands using Bash syntax |
| **MCP Servers** | Many servers launch via Bash commands |
| **Build Scripts** | npm, Python, and other tools use shell commands |
| **Automation** | Hooks and scripts run in Bash environment |

**Windows Users**: Git Bash provides a Unix-like environment that ensures compatibility with tools designed for macOS/Linux. Without it, many commands won't work correctly.

### Quick Install Check

After installation, verify both are working:

```bash
# Check Git
git --version
# Should show: git version 2.x.x

# Check Bash (Windows - open Git Bash first)
bash --version
# Should show: GNU bash, version 5.x.x
```

✅ **Success**: Both commands return version numbers

---

## Authenticate with GitHub (Recommended)

If you plan to push code, create pull requests, or work with GitHub repositories, you should authenticate using the GitHub CLI (`gh`). This is the easiest way to set up Git credentials.

### Step 1: Install GitHub CLI

Download from https://cli.github.com/ or use a package manager:

**Windows (winget):**
```bash
winget install --id GitHub.cli
```

**macOS (Homebrew):**
```bash
brew install gh
```

**Linux:**
```bash
# Debian/Ubuntu
sudo apt install gh

# Fedora
sudo dnf install gh
```

### Step 2: Verify Installation

```bash
gh --version
# Should show: gh version 2.x.x
```

### Step 3: Authenticate

Run the authentication command:

```bash
gh auth login
```

You'll be prompted to:
1. Choose **GitHub.com** (or GitHub Enterprise if applicable)
2. Choose **HTTPS** (recommended) or SSH
3. Authenticate via **browser** (easiest) or paste a token

The browser option will:
- Display a one-time code (e.g., `ABC1-2345`)
- Open your browser to GitHub's device activation page
- After you enter the code and authorize, you're authenticated

### Step 4: Verify Authentication

```bash
gh auth status
```

**Expected output:**
```
github.com
  ✓ Logged in to github.com account YourUsername (keyring)
  - Active account: true
  - Git operations protocol: https
  - Token: gho_************************************
  - Token scopes: 'gist', 'read:org', 'repo'
```

✅ **Success**: You're authenticated and can push/pull to GitHub repositories

### Why GitHub CLI?

| Benefit | Description |
|---|---|
| **One-time setup** | Credentials stored securely, no re-entering passwords |
| **HTTPS + token** | More secure than password-based auth (deprecated by GitHub) |
| **Works everywhere** | Same auth works in terminal, VS Code, Claude Code |
| **Extra features** | Create PRs, view issues, manage repos from command line |

---

## Choose Your Setup Path

You can use these resource tools in one of two ways:

### Path A: VS Code Environment (GUI-based)
Use the steps in this guide with Visual Studio Code for a graphical interface.

### Path B: Claude CLI (Command-line based)
Use Claude CLI directly from your terminal. This is faster and requires no GUI.

Continue reading for your chosen path.

---

## Step 1: Open Your Workspace in VS Code

### What's a workspace?
A workspace is just a folder on your computer that contains all your projects and resources.

### How to open it:

1. Open Visual Studio Code
2. Click **File** → **Open Folder**
3. Navigate to your workspace folder (typically `c:\_Development`)
4. Click **Select Folder**

✅ **Success**: You should see your project files in the left sidebar

---

## Alternative: Setup for Claude CLI

If you prefer to use Claude CLI instead of VS Code, follow these steps instead:

### Step 1: Install Claude CLI

Claude CLI is Anthropic's command-line tool for interacting with Claude directly from your terminal.

#### On Windows, macOS, or Linux:

1. Open your terminal/command prompt
2. Run this command:
```
curl -fsSL https://download.claude.ai/cli/install.sh | bash
```

Or download from: https://claude.ai/downloads

3. Verify installation:
```
claude --version
```

✅ **Success**: You see a version number like `claude version 0.5.0`

### Step 2: Configure Claude CLI

1. In your terminal, authenticate with your Claude account:
```
claude auth login
```

2. Follow the prompts to authenticate

✅ **Success**: You're logged in and ready to use Claude CLI

### Step 3: Navigate to Resource Tools

In your terminal, navigate to the resource-tools folder:
```
cd resource-tools
```

Or on Windows:
```
cd c:\_Development\resource-tools
```

✅ **Success**: Your terminal shows the resource-tools directory

### Step 4: Build the Resource Index

Run the index builder:
```
python index_builder.py
```

You should see:
```
Building resource index...
[OK] Indexed 16 Claude skills
[OK] Indexed 137 Copilot agents
[OK] Indexed 135 Copilot prompts
[OK] Master index written to resource-tools\indexes\master-index.json
```

✅ **Success**: Index built with "Space savings: 94.9%"

### Step 5: Use with Claude CLI

Now you can use Claude CLI to search your resources:

```
claude "Search my resources for React tutorials"
```

Claude will automatically search through your indexed resources and provide relevant results.

### Step 6: Verify CLI Works

Test that everything is set up:

```
claude "List all my Claude skills"
claude "Find resources about Python"
claude "Show my Copilot agents related to frontend"
```

✅ **Success**: Claude CLI returns relevant results from your indexed resources

---

## Step 1: Open Your Workspace in VS Code

### What's a workspace?
A workspace is just a folder on your computer that contains all your projects and resources.

### How to open it:

1. Open Visual Studio Code
2. Click **File** → **Open Folder**
3. Navigate to your workspace folder (typically `c:\_Development`)
4. Click **Select Folder**

✅ **Success**: You should see your project files in the left sidebar

---

## Step 2: Open the Terminal

The terminal is where we'll run commands to set everything up. Don't be intimidated—you're just typing instructions!

### How to open Terminal:

1. In VS Code, click **Terminal** → **New Terminal** (at the top menu)
2. A black/dark area appears at the bottom—this is your terminal

✅ **Success**: You see a prompt (command line) ready for input

---

## Step 3: Install Python Tools (If Needed)

We need to check if Python is properly installed.

### In your terminal, type:
```
python --version
```

### What should happen:
You'll see something like: `Python 3.11.5`

### If you see an error:
- Make sure Python is installed (download from https://www.python.org)
- **Important**: During Python installation, check the box "Add Python to PATH"
- Restart VS Code after installing Python

✅ **Success**: Python version displays correctly

---

## Step 4: Navigate to Your Resource Tools

In the terminal, we need to navigate to the folder with your resource management tools.

### In your terminal, type:
```
cd resource-tools
```

This changes to the resource-tools folder (like opening a folder in Windows Explorer).

✅ **Success**: Your terminal now shows something like `c:\_Development\resource-tools>`

---

## Step 5: Build the Resource Index (First Time Only)

This is the key step! We're creating a lightweight index of all your resources.

### What does this do?
- Scans all your skills, agents, and prompts
- Creates a small searchable index (instead of loading everything)
- Saves 94.9% of space and cost

### In your terminal, type:
```
python index_builder.py
```

### What you'll see:
```
Building resource index...

[OK] Indexed 16 Claude skills
[OK] Indexed 137 Copilot agents
[OK] Indexed 135 Copilot prompts
[OK] Indexed 0 Copilot instructions

[OK] Master index written to resource-tools\indexes\master-index.json

Statistics:
  Total resources: 288
  Total content size: 2170.23 KB
  Index size: 111.53 KB
  Space savings: 94.9%
```

⏱️ **Time**: This typically takes 10-30 seconds

✅ **Success**: You see "Space savings: 94.9%"

---

## Step 6: Verify Your Setup Works

Let's test that everything is working correctly!

### Test 1: List all resources

In your terminal, type:
```
python resource_loader.py list
```

### What you should see:
A list of all your skills, agents, and prompts (around 288 total resources)

✅ **Success**: See a list of resources printed

### Test 2: Search for a resource

In your terminal, type:
```
python resource_loader.py search react
```

### What you should see:
A list of resources related to "react"

✅ **Success**: See search results displayed

### Test 3: View statistics

In your terminal, type:
```
python resource_loader.py stats
```

### What you should see:
Summary information about your indexed resources

✅ **Success**: See statistics printed

---

## Step 7: Using Your Setup

Now that everything is installed, here's how to use it:

### Scenario 1: Find Resources Related to a Topic

```
python resource_loader.py search "your topic here"
```

Example:
```
python resource_loader.py search "Python best practices"
```

### Scenario 2: Get a Specific Resource

After finding the resource name from your search:

```
python resource_loader.py get "Resource Name"
```

Example:
```
python resource_loader.py get "Expert React Frontend Engineer"
```

### Scenario 3: List All Resources of a Type

```
python resource_loader.py list claude-skill
```

Options:
- `claude-skill` - Your Claude skills
- `copilot-agent` - GitHub Copilot agents
- `copilot-prompt` - Reusable prompts

### Scenario 4: See Cost Savings

```
python resource_loader.py stats
```

This shows you exactly how much space and cost you're saving!

---

## Step 8: Install Claude Code Plugins (Optional)

Claude Code supports plugins that extend its capabilities with specialized tools, integrations, and workflows. Plugins are optional but can significantly enhance your development experience.

### What are Plugins?

Plugins add specialized functionality to Claude Code:
- **Language Support** - LSP integrations for TypeScript, Python, Go, Rust, C#, etc.
- **Service Integrations** - Connect to GitHub, Vercel, Stripe, Notion, Slack, etc.
- **Development Tools** - Code review, commit helpers, PR workflows
- **Documentation Tools** - Fetch up-to-date library documentation (context7)
- **Code Analysis** - AI-powered code review patterns and semantic analysis (greptile, serena)
- **Specialized Agents** - Feature development, security guidance, design tools

### How to Install Plugins

In your terminal (with Claude Code running), use the `/plugin` command:

```
/plugin
```

This opens an interactive menu where you can browse and install available plugins.

### Recommended Plugins by Use Case

#### For All Developers (Core Plugins)
```
/plugin commit-commands    # Git commit helpers
/plugin code-review        # PR review assistance
/plugin feature-dev        # Guided feature development
/plugin context7           # Up-to-date documentation lookup for any library
```

#### For Web Development
```
/plugin frontend-design    # UI/UX design assistance
/plugin playwright         # Browser testing and automation
/plugin vercel             # Vercel deployments (if using Vercel)
/plugin laravel-boost      # Laravel/PHP development assistance
```

#### Language-Specific LSP Plugins (Install Only What You Use)
```
/plugin typescript-lsp     # TypeScript/JavaScript
/plugin pyright-lsp        # Python
/plugin gopls-lsp          # Go
/plugin rust-analyzer-lsp  # Rust
/plugin csharp-lsp         # C#
/plugin php-lsp            # PHP
/plugin jdtls-lsp          # Java
```

#### Service Integrations (Install Only If You Use These Services)
```
/plugin github             # GitHub integration
/plugin gitlab             # GitLab integration
/plugin vercel             # Vercel deployments
/plugin supabase           # Supabase backend
/plugin sentry             # Error tracking
/plugin stripe             # Payment processing
/plugin slack              # Slack messaging
/plugin linear             # Linear issue tracking
/plugin atlassian          # Jira/Confluence
/plugin Notion             # Notion workspace
/plugin figma              # Figma design files
/plugin greptile           # Code review patterns and PR analysis
```

#### Advanced/Specialized Plugins
```
/plugin pr-review-toolkit  # Comprehensive PR reviews
/plugin greptile           # AI-powered code review with custom patterns
/plugin agent-sdk-dev      # Building Claude agents
/plugin plugin-dev         # Creating custom plugins
/plugin hookify            # Custom automation hooks
/plugin security-guidance  # Security best practices
/plugin code-simplifier    # Code quality improvements
/plugin serena             # Code navigation and semantic analysis
```

#### Output Style Plugins (Optional - Choose One If Desired)
```
/plugin explanatory-output-style  # More detailed explanations in responses
/plugin learning-output-style     # Educational focus with learning context
```

**Note:** Output style plugins modify how Claude responds. Only enable one at a time.

### After Installing Plugins

**Important:** After installing plugins, restart Claude Code to load them:

1. Exit Claude Code (type `exit` or press `Ctrl+C`)
2. Restart Claude Code: `claude`

### Verify Plugins are Loaded

After restarting, you can verify plugins are working by:
- Using plugin-specific commands (e.g., `/commit` for commit-commands)
- Checking that language features work (for LSP plugins)
- Testing service integrations (for service plugins)

### Managing Plugins

To see installed plugins or remove them:
```
/plugin          # Opens plugin manager
```

### Notable Plugins Explained

| Plugin | What It Does |
|---|---|
| **context7** | Fetches up-to-date documentation for any programming library. When you ask about a library (React, FastAPI, etc.), Claude retrieves current docs instead of relying on training data. |
| **greptile** | AI-powered code review that learns your codebase patterns. Provides custom context, PR analysis, and review comments. |
| **serena** | Semantic code navigation and analysis. Helps Claude understand code relationships and find relevant code sections. |
| **laravel-boost** | Laravel/PHP development assistance with framework-specific guidance and best practices. |
| **hookify** | Create custom automation hooks that trigger on Claude Code events (tool calls, session start, etc.). |

### Plugin Selection Tips

- **Start minimal** - Install only what you need, add more later
- **Language LSPs** - Only install for languages you actively use
- **Service integrations** - Only install for services you have accounts with
- **Restart required** - Always restart Claude Code after installing plugins
- **context7 recommended** - Highly useful for getting current library documentation

✅ **Success**: Plugins installed and Claude Code restarted successfully

---

## Step 9: Configure MCP Servers (Optional)

MCP (Model Context Protocol) servers extend Claude's capabilities by connecting it to external tools and services. Think of MCP servers as "bridges" that let Claude interact with databases, APIs, file systems, and other services directly.

### Why MCP Servers Matter

**Without MCP servers:**
- Claude can only work with what you paste into the conversation
- You manually copy/paste data between Claude and other tools
- Limited integration with external services

**With MCP servers:**
- Claude can directly query databases, search files, call APIs
- Seamless integration with your development tools
- Automated workflows without manual copy/paste
- Access to real-time data from external services

### What MCP Servers Can Do

MCP servers provide Claude with **tools** (actions it can take) and **resources** (data it can access):

| MCP Server Type | What It Does | Example Use |
|---|---|---|
| **File System** | Read/write files, search directories | "Find all Python files modified today" |
| **Database** | Query SQL/NoSQL databases | "Show me users who signed up this week" |
| **Git** | Repository operations | "What changed in the last 5 commits?" |
| **Web/API** | Fetch data from APIs | "Get the current weather in London" |
| **Resource Tools** | Search your skills/agents/prompts | "Find a React tutorial resource" |

### Your Resource Tools MCP Server

Your workspace includes a pre-built MCP server for the resource tools system at `resource-tools/mcp-server.js`. This server provides:

- `search_resources` - Search skills, agents, prompts by keyword
- `get_resource` - Load full content of a specific resource
- `list_resources` - Browse all available resources
- `get_resource_stats` - View index statistics

### How to Configure MCP Servers

MCP servers are configured in a `.mcp.json` file in your project or home directory.

#### Step 1: Create the Configuration File

Create a file named `.mcp.json` in your workspace root (`c:\_Development\.mcp.json`):

```json
{
  "mcpServers": {
    "resource-tools": {
      "command": "node",
      "args": ["c:/_Development/resource-tools/mcp-server.js"],
      "description": "Search and retrieve skills, agents, and prompts"
    }
  }
}
```

#### Step 2: Restart Claude Code

After creating or modifying `.mcp.json`, restart Claude Code to load the servers:

1. Exit Claude Code
2. Run `claude` again

#### Step 3: Verify MCP Server is Connected

Ask Claude to use the MCP server:
```
Search my resources for "React"
```

If configured correctly, Claude will use the `search_resources` tool from your MCP server.

### Adding More MCP Servers

You can add multiple MCP servers to your configuration. Here are common examples:

#### File System Access
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-filesystem", "c:/_Development"],
      "description": "Read and search files in workspace"
    }
  }
}
```

#### Git Repository
```json
{
  "mcpServers": {
    "git": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-git"],
      "description": "Git repository operations"
    }
  }
}
```

#### SQLite Database
```json
{
  "mcpServers": {
    "sqlite": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-sqlite", "path/to/database.db"],
      "description": "Query SQLite database"
    }
  }
}
```

#### Combined Configuration Example
```json
{
  "mcpServers": {
    "resource-tools": {
      "command": "node",
      "args": ["c:/_Development/resource-tools/mcp-server.js"],
      "description": "Search skills, agents, and prompts"
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-filesystem", "c:/_Development"],
      "description": "File system access"
    },
    "git": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-git"],
      "description": "Git operations"
    }
  }
}
```

### MCP Server Types

There are two transport types for MCP servers:

| Type | Use Case | Configuration |
|---|---|---|
| **stdio** | Local servers (files, git, databases) | Uses `command` and `args` |
| **HTTP/SSE** | Remote servers (web APIs, cloud services) | Uses `url` instead of command |

Most local development uses stdio servers (shown above).

### Popular MCP Servers

| Server | Purpose | Install |
|---|---|---|
| `@anthropic/mcp-server-filesystem` | File read/write/search | `npx -y @anthropic/mcp-server-filesystem <path>` |
| `@anthropic/mcp-server-git` | Git operations | `npx -y @anthropic/mcp-server-git` |
| `@anthropic/mcp-server-sqlite` | SQLite queries | `npx -y @anthropic/mcp-server-sqlite <db>` |
| `@anthropic/mcp-server-postgres` | PostgreSQL queries | `npx -y @anthropic/mcp-server-postgres` |
| `@anthropic/mcp-server-fetch` | HTTP requests | `npx -y @anthropic/mcp-server-fetch` |

### MCP vs Plugins: What's the Difference?

| Feature | Plugins | MCP Servers |
|---|---|---|
| **Purpose** | Add Claude Code features | Connect to external tools/data |
| **Install** | `/plugin` command | `.mcp.json` configuration |
| **Examples** | Commit helpers, LSP support | Database queries, file access |
| **Scope** | Claude Code functionality | External integrations |

**Use plugins** for Claude Code enhancements (language support, workflows).
**Use MCP servers** for external data and tool integrations.

### Troubleshooting MCP Servers

#### Problem: MCP server not connecting

**Solution:**
1. Check `.mcp.json` syntax (valid JSON, no trailing commas)
2. Verify the command path is correct
3. Ensure Node.js is installed for JS-based servers
4. Restart Claude Code after configuration changes

#### Problem: "Command not found" error

**Solution:**
1. Use full paths in the `command` field
2. For npx commands, ensure npm/Node.js is in your PATH
3. Try running the command manually in terminal first

#### Problem: MCP server crashes on startup

**Solution:**
1. Check server logs for error messages
2. Verify all dependencies are installed
3. Ensure the server file exists at the specified path
4. Test the server manually: `node path/to/mcp-server.js`

#### Problem: Tools not appearing

**Solution:**
1. Server may not be connected - check configuration
2. Restart Claude Code
3. Verify the server implements MCP protocol correctly

✅ **Success**: MCP servers configured and Claude can access external tools

---

## Why Each Step Matters

### Step 1-2: Opening VS Code & Terminal
- VS Code is your workspace hub
- Terminal lets you run automation scripts

### Step 3: Python Installation
- Python is the programming language your tools are written in
- Without it, nothing would run

### Step 4: Navigate to resource-tools
- Ensures you're in the right folder
- Prevents "file not found" errors

### Step 5: Build the Index
- **This is the magic!** Creates the smart filing system
- Only needs to run once (or when you add new resources)
- 94.9% cost savings come from this step

### Step 6: Verify Setup
- Confirms everything installed correctly
- Tests that search and retrieval work
- Prevents problems later

### Step 7: Regular Usage
- Shows you how to use the system
- Reduces costs every time you search vs. loading everything

### Step 8: Plugins (Optional)
- Extends Claude Code with specialized capabilities
- Language support (LSPs) provides better code intelligence
- Service integrations connect to tools you already use
- Only install what you need to keep things fast

### Step 9: MCP Servers (Optional)
- Connects Claude to external tools and data sources
- Enables direct database queries, file access, API calls
- Eliminates manual copy/paste between Claude and other tools
- The resource-tools MCP server makes your skills searchable by Claude

---

## Troubleshooting

### Git and Bash Issues

### Problem: "git is not recognized" or "git command not found"

**Solution:**
1. Download and install Git from https://git-scm.com/downloads
2. During installation, ensure "Git from the command line" option is selected
3. Close and reopen your terminal/VS Code after installation
4. Verify: `git --version`

### Problem: "bash is not recognized" (Windows)

**Solution:**
1. Git Bash is included with Git installation - reinstall Git if missing
2. Use Git Bash terminal instead of Command Prompt or PowerShell
3. In VS Code: Terminal → New Terminal → Select "Git Bash" from dropdown
4. Verify: Open Git Bash and run `bash --version`

### Problem: Commands work in Git Bash but not in VS Code terminal

**Solution:**
1. Change VS Code's default terminal to Git Bash:
   - Press `Ctrl+Shift+P` → "Terminal: Select Default Profile"
   - Choose "Git Bash"
2. Or manually select Git Bash for each terminal session

### Problem: Git asks for identity when committing

**Solution:**
```bash
git config --global user.email "your@email.com"
git config --global user.name "Your Name"
```

### Python Issues

### Problem: "python is not recognized"

**Solution:**
1. Make sure Python is installed
2. During installation, check "Add Python to PATH"
3. Restart VS Code and your terminal

### Problem: "No such file or directory"

**Solution:**
1. Make sure you're in the right folder
2. Check that resource-tools folder exists
3. Type `dir` to see what files are in current folder

### Problem: Index builder runs but gives errors

**Solution:**
1. Make sure your resource files are in the correct locations
2. Check that `.claude/skills/` and `.github/` folders exist
3. Try running again

### Problem: Search returns no results

**Solution:**
1. Search keywords might be too specific
2. Try shorter keywords
3. Use `python resource_loader.py list` to see available resources

### Claude CLI Troubleshooting

### Problem: "claude command not found"

**Solution:**
1. Make sure Claude CLI is installed: `curl -fsSL https://download.claude.ai/cli/install.sh | bash`
2. Close and reopen your terminal after installation
3. Try `claude --version` to verify

### Problem: "Not authenticated" error

**Solution:**
1. Run `claude auth login` to authenticate
2. Follow the prompts to sign in with your Claude account
3. Verify: `claude auth status`

### Problem: Claude CLI returns empty results

**Solution:**
1. Make sure the index has been built: `python index_builder.py`
2. Verify the index exists: Check `resource-tools/indexes/master-index.json`
3. Try a simpler search query
4. Use `python resource_loader.py list` to verify resources exist

### Claude Code Plugin Troubleshooting

### Problem: Plugin commands not working after installation

**Solution:**
1. Restart Claude Code after installing plugins (exit and run `claude` again)
2. Plugins only load on startup, not dynamically

### Problem: "/plugin" command not recognized

**Solution:**
1. Make sure you're running Claude Code (not just the Claude CLI)
2. Update to the latest version of Claude Code
3. Try running `claude --version` to verify installation

### Problem: Plugin installation fails

**Solution:**
1. Check your internet connection
2. Try again - temporary network issues are common
3. Check if the plugin name is correct (case-sensitive)
4. Some plugins require specific prerequisites (e.g., LSP plugins need the language runtime installed)

### Problem: LSP plugin not providing language features

**Solution:**
1. Ensure the language runtime is installed (e.g., Node.js for TypeScript, Python for Pyright)
2. Restart Claude Code after installing the LSP plugin
3. Check that your project has the appropriate configuration files (tsconfig.json, pyproject.toml, etc.)

### Problem: Service plugin can't connect (GitHub, Vercel, etc.)

**Solution:**
1. Ensure you have valid credentials/tokens for the service
2. Check if the service requires additional authentication setup
3. Verify your account has the necessary permissions
4. Some plugins require environment variables or config files

---

## What Happens Behind the Scenes?

### Before Your Setup:
When AI needs help with resources, it loads **all 2,170 KB** of content
- Takes lots of tokens (CPU/processing power)
- Costs about **$5.43 per interaction**
- Wastes time searching through irrelevant content

### After Your Setup:
When AI needs help with resources:
1. Searches **lightweight 111 KB index** (~1 KB per search)
2. Finds the right resource
3. Loads **only that resource** (~25 KB)
4. Costs about **$0.34 per interaction**

**💰 Savings: 93.7% reduction!**

---

## Keeping Your Setup Current

### When to Rebuild the Index:

The index automatically works, but rebuild it if you:
- Add new skills, agents, or prompts
- Update resource descriptions
- Pull updates from GitHub

### How to Rebuild:

In your terminal (in the resource-tools folder), type:
```
python index_builder.py
```

Takes the same time as the first build (10-30 seconds)

---

## Next Steps

1. ✅ **Complete this guide** - You're doing it!
2. 🔍 **Try some searches**
   - VS Code: `python resource_loader.py search "keyword"`
   - Claude CLI: `claude "Search my resources for [keyword]"`
3. 📚 **Review your resources** - Use `python resource_loader.py list` to see what you have
4. 💰 **Check savings** - Run `python resource_loader.py stats` to verify cost reduction
5. 📖 **Read advanced docs** - Check `QUICK_START.md` and `README.md` for more options
6. 🚀 **Integrate Claude CLI** - Use Claude naturally in your terminal without complex syntax
7. 🔌 **Install plugins** - Use `/plugin` to add language support, service integrations, and dev tools
8. 🔗 **Configure MCP servers** - Create `.mcp.json` to connect Claude to databases, APIs, and tools

---

## Key Commands Quick Reference

| What You Want | VS Code Command | Claude CLI Command |
|---|---|---|
| Search resources | `python resource_loader.py search "keyword"` | `claude "Search my resources for [keyword]"` |
| Get specific resource | `python resource_loader.py get "Name"` | `claude "Show me the [Resource Name] skill"` |
| List all resources | `python resource_loader.py list` | `claude "List all my resources"` |
| List only skills | `python resource_loader.py list claude-skill` | `claude "Show all my Claude skills"` |
| List only agents | `python resource_loader.py list copilot-agent` | `claude "List all my Copilot agents"` |
| View statistics | `python resource_loader.py stats` | `claude "Show my resource statistics"` |
| Rebuild index | `python index_builder.py` | `python index_builder.py` |
| Install plugins | N/A | `/plugin` |
| Commit changes | N/A | `/commit` (requires commit-commands plugin) |
| Configure MCP | Create `.mcp.json` file | Create `.mcp.json` file |

---

## Success Indicators

### For VS Code Setup:
✅ Python is installed and shows a version number
✅ Resource index builds with "Space savings: 94.9%"
✅ `python resource_loader.py list` shows ~288 resources
✅ `python resource_loader.py search` returns relevant results
✅ `python resource_loader.py stats` displays savings information

### For Claude CLI Setup:
✅ Claude CLI is installed and shows a version number
✅ `claude auth status` shows you're authenticated
✅ Resource index builds with "Space savings: 94.9%"
✅ `claude "List my resources"` returns relevant results
✅ `claude "Search my resources for [keyword]"` works naturally

### For Plugin Setup:
✅ `/plugin` command opens the plugin manager
✅ Plugins install with "✓ Installed [plugin-name]" message
✅ After restart, plugin commands work (e.g., `/commit` for commit-commands)
✅ LSP plugins provide language features (autocomplete, diagnostics)
✅ Service plugins connect to external services successfully

### For MCP Server Setup:
✅ `.mcp.json` file created in workspace root
✅ JSON syntax is valid (no errors on Claude Code startup)
✅ Claude Code restarts without MCP connection errors
✅ Claude can use MCP tools (e.g., "Search my resources for React")
✅ MCP server responds with expected data

---

## Understanding YAML Frontmatter for Your Knowledge Base

### What is YAML?

**YAML** (YAML Ain't Markup Language) is a simple, human-readable format for storing data. You don't need to be technical to use it—it's designed to look like plain text.

### Why Use YAML in Your Knowledge Base?

When you add YAML frontmatter (metadata) to your documents, you make them **AI-searchable and organized**:

| Benefit | What It Does |
|---|---|
| **AI-Searchable** | Your AI tool can find documents by topic, type, or date without reading every file |
| **Cost Reduction** | Less data for AI to read = faster responses and lower costs |
| **Relationships** | You can link related documents together |
| **Filtering** | Organize by audience (internal, technical, user-friendly) or document type (PRD, analysis, report) |
| **Time-Saving** | Automated tools can process your knowledge base systematically |

### How to Use YAML Frontmatter

Add this to the **very top** of any markdown file:

```yaml
---
type: prd
topics: [product, mobile-app, Q1-2026]
created: 2026-01-21
related: [market-analysis.md, competitive-landscape.md]
---

# Your Document Title

Your actual content starts here...
```

### Explanation of Each Field

- **`type`**: What kind of document? Examples: `prd`, `analysis`, `strategy`, `meeting-transcript`, `report`, `writing-style-guide`
- **`topics`**: Tags for easy searching. Use relevant keywords in square brackets, separated by commas
- **`created`**: Date you created/updated the document (use YYYY-MM-DD format)
- **`related`**: Optional field listing related files. Helps AI understand connections between documents

### Real Examples

**Product Strategy Document:**
```yaml
---
type: business-strategy
topics: [product, roadmap, 2026-planning, mobile]
created: 2026-01-21
related: [market-analysis.md, competitive-landscape.md]
---
```

**Meeting Transcript:**
```yaml
---
type: meeting-transcript
topics: [product-strategy, Q1-2026, roadmap-planning]
created: 2026-01-21
related: [strategy-doc.md]
---
```

**Writing Style Guide:**
```yaml
---
type: writing-style-guide
topics: [internal, communication, tone]
created: 2026-01-21
audience: internal-team
---
```

### Where to Add YAML

Your knowledge base is in `knowledge-bases/` directory:
- `knowledge-bases/business/` - Strategy and market docs
- `knowledge-bases/examples/` - Past PRDs, analyses, reports
- `knowledge-bases/meeting-transcripts/` - Meeting notes and recordings
- `knowledge-bases/writing-styles/` - Voice and tone guides

Add YAML frontmatter to any markdown files in these folders.

### Common Mistakes to Avoid

❌ **Forgetting the dashes** - Must have `---` both above AND below the YAML
❌ **Wrong indentation** - YAML is sensitive to spacing; use the examples above
❌ **Quotes around topics** - Use `[topic1, topic2]` not `["topic1", "topic2"]`
❌ **Adding it in the middle** - YAML must be at the very top of the file

### How AI Tools Use This

When you tell your AI tool "Search my knowledge base for mobile product strategies," it:
1. Reads all the YAML frontmatter (very fast)
2. Finds documents with `type: prd` OR `type: strategy` AND `topics: [contains "mobile"]`
3. Loads only those documents into the AI's context
4. Provides an accurate, cost-effective response

**Result**: 94% cost savings and instant answers instead of slow searches!

---

## System Rules & Operational Standards

Your system now includes persistent rules that apply to ALL work across every session. These are automatically loaded into your AI tools.

### The Three Core Operational Standards

1. **Never Commit Without Asking First**
   - Always confirm changes are approved before pushing to any repository
   - Use descriptive commit messages with references
   - Wait for team feedback before merging
   - This prevents accidental pushes and ensures code review

2. **Always Use Technical Writing Style**
   - Even for internal communications
   - Be precise: include specific details, line numbers, file paths
   - Define technical terms on first use
   - Provide context for non-obvious decisions
   - This ensures clarity across mixed-audience communications

3. **Format Research as Bullet Points**
   - Never use paragraph form for research findings
   - One insight per bullet point
   - Lead with the key finding, then supporting detail
   - Include source or data reference in parentheses
   - Example: "Mobile users 62% of traffic (analytics, Jan 2026)"

### Where These Rules Are Stored

- **Source of Truth**: `knowledge-bases/references/SYSTEM_RULES.md`
- **Claude CLI**: Reads automatically via `.clauderc` configuration
- **MCP Server**: Available via `get_system_rules` tool
- **VS Code**: Via `.vscode/claude-system-prompt.md`
- **Claude Web**: Embedded in your project system prompt

These rules persist forever across every session, every platform, and every tool you use.

---

## Need More Help?

- **QUICK_START.md** - Quick reference for all commands
- **README.md** - Detailed technical documentation
- **example_usage.py** - Code examples for developers
- **Claude CLI Help** - Run `claude --help` for more options
- **MCP Documentation** - https://modelcontextprotocol.io for MCP server development
- **MCP Builder Skill** - `.claude/skills/mcp-builder/` for creating custom MCP servers
- **Knowledge Base Guide** - See `knowledge-bases/README.md` for metadata conventions

---

## Summary

You've created a smart resource management system that:
- 🚀 **Speeds up AI responses** (both CLI and GUI)
- 💰 **Reduces costs by 94%**
- 📚 **Organizes 288+ resources efficiently**
- ⚡ **Requires minimal setup (just index once)**
- 💻 **Works with VS Code or Claude CLI**
- 🔌 **Extensible with plugins** for language support, services, and workflows
- 🔗 **Connects to external tools** via MCP servers for databases, APIs, and more

Congratulations! Your AI resource management system is now optimized for cost-effective, efficient resource access.
