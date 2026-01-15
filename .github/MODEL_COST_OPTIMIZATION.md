# Model Cost Optimization Guide

## Overview

This guide helps you minimize GitHub Copilot premium token usage by directing tasks to cost-optimized AI models. Proper model selection can save **60-80% on premium tokens** for routine tasks.

## Cost Tiers

| Tier | Multiplier | Models | Best For |
|------|-----------|--------|----------|
| **Free** | 0x | GPT-4.1, GPT-5 mini | Routine tasks, included in all plans |
| **Standard Premium** | 1x | GPT-5, GPT-5 Codex, Claude Sonnet 4/4.5, Gemini 2.5 Pro | Complex code, advanced reasoning |
| **Ultra Premium** | 10x | Claude Opus 4.1 | Architecture, large codebases only |

## Model Selection Strategy

### Use Free Models (0x) For:
- ✅ Documentation updates and formatting
- ✅ Simple code reviews and pattern matching
- ✅ Adding comments to code
- ✅ Basic CRUD operations
- ✅ File manipulation (DOCX, PDF, PPTX)
- ✅ Memory organization and context tracking
- ✅ Simple refactoring and code cleanup

**Recommended Models:**
- **GPT-4.1**: Balanced general-purpose (vision-capable)
- **GPT-5 mini**: Fastest for simple tasks

### Use Standard Premium (1x) For:
- ⚠️ Complex algorithm optimization
- ⚠️ Financial model creation (Excel formulas)
- ⚠️ Advanced SQL query optimization
- ⚠️ Multi-file refactoring
- ⚠️ API integration and authentication
- ⚠️ Complex Dataverse/Python workflows

**Recommended Models:**
- **GPT-5 Codex**: Code optimization, refactoring
- **Claude Sonnet 4.5**: Complex Python, advanced reasoning
- **Claude Sonnet 4**: Enterprise tasks, robust code

### Use Ultra Premium (10x) ONLY For:
- 🚨 Architectural design reviews
- 🚨 Large codebase analysis (1M+ tokens)
- 🚨 Critical system design decisions

**Model:**
- **Claude Opus 4.1**: Reserved for rare, complex tasks

## Current Configuration

### Skills (Document Processing)
| Skill | Model | Reasoning |
|-------|-------|-----------|
| **DOCX** | GPT-4.1 (0x) | Simple OOXML manipulation |
| **XLSX** | Claude Sonnet 4.5 (1x) | Complex formulas require accuracy |
| **PDF** | GPT-4.1 (0x) | Text extraction, basic operations |
| **PPTX** | GPT-4.1 (0x) | Simple OOXML manipulation |

### Prompts (Reusable Templates)
| Prompt | Model | Reasoning |
|--------|-------|-----------|
| **sql-code-review** | GPT-5 mini (0x) | Pattern-based review |
| **sql-optimization** | GPT-5 Codex (1x) | Algorithmic query tuning |
| **add-educational-comments** | GPT-4.1 (0x) | Simple text additions |
| **github-copilot-starter** | Claude Sonnet 4 (1x) | Complex setup workflow |
| **prompt-builder** | GPT-4.1 (0x) | Structured text generation |
| **remember** | GPT-4.1 (0x) | Simple organization |
| **remember-interactive-programming** | GPT-4.1 (0x) | Workflow reminder |
| **write-coding-standards** | GPT-5 mini (0x) | Pattern recognition |
| **model-recommendation** | Auto (0x) | Auto-selects appropriate model |

## Cost Savings Examples

### Example 1: Documentation Update
```
❌ Before: Claude Opus 4.1 (10x) = 1000 tokens × 10 = 10,000 premium tokens
✅ After: GPT-4.1 (0x) = 1000 tokens × 0 = 0 premium tokens
💰 Savings: 100% (10,000 premium tokens saved)
```

### Example 2: Code Review
```
❌ Before: Claude Sonnet 4.5 (1x) = 5000 tokens × 1 = 5,000 premium tokens
✅ After: GPT-5 mini (0x) = 5000 tokens × 0 = 0 premium tokens
💰 Savings: 100% (5,000 premium tokens saved)
```

### Example 3: Excel Formula Creation
```
⚠️ Keep: Claude Sonnet 4.5 (1x) = 3000 tokens × 1 = 3,000 premium tokens
Reason: Complex formulas require accuracy - worth the cost
```

## Usage Guidelines

### When to Override Model Selection

**Force Free Model:**
```
"Use GPT-4.1 to review this code for basic issues"
```

**Force Premium When Needed:**
```
"Use Claude Sonnet 4.5 to optimize these complex algorithms"
```

**Let Auto-Selection Decide:**
```
"Review this code" (Auto will choose appropriate model)
```

### Monitoring Token Usage

**GitHub Copilot Dashboard:**
1. Open VS Code Settings
2. Navigate to Copilot → Usage
3. Monitor premium token consumption
4. Adjust model selections if exceeding budget

**Subscription Limits:**
- **Free**: 2K completions + 50 chat/month (0x models only)
- **Pro**: Unlimited 0x + 1,000 premium requests/month
- **Pro+**: Unlimited 0x + 5,000 premium requests/month

## Best Practices

1. **Default to Free Models**: Let auto-selection use 0x models for routine tasks
2. **Be Explicit for Premium**: Only request premium models when complexity justifies cost
3. **Review Periodically**: Check which tasks consume most premium tokens
4. **Update Configurations**: Adjust `model:` fields in skills/prompts based on actual needs
5. **Test Free Models First**: Try GPT-4.1 or GPT-5 mini before escalating to premium

## Quick Reference

```yaml
# In .prompt.md or SKILL.md frontmatter

# Cost-effective defaults
model: GPT-4.1          # Most tasks (0x)
model: GPT-5 mini       # Simple/fast tasks (0x)

# Premium when justified
model: GPT-5 Codex      # Code optimization (1x)
model: Claude Sonnet 4.5 # Complex reasoning (1x)

# Rare/critical only
model: Claude Opus 4.1  # Architecture (10x) - use sparingly
```

## ROI Calculator

**Scenario: 100 documentation tasks per month**
- Before (unoptimized): 100 × 2000 tokens × 1x avg = 200,000 premium tokens
- After (optimized): 100 × 2000 tokens × 0x = 0 premium tokens
- **Monthly Savings**: 200,000 premium tokens (stays within Pro tier)

**Scenario: Mixed workload (80% routine, 20% complex)**
- Before: 100 tasks × 1x avg = 100,000 premium tokens
- After: 80 tasks × 0x + 20 tasks × 1x = 20,000 premium tokens
- **Monthly Savings**: 80% reduction (80,000 premium tokens)

## Resources

- [GitHub Copilot Pricing](https://github.com/features/copilot)
- [Model Capabilities Matrix](.github/prompts/model-recommendation.prompt.md)
- [VS Code Model Selection](https://code.visualstudio.com/docs/copilot/copilot-customization)

---

**Last Updated**: January 15, 2026  
**Maintained By**: AI Coding Agent  
**Review Frequency**: Quarterly or when new models added
