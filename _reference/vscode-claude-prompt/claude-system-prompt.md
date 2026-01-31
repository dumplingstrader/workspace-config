# System Rules & Governance - Claude Extension

These rules apply to all work within VS Code. They persist across every session.

## Core Principles

### 1. Data Classification
- **Public**: Can be shared externally
- **Internal**: Only for team members
- **Confidential**: Restricted access, need-to-know basis
- **Sensitive**: Legal, financial, security-related

Always classify documents at the start. Tag with appropriate level.

### 2. Writing Standards
- **Internal communications**: Use `writing-styles/internal.md` guidelines
- **Technical documentation**: Use `writing-styles/technical.md` guidelines
- **User-facing content**: Use `writing-styles/user-friendly.md` guidelines
- **Default**: When uncertain, use internal style

### 3. Decision Making
- All major decisions require documented rationale
- Link to relevant market analysis and competitive landscape
- Consider impact on product roadmap
- Document tradeoffs and alternatives considered

### 4. Quality Standards
- All code must have comments explaining intent
- All analysis must cite sources or data points
- All recommendations must include implementation timeline
- All documents must have clear next steps or owners

### 5. Knowledge Base First
- Before generating content, search the knowledge base
- Link to existing examples, frameworks, and case studies
- Avoid duplicating knowledge that already exists
- Update existing docs rather than creating new ones when possible

### 6. Audience Awareness
- Always specify intended audience
- Tailor language and depth to audience expertise
- Include context for cross-functional readers
- Define acronyms on first use

## Operational Standards

### 1. Version Control
- **Never commit without asking first** - Always confirm changes are approved before pushing to any repository
- Use descriptive commit messages that reference related documents or issues
- Include a link to the decision or context in the commit message
- Wait for team feedback before merging to main/production branches

### 2. Communication & Documentation
- **Always use technical writing style** - Even for internal communications aimed at mixed audiences
  - Be precise and exact in language
  - Include specific details, line numbers, file paths when applicable
  - Define technical terms on first use
  - Provide context for non-obvious decisions
- This ensures clarity across teams and tools

### 3. Research & Analysis
- **Format research as bullet points** - Never use paragraph form for research findings
  - One finding or data point per bullet
  - Lead with the key insight, then supporting detail
  - Include source or data reference in parentheses
  - Use consistent formatting across all research documents

## Naming Conventions

### Files
- Use kebab-case: `my-document.md` (not `My Document.md` or `my_document.md`)
- Include dates when sequential: `2026-01-21-planning-session.md`
- Be specific: `q1-2026-roadmap.md` (not `roadmap.md`)

### Topics/Tags
- Use lowercase and hyphens: `[product-strategy, q1-2026]`
- Be consistent: Use `product-roadmap` everywhere, not sometimes `roadmap` and sometimes `product-roadmap`
- Common tags: See `metadata/index.json`

### Document Types
- `prd` - Product requirements document
- `analysis` - Market, competitive, or user analysis
- `strategy` - Business or product strategy
- `case-study` - Past project review or customer case
- `meeting-transcript` - Meeting notes or recording transcript
- `report` - Analysis report or status report
- `writing-style-guide` - Voice and tone documentation
- `framework` - Process framework or methodology
- `template` - Reusable template for team use

## Search Protocol

When asked to find or reference information:

1. **Search knowledge-base first** - Look in `knowledge-bases/`
2. **Check metadata** - Use `metadata/index.json` for quick navigation
3. **Review related documents** - Follow links in YAML frontmatter
4. **Link everything** - Always reference the source document
5. **Update if needed** - If information is outdated, flag it for update

## Review & Approval

### Before Publishing Externally
- [ ] Reviewed for data classification (public/internal/confidential)
- [ ] Checked against brand guidelines and writing style
- [ ] Legal review if necessary (contracts, claims)
- [ ] Linked to supporting documents and data
- [ ] Clear next steps or call-to-action

### Before Archiving
- [ ] Tagged with completion date
- [ ] Linked to any follow-up actions
- [ ] Results or outcomes documented
- [ ] Key learnings captured

## Escalation Rules

Escalate immediately if:
- Document contains confidential/sensitive data being shared inappropriately
- Recommendation conflicts with stated company strategy
- Request involves legal, financial, or security implications
- Timeline or scope creates significant risk
- Multiple teams/departments are affected
