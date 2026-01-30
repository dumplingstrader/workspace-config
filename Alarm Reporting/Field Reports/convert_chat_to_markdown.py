#!/usr/bin/env python3
"""
Convert GitHub Copilot chat JSON export to readable markdown format.
"""

import json
import sys
from pathlib import Path
from datetime import datetime

def extract_text_from_parts(parts):
    """Extract text from message parts."""
    if not parts:
        return ""
    
    text_parts = []
    for part in parts:
        if isinstance(part, dict) and 'text' in part:
            text_parts.append(part['text'])
    
    return "\n".join(text_parts)

def format_response_content(response_items):
    """Format response items into readable text."""
    content_parts = []
    
    for item in response_items:
        if isinstance(item, dict):
            kind = item.get('kind', '')
            
            # Handle text responses
            if 'value' in item and isinstance(item['value'], str):
                content_parts.append(item['value'])
            
            # Handle thinking/reasoning
            elif kind == 'thinking' and item.get('value'):
                content_parts.append(f"*[Thinking: {item['value'][:200]}...]*" if len(item['value']) > 200 else f"*[Thinking: {item['value']}]*")
            
            # Handle tool invocations
            elif kind == 'toolInvocationSerialized' and 'invocationMessage' in item:
                inv_msg = item['invocationMessage']
                if isinstance(inv_msg, dict) and 'value' in inv_msg:
                    content_parts.append(f"🔧 *Tool: {inv_msg['value']}*")
            
            # Handle code blocks
            elif kind == 'codeblockUri' or kind == 'codeblock':
                if 'uri' in item:
                    content_parts.append(f"📄 *Code: {item.get('uri', {}).get('path', 'unknown')}*")
    
    return "\n\n".join(content_parts) if content_parts else "*[No text response]*"

def convert_chat_to_markdown(json_file, output_file):
    """Convert GitHub Copilot chat JSON to markdown."""
    
    print(f"Loading JSON from {json_file}...")
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"Processing {len(data.get('requests', []))} conversation exchanges...")
    
    # Start markdown content
    md_content = []
    md_content.append("# GitHub Copilot Chat History")
    md_content.append(f"\n**Exported**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    md_content.append(f"**Total Exchanges**: {len(data.get('requests', []))}")
    md_content.append("\n---\n")
    
    # Process each request/response pair
    for idx, request in enumerate(data.get('requests', []), 1):
        # User message
        message = request.get('message', {})
        user_text = message.get('text', '')
        
        if not user_text and 'parts' in message:
            user_text = extract_text_from_parts(message.get('parts', []))
        
        md_content.append(f"## Exchange {idx}")
        md_content.append(f"\n### 👤 User")
        md_content.append(f"\n{user_text}")
        
        # Assistant response
        response_items = request.get('response', [])
        response_text = format_response_content(response_items)
        
        md_content.append(f"\n### 🤖 GitHub Copilot")
        md_content.append(f"\n{response_text}")
        md_content.append("\n---\n")
    
    # Write markdown file
    print(f"Writing markdown to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(md_content))
    
    print(f"✅ Conversion complete! Created {output_file}")
    print(f"   Converted {len(data.get('requests', []))} conversation exchanges")

if __name__ == "__main__":
    input_file = Path(__file__).parent / "alarmreportingchat.json"
    output_file = Path(__file__).parent / "alarmreportingchat.md"
    
    if not input_file.exists():
        print(f"❌ Error: {input_file} not found")
        sys.exit(1)
    
    convert_chat_to_markdown(input_file, output_file)
