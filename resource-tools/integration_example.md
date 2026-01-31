# Integration Examples

## How to Integrate Resource Tools into AI Workflows

This document shows practical ways to integrate the resource tools into your AI workflows.

## 1. As a Python Library

### Basic Integration

```python
# Import the functions
from resource_loader import search_resources, get_resource_by_name, list_resources

def ai_assistant(user_query: str) -> str:
    """AI assistant that uses resources efficiently"""

    # Step 1: Determine if we need external resources
    if needs_specialized_knowledge(user_query):
        # Step 2: Search for relevant resources
        results = search_resources(
            extract_keywords(user_query),
            limit=3
        )

        # Step 3: Load the most relevant resource
        if results:
            resource = get_resource_by_name(results[0]['name'])
            context = resource['content']

            # Step 4: Use resource content as context for AI
            return generate_response_with_context(user_query, context)

    # No specialized resource needed
    return generate_response(user_query)
```

### Advanced Pattern with Caching

```python
from functools import lru_cache
from resource_loader import search_resources, get_resource_by_name

# Cache loaded resources to avoid repeated file reads
@lru_cache(maxsize=10)
def load_resource_cached(name: str):
    """Load resource with caching"""
    return get_resource_by_name(name)

def smart_ai_assistant(user_query: str):
    """AI with intelligent resource selection"""

    # Map query types to resource searches
    resource_map = {
        'react': 'Expert React Frontend Engineer',
        'azure': 'Azure Principal Architect',
        'frontend': 'frontend-design',
        'pdf': 'pdf'
    }

    # Check if query matches known patterns
    for keyword, resource_name in resource_map.items():
        if keyword.lower() in user_query.lower():
            resource = load_resource_cached(resource_name)
            return f"Using {resource_name}: {resource['content'][:500]}..."

    # Fall back to search
    results = search_resources(user_query, limit=1)
    if results:
        resource = load_resource_cached(results[0]['name'])
        return f"Found relevant resource: {resource['name']}"

    return "No specialized resource needed"
```

## 2. As a Command-Line Tool

### Shell Script Integration

```bash
#!/bin/bash
# ai_helper.sh - Shell script that uses resource tools

RESOURCE_DIR="c:\_Development\resource-tools"

# Function to search resources
search_resource() {
    local query="$1"
    cd "$RESOURCE_DIR"
    python resource_loader.py search "$query"
}

# Function to load resource
load_resource() {
    local name="$1"
    cd "$RESOURCE_DIR"
    python resource_loader.py get "$name"
}

# Example: Help with React
echo "Searching for React resources..."
RESULTS=$(search_resource "react")
echo "$RESULTS"

# Load the first result
echo "Loading Expert React Frontend Engineer..."
CONTENT=$(load_resource "Expert React Frontend Engineer")
echo "$CONTENT"
```

## 3. As an API Service

### Flask Example

```python
from flask import Flask, request, jsonify
from resource_loader import search_resources, get_resource_by_name, get_stats

app = Flask(__name__)

@app.route('/api/search', methods=['GET'])
def api_search():
    """Search endpoint"""
    query = request.args.get('q', '')
    resource_type = request.args.get('type', None)
    limit = int(request.args.get('limit', 10))

    results = search_resources(query, resource_type=resource_type, limit=limit)
    return jsonify({
        'query': query,
        'count': len(results),
        'results': results
    })

@app.route('/api/resource/<name>', methods=['GET'])
def api_get_resource(name):
    """Get resource by name"""
    try:
        resource = get_resource_by_name(name)
        return jsonify({
            'success': True,
            'resource': resource
        })
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404

@app.route('/api/stats', methods=['GET'])
def api_stats():
    """Get statistics"""
    return jsonify(get_stats())

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

### Usage:
```bash
# Start the API
python api_server.py

# Use it
curl "http://localhost:5000/api/search?q=react&limit=5"
curl "http://localhost:5000/api/resource/Expert%20React%20Frontend%20Engineer"
curl "http://localhost:5000/api/stats"
```

## 4. As an MCP Server (Model Context Protocol)

### For Node.js-based AI Tools

If you have Node.js installed, you can use the MCP server:

```bash
# Start the MCP server
cd resource-tools
node mcp-server.js
```

### MCP Configuration

Add to your Claude Desktop or VS Code MCP settings:

```json
{
  "mcpServers": {
    "resource-tools": {
      "command": "python",
      "args": ["c:\\_Development\\resource-tools\\mcp_server.py"]
    }
  }
}
```

Then AI models can use these tools:
- `search_resources` - Search by keyword
- `get_resource` - Load full content
- `list_resources` - Browse all resources
- `get_resource_stats` - View statistics

## 5. In a Chatbot

### Example Chatbot Integration

```python
class ResourceAwareChat:
    def __init__(self):
        self.conversation_history = []
        self.loaded_resources = {}

    def process_message(self, user_message: str) -> str:
        # Add to history
        self.conversation_history.append({
            'role': 'user',
            'content': user_message
        })

        # Check if we need specialized resources
        resource = self.find_relevant_resource(user_message)

        if resource:
            # Load if not already loaded
            if resource['name'] not in self.loaded_resources:
                full_resource = get_resource_by_name(resource['name'])
                self.loaded_resources[resource['name']] = full_resource

            # Generate response with resource context
            response = self.generate_with_context(
                user_message,
                self.loaded_resources[resource['name']]['content']
            )
        else:
            # Generate normal response
            response = self.generate_response(user_message)

        self.conversation_history.append({
            'role': 'assistant',
            'content': response
        })

        return response

    def find_relevant_resource(self, message: str):
        """Search for relevant resources"""
        results = search_resources(message, limit=1)
        return results[0] if results else None

    def generate_with_context(self, message: str, context: str) -> str:
        """Generate response using resource context"""
        # Your AI generation logic here
        return f"Based on specialized knowledge: {context[:200]}..."

    def generate_response(self, message: str) -> str:
        """Generate normal response"""
        # Your AI generation logic here
        return f"Response to: {message}"
