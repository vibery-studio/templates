---
name: sequential-thinking
description: Use when complex problems require systematic step-by-step reasoning with ability to revise thoughts, branch into alternative approaches, or dynamically adjust scope.
license: MIT
---

# Sequential Thinking

Structured problem-solving through iterative reasoning with dynamic scope adjustment.

## When to Use

- Complex problems requiring systematic analysis
- Multi-step reasoning with potential revisions
- Exploring alternative approaches
- Problems where scope may change during analysis

## Core Capabilities

1. Break complex problems into sequential thought steps
2. Adjust scope dynamically
3. Track revisions to previous thoughts
4. Explore alternative reasoning paths
5. Maintain full context throughout analysis

## Implementation Pattern

### Basic Workflow

```
Thought 1: Initial analysis of problem
→ nextThoughtNeeded: true
→ estimatedSteps: 5

Thought 2: Deeper exploration
→ nextThoughtNeeded: true
→ estimatedSteps: 4 (refined)

...

Thought N: Conclusion reached
→ nextThoughtNeeded: false
```

### Revision Pattern

```
Thought 3: Revising assumption from Thought 1
→ isRevision: true
→ revisesThought: 1
```

### Branching Pattern

```
Thought 4: Exploring alternative approach
→ branchFromThought: 2
→ branchId: "alternative-A"
```

## Key Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| thought | Yes | Current reasoning step |
| nextThoughtNeeded | Yes | Continue reasoning? |
| thoughtNumber | Yes | Current step (starts at 1) |
| totalThoughts | Yes | Estimated total steps |
| isRevision | No | Reconsidering prior thought? |
| revisesThought | No | Which thought being revised |
| branchFromThought | No | Branch point |
| branchId | No | Branch identifier |

## Practical Guidance

1. Begin with rough estimates for total thoughts
2. Refine estimates as progress is made
3. Use revisions when assumptions prove incorrect
4. Branch when multiple viable approaches exist
5. Express uncertainty explicitly
6. Adjust scope freely as understanding develops

## Example

```
Problem: "Design a caching strategy for API responses"

Thought 1: Identify cache requirements (TTL, invalidation, size)
Thought 2: Evaluate caching layers (CDN, Redis, in-memory)
Thought 3: [Revision] Reconsider TTL based on data volatility
Thought 4: Design invalidation strategy
Thought 5: Implement monitoring and fallback
```

## Credits

Source: https://github.com/mrgoonie/claudekit-skills
