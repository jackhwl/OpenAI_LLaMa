---
name: code-review
description: Performs a thorough code review covering complexity, security,
  and style. Use when the user asks for a review, asks to check this code,
  or mentions PR review.
allowed-tools: Read, Bash(python *), Grep
---

# Code Review

Perform a structured code review in three phases.

## Phase 1: Complexity
Run `python ~/.claude/skills/code-review/scripts/complexity_check.py <file>`
and report any functions flagged as overly long.

## Phase 2: Security
Read references/security_checklist.md and check each item against the target file.

## Phase 3: Style
Check naming conventions, comment quality, and consistency.

## Output Format
Use three sections: Complexity Issues / Security Issues / Style Notes.
Be specific — line numbers and suggested fixes where possible.