```

## 6. For Automated Workflows

### Example: Automated Code Review

```python
import os
from pathlib import Path
from resource_loader import search_resources, get_resource_by_name

def automated_code_review(file_path: str):
    """Review code using relevant resources"""

    # Determine what kind of file it is
    ext = Path(file_path).suffix
    file_content = Path(file_path).read_text()

    # Search for relevant coding standards/agents
    if ext in ['.jsx', '.tsx']:
        # React file
        resource = get_resource_by_name('Expert React Frontend Engineer')
        guidelines = resource['content']

        # Perform review using guidelines
        issues = check_against_guidelines(file_content, guidelines)

        return {
            'file': file_path,
            'resource_used': 'Expert React Frontend Engineer',
            'issues': issues
        }

    elif ext == '.bicep':
        # Azure Bicep file
        results = search_resources('azure bicep', limit=1)
        if results:
            resource = get_resource_by_name(results[0]['name'])
            guidelines = resource['content']

            issues = check_against_guidelines(file_content, guidelines)
            return {
                'file': file_path,
                'resource_used': results[0]['name'],
                'issues': issues
            }

    return {
        'file': file_path,
        'resource_used': None,
        'issues': []
    }

def check_against_guidelines(code: str, guidelines: str):
    """Check code against guidelines"""
    # Your analysis logic here
    return []
```

## 7. Cost-Aware AI System

### Token Budget Management

```python
from resource_loader import search_resources, get_resource_by_name

class TokenBudgetManager:
    def __init__(self, max_tokens_per_request=100000):
        self.max_tokens = max_tokens_per_request
        self.used_tokens = 0

    def can_afford(self, tokens: int) -> bool:
        return self.used_tokens + tokens <= self.max_tokens

    def estimate_tokens(self, text: str) -> int:
        """Rough token estimation"""
        return len(text) // 4

    def process_with_resources(self, query: str):
        # Search is cheap (only metadata)
        results = search_resources(query, limit=5)
        search_tokens = self.estimate_tokens(str(results))

        if not self.can_afford(search_tokens):
            return "Token budget exceeded"

        self.used_tokens += search_tokens

        # Load resource only if we can afford it
        if results:
            resource = get_resource_by_name(results[0]['name'])
            resource_tokens = self.estimate_tokens(resource['content'])

            if self.can_afford(resource_tokens):
                self.used_tokens += resource_tokens
                return f"Loaded {results[0]['name']} ({resource_tokens} tokens)"
            else:
                return f"Found {results[0]['name']} but token budget insufficient"

        return "No resources found"
```

## 8. Continuous Integration

### GitHub Actions Example

```yaml
name: Update Resource Index

on:
  push:
    paths:
      - '.claude/skills/**'
      - '.github/awesome-copilot-main/**'
  workflow_dispatch:

jobs:
  rebuild-index:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Rebuild resource index
        run: |
          cd resource-tools
          python index_builder.py

      - name: Commit updated indexes
        run: |
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"
          git add resource-tools/indexes/
          git commit -m "Update resource indexes" || echo "No changes"
          git push
```

## Key Integration Principles

1. **Search First** - Always search metadata before loading content
2. **Cache Resources** - Cache loaded resources to avoid repeated reads
3. **Token Budgets** - Monitor token usage and load resources selectively
4. **Lazy Loading** - Only load when necessary
5. **Type Filtering** - Use type filters to narrow searches
6. **Fallback Logic** - Have fallbacks when resources aren't found

## Performance Tips

1. **Keep indexes in memory** - Load once, query many times
2. **Use LRU cache** - Cache most recently used resources
3. **Batch searches** - If searching multiple times, combine queries
4. **Monitor token usage** - Track costs in production
5. **Regular rebuilds** - Keep indexes fresh with automated rebuilds

## Monitoring and Debugging

```python
import logging
from resource_loader import search_resources

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def search_with_logging(query: str):
    logger.info(f"Searching for: {query}")
    results = search_resources(query)
    logger.info(f"Found {len(results)} results")

    for r in results:
        logger.debug(f"  - {r['name']} ({r['size']} bytes)")

    return results
```

## Conclusion

These integration patterns show how to:
- Reduce AI token costs by 90%+
- Provide specialized knowledge on-demand
- Scale to hundreds or thousands of resources
- Build cost-aware AI systems

Choose the integration pattern that fits your use case!
