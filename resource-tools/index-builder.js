#!/usr/bin/env node

/**
 * Resource Index Builder
 * Scans .claude/skills and .github/awesome-copilot-main to create lightweight indexes
 * This reduces AI token costs by providing metadata without full content
 */

const fs = require('fs');
const path = require('path');

const ROOT_DIR = path.resolve(__dirname, '..');
const OUTPUT_DIR = path.join(ROOT_DIR, 'resource-tools', 'indexes');

// Ensure output directory exists
if (!fs.existsSync(OUTPUT_DIR)) {
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

/**
 * Parse frontmatter from markdown files
 */
function parseFrontmatter(content) {
  const frontmatterRegex = /^---\s*\n([\s\S]*?)\n---/;
  const match = content.match(frontmatterRegex);

  if (!match) return {};

  const frontmatter = {};
  const lines = match[1].split('\n');

  for (const line of lines) {
    const colonIndex = line.indexOf(':');
    if (colonIndex === -1) continue;

    const key = line.slice(0, colonIndex).trim();
    let value = line.slice(colonIndex + 1).trim();

    // Remove quotes if present
    if ((value.startsWith('"') && value.endsWith('"')) ||
        (value.startsWith("'") && value.endsWith("'"))) {
      value = value.slice(1, -1);
    }

    frontmatter[key] = value;
  }

  return frontmatter;
}

/**
 * Extract first paragraph after frontmatter as summary
 */
function extractSummary(content, maxLength = 200) {
  // Remove frontmatter
  const withoutFrontmatter = content.replace(/^---\s*\n[\s\S]*?\n---\s*\n/, '');

  // Get first non-empty paragraph
  const paragraphs = withoutFrontmatter.split('\n\n');
  for (const para of paragraphs) {
    const cleaned = para.trim().replace(/^#+\s*/, ''); // Remove headers
    if (cleaned && !cleaned.startsWith('```')) {
      return cleaned.length > maxLength
        ? cleaned.slice(0, maxLength) + '...'
        : cleaned;
    }
  }

  return '';
}

/**
 * Index Claude skills from .claude/skills
 */
function indexClaudeSkills() {
  const skillsDir = path.join(ROOT_DIR, '.claude', 'skills');
  if (!fs.existsSync(skillsDir)) {
    console.log('No .claude/skills directory found');
    return [];
  }

  const skills = [];
  const skillDirs = fs.readdirSync(skillsDir);

  for (const skillName of skillDirs) {
    const skillPath = path.join(skillsDir, skillName);
    const skillFile = path.join(skillPath, 'SKILL.md');

    if (!fs.existsSync(skillFile)) continue;

    const content = fs.readFileSync(skillFile, 'utf-8');
    const frontmatter = parseFrontmatter(content);
    const summary = extractSummary(content);

    skills.push({
      name: frontmatter.name || skillName,
      description: frontmatter.description || summary,
      type: 'claude-skill',
      path: path.relative(ROOT_DIR, skillFile),
      tags: frontmatter.tags ? frontmatter.tags.split(',').map(t => t.trim()) : [],
      size: Buffer.byteLength(content, 'utf-8')
    });
  }

  return skills;
}

/**
 * Index agents from .github/awesome-copilot-main/agents
 */
function indexAgents() {
  const agentsDir = path.join(ROOT_DIR, '.github', 'awesome-copilot-main', 'agents');
  if (!fs.existsSync(agentsDir)) {
    console.log('No agents directory found');
    return [];
  }

  const agents = [];
  const agentFiles = fs.readdirSync(agentsDir).filter(f => f.endsWith('.agent.md'));

  for (const agentFile of agentFiles) {
    const agentPath = path.join(agentsDir, agentFile);
    const content = fs.readFileSync(agentPath, 'utf-8');
    const frontmatter = parseFrontmatter(content);

    agents.push({
      name: frontmatter.name || path.basename(agentFile, '.agent.md'),
      description: frontmatter.description || '',
      type: 'copilot-agent',
      path: path.relative(ROOT_DIR, agentPath),
      tools: frontmatter.tools ? JSON.parse(frontmatter.tools.replace(/'/g, '"')) : [],
      size: Buffer.byteLength(content, 'utf-8')
    });
  }

  return agents;
}

/**
 * Index prompts from .github/awesome-copilot-main/prompts
 */
function indexPrompts() {
  const promptsDir = path.join(ROOT_DIR, '.github', 'awesome-copilot-main', 'prompts');
  if (!fs.existsSync(promptsDir)) {
    console.log('No prompts directory found');
    return [];
  }

  const prompts = [];
  const promptFiles = fs.readdirSync(promptsDir).filter(f => f.endsWith('.prompt.md'));

  for (const promptFile of promptFiles) {
    const promptPath = path.join(promptsDir, promptFile);
    const content = fs.readFileSync(promptPath, 'utf-8');
    const frontmatter = parseFrontmatter(content);

    prompts.push({
      name: frontmatter.name || path.basename(promptFile, '.prompt.md'),
      description: frontmatter.description || '',
      type: 'copilot-prompt',
      path: path.relative(ROOT_DIR, promptPath),
      tags: frontmatter.tags ? frontmatter.tags.split(',').map(t => t.trim()) : [],
      size: Buffer.byteLength(content, 'utf-8')
    });
  }

  return prompts;
}

/**
 * Index instructions from .github/awesome-copilot-main/instructions
 */
function indexInstructions() {
  const instructionsDir = path.join(ROOT_DIR, '.github', 'awesome-copilot-main', 'instructions');
  if (!fs.existsSync(instructionsDir)) {
    console.log('No instructions directory found');
    return [];
  }

  const instructions = [];
  const instructionFiles = fs.readdirSync(instructionsDir).filter(f => f.endsWith('.instruction.md'));

  for (const instructionFile of instructionFiles) {
    const instructionPath = path.join(instructionsDir, instructionFile);
    const content = fs.readFileSync(instructionPath, 'utf-8');
    const frontmatter = parseFrontmatter(content);

    instructions.push({
      name: frontmatter.name || path.basename(instructionFile, '.instruction.md'),
      description: frontmatter.description || '',
      type: 'copilot-instruction',
      path: path.relative(ROOT_DIR, instructionPath),
      appliesTo: frontmatter.appliesTo || frontmatter.patterns || '',
      size: Buffer.byteLength(content, 'utf-8')
    });
  }

  return instructions;
}

/**
 * Build master index
 */
function buildIndex() {
  console.log('Building resource index...\n');

  const skills = indexClaudeSkills();
  console.log(`✓ Indexed ${skills.length} Claude skills`);

  const agents = indexAgents();
  console.log(`✓ Indexed ${agents.length} Copilot agents`);

  const prompts = indexPrompts();
  console.log(`✓ Indexed ${prompts.length} Copilot prompts`);

  const instructions = indexInstructions();
  console.log(`✓ Indexed ${instructions.length} Copilot instructions`);

  const masterIndex = {
    generatedAt: new Date().toISOString(),
    stats: {
      totalResources: skills.length + agents.length + prompts.length + instructions.length,
      skills: skills.length,
      agents: agents.length,
      prompts: prompts.length,
      instructions: instructions.length
    },
    resources: {
      skills,
      agents,
      prompts,
      instructions
    }
  };

  // Write master index
  const indexPath = path.join(OUTPUT_DIR, 'master-index.json');
  fs.writeFileSync(indexPath, JSON.stringify(masterIndex, null, 2));
  console.log(`\n✓ Master index written to ${path.relative(ROOT_DIR, indexPath)}`);

  // Write separate indexes for faster lookups
  fs.writeFileSync(path.join(OUTPUT_DIR, 'skills-index.json'), JSON.stringify(skills, null, 2));
  fs.writeFileSync(path.join(OUTPUT_DIR, 'agents-index.json'), JSON.stringify(agents, null, 2));
  fs.writeFileSync(path.join(OUTPUT_DIR, 'prompts-index.json'), JSON.stringify(prompts, null, 2));
  fs.writeFileSync(path.join(OUTPUT_DIR, 'instructions-index.json'), JSON.stringify(instructions, null, 2));

  console.log('✓ Separate indexes written\n');

  // Print statistics
  const totalSize = [...skills, ...agents, ...prompts, ...instructions]
    .reduce((sum, r) => sum + r.size, 0);

  console.log('Statistics:');
  console.log(`  Total resources: ${masterIndex.stats.totalResources}`);
  console.log(`  Total content size: ${(totalSize / 1024).toFixed(2)} KB`);
  console.log(`  Index size: ${(Buffer.byteLength(JSON.stringify(masterIndex), 'utf-8') / 1024).toFixed(2)} KB`);
  console.log(`  Space savings: ${((1 - (Buffer.byteLength(JSON.stringify(masterIndex), 'utf-8') / totalSize)) * 100).toFixed(1)}%`);
}

// Run the indexer
buildIndex();
