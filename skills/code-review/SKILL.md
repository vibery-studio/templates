---
name: code-review
description: Use when receiving code review feedback, completing tasks requiring review before proceeding, or before making completion claims. Covers receiving feedback with technical rigor, requesting reviews via code-reviewer subagent, and verification gates requiring evidence.
license: MIT
---

# Code Review Skill

Three core practices for rigorous code review ensuring quality and preventing false completion claims.

## Core Practices

### 1. Receiving Feedback

**Principle:** Technical correctness over social comfort.

**Protocol:** READ → UNDERSTAND → VERIFY → EVALUATE → RESPOND → IMPLEMENT

**Avoid:**
- "You're absolutely right!"
- Performative agreement

**Instead:**
- Restate requirements
- Ask clarifying questions
- Provide technical pushback when warranted

### 2. Requesting Reviews

**When to trigger:**
- After each task in subagent-driven development
- Before major merges

**Process:**
1. Obtain git SHAs for changes
2. Dispatch code-reviewer subagent with:
   - Implementation details
   - Requirements
   - Commit references
3. Act on feedback by priority:
   - Critical: Fix immediately
   - Important: Fix before proceeding

### 3. Verification Gates

**Iron Law:** NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE

**Process:**
1. IDENTIFY what needs verification
2. RUN the command
3. READ output
4. VERIFY it confirms the claim

## Key Principles

- Verification precedes claims (never skip)
- Evidence-based language only (eliminate "should," "probably," "seems")
- Technical rigor over comfort
- YAGNI principle (verify actual usage before implementing suggestions)

## Anti-Patterns

- Claiming completion without running tests
- Assuming code works without verification
- Implementing suggestions without evaluating necessity
- Skipping review for "small" changes

## Credits

Source: https://github.com/mrgoonie/claudekit-skills
