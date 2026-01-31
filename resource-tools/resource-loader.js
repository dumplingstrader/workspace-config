#!/usr/bin/env node

/**
 * Resource Loader
 * Provides functions to search and load resources efficiently
 * Designed for use as a tool by AI models to minimize token usage
 */

const fs = require('fs');
const path = require('path');

const ROOT_DIR = path.resolve(__dirname, '..');
const INDEX_DIR = path.join(__dirname, 'indexes');

/**
 * Load index files
 */
function loadIndex(type = 'master') {
  const indexPath = path.join(INDEX_DIR, `${type}-index.json`);
  if (!fs.existsSync(indexPath)) {
    throw new Error(`Index not found: ${type}. Run index-builder.js first.`);
  }
  return JSON.parse(fs.readFileSync(indexPath, 'utf-8'));
}

/**
 * Search resources by query
 */
function searchResources(query, options = {}) {
  const {
    type = null,        // Filter by type: 'claude-skill', 'copilot-agent', 'copilot-prompt', 'copilot-instruction'
    tags = [],          // Filter by tags
    limit = 10,         // Max results
    includeContent = false  // Whether to load full content
  } = options;

  const masterIndex = loadIndex('master');
  const allResources = [
    ...masterIndex.resources.skills,
    ...masterIndex.resources.agents,
    ...masterIndex.resources.prompts,
    ...masterIndex.resources.instructions
  ];

  // Filter by type if specified
  let filtered = type ? allResources.filter(r => r.type === type) : allResources;

  // Filter by tags if specified
  if (tags.length > 0) {
    filtered = filtered.filter(r =>
      r.tags && tags.some(tag => r.tags.includes(tag))
    );
  }

  // Search in name and description
  const queryLower = query.toLowerCase();
  const results = filtered.filter(r =>
    r.name.toLowerCase().includes(queryLower) ||
    (r.description && r.description.toLowerCase().includes(queryLower))
  );

  // Sort by relevance (exact matches first, then name matches, then description matches)
  results.sort((a, b) => {
    const aNameExact = a.name.toLowerCase() === queryLower ? 1 : 0;
    const bNameExact = b.name.toLowerCase() === queryLower ? 1 : 0;
    if (aNameExact !== bNameExact) return bNameExact - aNameExact;

    const aNameMatch = a.name.toLowerCase().includes(queryLower) ? 1 : 0;
    const bNameMatch = b.name.toLowerCase().includes(queryLower) ? 1 : 0;
    if (aNameMatch !== bNameMatch) return bNameMatch - aNameMatch;

    return a.name.localeCompare(b.name);
  });

  // Limit results
  const limitedResults = results.slice(0, limit);

  // Load full content if requested
  if (includeContent) {
    return limitedResults.map(r => ({
      ...r,
      content: loadResourceContent(r.path)
    }));
  }

  return limitedResults;
}

/**
 * Load full content of a resource by path
 */
function loadResourceContent(resourcePath) {
  const fullPath = path.join(ROOT_DIR, resourcePath);
  if (!fs.existsSync(fullPath)) {
    throw new Error(`Resource not found: ${resourcePath}`);
  }
  return fs.readFileSync(fullPath, 'utf-8');
}

/**
 * Get resource by exact name
 */
function getResourceByName(name, type = null) {
  const masterIndex = loadIndex('master');
  const allResources = [
    ...masterIndex.resources.skills,
    ...masterIndex.resources.agents,
    ...masterIndex.resources.prompts,
    ...masterIndex.resources.instructions
  ];

  const filtered = type ? allResources.filter(r => r.type === type) : allResources;
  const resource = filtered.find(r => r.name === name || r.name.toLowerCase() === name.toLowerCase());

  if (!resource) {
    throw new Error(`Resource not found: ${name}`);
  }

  return {
    ...resource,
    content: loadResourceContent(resource.path)
  };
}

/**
 * List all available resources (metadata only)
 */
function listResources(type = null) {
  const masterIndex = loadIndex('master');

  if (type) {
    switch (type) {
      case 'claude-skill':
        return masterIndex.resources.skills;
      case 'copilot-agent':
        return masterIndex.resources.agents;
      case 'copilot-prompt':
        return masterIndex.resources.prompts;
      case 'copilot-instruction':
        return masterIndex.resources.instructions;
      default:
        throw new Error(`Unknown type: ${type}`);
    }
  }

  return [
    ...masterIndex.resources.skills,
    ...masterIndex.resources.agents,
    ...masterIndex.resources.prompts,
    ...masterIndex.resources.instructions
  ];
}

/**
 * Get statistics about indexed resources
 */
function getStats() {
  const masterIndex = loadIndex('master');
  return {
    ...masterIndex.stats,
    generatedAt: masterIndex.generatedAt
  };
}

/**
 * CLI interface
 */
function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  try {
    switch (command) {
      case 'search': {
        const query = args[1];
        if (!query) {
          console.error('Usage: resource-loader.js search <query> [--type=<type>] [--content]');
          process.exit(1);
        }

        const type = args.find(a => a.startsWith('--type='))?.split('=')[1];
        const includeContent = args.includes('--content');

        const results = searchResources(query, { type, includeContent });
        console.log(JSON.stringify(results, null, 2));
        break;
      }

      case 'get': {
        const name = args[1];
        if (!name) {
          console.error('Usage: resource-loader.js get <name> [--type=<type>]');
          process.exit(1);
        }

        const type = args.find(a => a.startsWith('--type='))?.split('=')[1];
        const resource = getResourceByName(name, type);
        console.log(JSON.stringify(resource, null, 2));
        break;
      }

      case 'list': {
        const type = args[1];
        const resources = listResources(type);
        console.log(JSON.stringify(resources, null, 2));
        break;
      }

      case 'stats': {
        const stats = getStats();
        console.log(JSON.stringify(stats, null, 2));
        break;
      }

      default:
        console.log('Usage:');
        console.log('  resource-loader.js search <query> [--type=<type>] [--content]');
        console.log('  resource-loader.js get <name> [--type=<type>]');
        console.log('  resource-loader.js list [type]');
        console.log('  resource-loader.js stats');
        console.log('');
        console.log('Types: claude-skill, copilot-agent, copilot-prompt, copilot-instruction');
    }
  } catch (error) {
    console.error('Error:', error.message);
    process.exit(1);
  }
}

// Export functions for programmatic use
if (require.main === module) {
  main();
} else {
  module.exports = {
    searchResources,
    loadResourceContent,
    getResourceByName,
    listResources,
    getStats
  };
}
