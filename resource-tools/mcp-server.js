#!/usr/bin/env node

/**
 * MCP Server for Resource Tools
 * Exposes resource search and retrieval as MCP tools for AI models
 * This enables cost-effective access to skills, agents, prompts, and instructions
 */

const { searchResources, getResourceByName, listResources, getStats } = require('./resource-loader');

/**
 * MCP Server implementation using stdio
 */
class MCPResourceServer {
  constructor() {
    this.tools = [
      {
        name: 'search_resources',
        description: 'Search for skills, agents, prompts, or instructions by keyword. Returns metadata only (lightweight). Use get_resource to load full content.',
        inputSchema: {
          type: 'object',
          properties: {
            query: {
              type: 'string',
              description: 'Search query (searches in name and description)'
            },
            type: {
              type: 'string',
              enum: ['claude-skill', 'copilot-agent', 'copilot-prompt', 'copilot-instruction'],
              description: 'Filter by resource type (optional)'
            },
            tags: {
              type: 'array',
              items: { type: 'string' },
              description: 'Filter by tags (optional)'
            },
            limit: {
              type: 'number',
              description: 'Maximum number of results (default: 10)',
              default: 10
            }
          },
          required: ['query']
        }
      },
      {
        name: 'get_resource',
        description: 'Load full content of a specific resource by name. Use this after search_resources to get detailed instructions.',
        inputSchema: {
          type: 'object',
          properties: {
            name: {
              type: 'string',
              description: 'Exact name of the resource'
            },
            type: {
              type: 'string',
              enum: ['claude-skill', 'copilot-agent', 'copilot-prompt', 'copilot-instruction'],
              description: 'Resource type (optional, helps with disambiguation)'
            }
          },
          required: ['name']
        }
      },
      {
        name: 'list_resources',
        description: 'List all available resources with metadata (no content). Useful for browsing available resources.',
        inputSchema: {
          type: 'object',
          properties: {
            type: {
              type: 'string',
              enum: ['claude-skill', 'copilot-agent', 'copilot-prompt', 'copilot-instruction'],
              description: 'Filter by resource type (optional)'
            }
          }
        }
      },
      {
        name: 'get_system_rules',
        description: 'Retrieve the system rules and governance guidelines that apply to all work. Returns the current system rules from the knowledge base.',
        inputSchema: {
          type: 'object',
          properties: {}
        }
      },
      {
        name: 'get_resource_stats',
        description: 'Get statistics about indexed resources (counts, last update time).',
        inputSchema: {
          type: 'object',
          properties: {}
        }
      }
    ];
  }

  /**
   * Handle tool calls
   */
  async handleToolCall(toolName, args) {
    try {
      switch (toolName) {
        case 'search_resources': {
          const { query, type, tags = [], limit = 10 } = args;
          const results = searchResources(query, { type, tags, limit, includeContent: false });
          return {
            success: true,
            results: results.map(r => ({
              name: r.name,
              type: r.type,
              description: r.description,
              path: r.path,
              size: `${(r.size / 1024).toFixed(1)} KB`,
              ...(r.tags && { tags: r.tags }),
              ...(r.tools && { tools: r.tools })
            })),
            count: results.length,
            message: results.length > 0
              ? `Found ${results.length} resource(s). Use get_resource to load full content.`
              : 'No resources found matching your query.'
          };
        }

        case 'get_resource': {
          const { name, type } = args;
          const resource = getResourceByName(name, type);
          return {
            success: true,
            resource: {
              name: resource.name,
              type: resource.type,
              description: resource.description,
              path: resource.path,
              size: `${(resource.size / 1024).toFixed(1)} KB`,
              content: resource.content,
              ...(resource.tags && { tags: resource.tags }),
              ...(resource.tools && { tools: resource.tools })
            }
          };
        }

        case 'list_resources': {
          const { type } = args;
          const resources = listResources(type);
          return {
            success: true,
            resources: resources.map(r => ({
              name: r.name,
              type: r.type,
              description: r.description,
              size: `${(r.size / 1024).toFixed(1)} KB`,
              ...(r.tags && { tags: r.tags })
            })),
            count: resources.length
          };
        }

        case 'get_system_rules': {
          const fs = require('fs');
          const path = require('path');
          const rulesPath = path.join(__dirname, '..', 'knowledge-bases', 'references', 'SYSTEM_RULES.md');
          
          try {
            const rulesContent = fs.readFileSync(rulesPath, 'utf-8');
            return {
              success: true,
              systemRules: rulesContent,
              message: 'System rules loaded. These rules apply to all work sessions.'
            };
          } catch (error) {
            return {
              success: false,
              error: `Could not load system rules: ${error.message}`,
              path: rulesPath
            };
          }
        }

        case 'get_resource_stats': {
          const stats = getStats();
          return {
            success: true,
            stats
          };
        }

        default:
          return {
            success: false,
            error: `Unknown tool: ${toolName}`
          };
      }
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Start MCP server with stdio transport
   */
  start() {
    const readline = require('readline');
    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout,
      terminal: false
    });

    // Send server info on startup
    this.sendMessage({
      jsonrpc: '2.0',
      method: 'server/info',
      params: {
        name: 'Resource Tools MCP Server',
        version: '1.0.0',
        description: 'Search and retrieve skills, agents, prompts, and instructions',
        tools: this.tools
      }
    });

    // Handle incoming messages
    rl.on('line', async (line) => {
      try {
        const message = JSON.parse(line);

        if (message.method === 'tools/list') {
          this.sendMessage({
            jsonrpc: '2.0',
            id: message.id,
            result: { tools: this.tools }
          });
        } else if (message.method === 'tools/call') {
          const { name, arguments: args } = message.params;
          const result = await this.handleToolCall(name, args);

          this.sendMessage({
            jsonrpc: '2.0',
            id: message.id,
            result
          });
        }
      } catch (error) {
        this.sendMessage({
          jsonrpc: '2.0',
          id: message.id || null,
          error: {
            code: -32603,
            message: error.message
          }
        });
      }
    });

    rl.on('close', () => {
      process.exit(0);
    });
  }

  /**
   * Send message to stdout
   */
  sendMessage(message) {
    console.log(JSON.stringify(message));
  }
}

// Start server
if (require.main === module) {
  const server = new MCPResourceServer();
  server.start();
}

module.exports = MCPResourceServer;
