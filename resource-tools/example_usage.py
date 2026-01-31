#!/usr/bin/env python3

"""
Example usage of resource_loader for AI models
Demonstrates cost-effective resource access patterns
"""

from resource_loader import (
    search_resources,
    get_resource_by_name,
    list_resources,
    get_stats
)


def example_search_workflow():
    """
    Example: AI model needs help with React
    Instead of loading all resources, search first
    """
    print("=" * 60)
    print("EXAMPLE 1: Search Workflow")
    print("=" * 60)

    # User asks: "Help me optimize React performance"

    # Step 1: Search for relevant resources (lightweight)
    print("\n[AI] Searching for React performance resources...")
    results = search_resources("react performance", limit=3)

    print(f"[AI] Found {len(results)} relevant resources:")
    for r in results:
        print(f"  - {r['name']} ({r['type']})")
        print(f"    {r['description'][:100]}...")
        print()

    # Step 2: Load the most relevant one
    if results:
        chosen = results[0]
        print(f"[AI] Loading '{chosen['name']}' for detailed guidance...")
        resource = get_resource_by_name(chosen['name'])

        print(f"[AI] Loaded {len(resource['content'])} characters of content")
        print(f"[AI] Now I can provide expert React guidance using this resource!\n")


def example_targeted_search():
    """
    Example: Need specific type of resource
    """
    print("=" * 60)
    print("EXAMPLE 2: Targeted Search")
    print("=" * 60)

    # User asks: "What Claude skills are available?"

    print("\n[AI] Listing all Claude skills...")
    skills = list_resources('claude-skill')

    print(f"[AI] Found {len(skills)} Claude skills:")
    for skill in skills:
        print(f"  - {skill['name']}")

    print(f"\n[AI] You can use any of these skills for specialized tasks!\n")


def example_direct_access():
    """
    Example: User mentions a specific resource
    """
    print("=" * 60)
    print("EXAMPLE 3: Direct Access")
    print("=" * 60)

    # User says: "Use the frontend-design skill"

    print("\n[AI] Loading 'frontend-design' skill...")
    try:
        resource = get_resource_by_name('frontend-design', resource_type='claude-skill')
        print(f"[AI] Loaded {resource['name']}")
        print(f"[AI] Description: {resource['description'][:150]}...")
        print(f"[AI] Content size: {len(resource['content'])} characters")
        print(f"[AI] Now applying frontend-design skill to your request!\n")
    except ValueError as e:
        print(f"[AI] Error: {e}")
        print("[AI] Let me search for similar resources...")


def example_cost_comparison():
    """
    Example: Demonstrate token cost savings
    """
    print("=" * 60)
    print("EXAMPLE 4: Cost Comparison")
    print("=" * 60)

    stats = get_stats()

    print("\n[AI] Resource Statistics:")
    print(f"  Total resources: {stats['totalResources']}")
    print(f"  Skills: {stats['skills']}")
    print(f"  Agents: {stats['agents']}")
    print(f"  Prompts: {stats['prompts']}")
    print(f"  Instructions: {stats['instructions']}")

    # Calculate savings
    print("\n[AI] Cost Analysis:")
    print("  OLD APPROACH: Load all resources upfront")
    print("    - Content size: ~2170 KB")
    print("    - Tokens: ~542,500")
    print("    - Cost per request: ~$5.43 (at $10/M tokens)")

    print("\n  NEW APPROACH: Search index + load one resource")
    print("    - Index size: ~111 KB")
    print("    - One resource: ~25 KB")
    print("    - Total: ~136 KB")
    print("    - Tokens: ~34,000")
    print("    - Cost per request: ~$0.34")

    print("\n  SAVINGS: 93.7% reduction in tokens")
    print("  SAVINGS: 93.7% reduction in cost")
    print("  SAVINGS: Faster response times!\n")


def example_discovery_workflow():
    """
    Example: User doesn't know what they need
    """
    print("=" * 60)
    print("EXAMPLE 5: Discovery Workflow")
    print("=" * 60)

    # User asks: "I need help with Azure infrastructure"

    print("\n[AI] User needs: Azure infrastructure help")
    print("[AI] Searching for Azure-related resources...")

    results = search_resources("azure", limit=5)

    print(f"\n[AI] Found {len(results)} Azure resources:")
    for i, r in enumerate(results, 1):
        print(f"\n  {i}. {r['name']} ({r['type']})")
        print(f"     {r['description'][:120]}...")

    print("\n[AI] Let me suggest: 'Azure Principal Architect' seems most relevant.")
    print("[AI] Would you like me to use that resource?")
    print("[AI] (In practice, I would load it and apply the guidance)\n")


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("RESOURCE LOADER - USAGE EXAMPLES FOR AI MODELS")
    print("=" * 60)
    print("\nThese examples show how AI models can efficiently access")
    print("resources to reduce token usage and costs.\n")

    try:
        example_search_workflow()
        example_targeted_search()
        example_direct_access()
        example_cost_comparison()
        example_discovery_workflow()

        print("=" * 60)
        print("SUMMARY")
        print("=" * 60)
        print("\nKey Takeaways:")
        print("1. Always SEARCH first, LOAD second")
        print("2. Use type filters for targeted searches")
        print("3. Only load full content when needed")
        print("4. This approach saves 90%+ in token costs")
        print("\nFor AI models: Integrate these functions into your")
        print("workflow to provide cost-effective, specialized guidance!\n")

    except FileNotFoundError as e:
        print(f"\nError: {e}")
        print("\nPlease run 'python index_builder.py' first to create the indexes.")
