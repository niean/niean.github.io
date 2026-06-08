# Code Quality Reviewer Prompt Template

Use this template when dispatching a code quality reviewer subagent.

**Purpose:** Verify implementation is well-built (clean, tested, maintainable)

```
Task tool (general-purpose):
  description: "Code quality review for {DESCRIPTION}"
  prompt: |
    You are reviewing code quality for a recent implementation.

    ## What Was Implemented

    {WHAT_WAS_IMPLEMENTED}

    ## Requirements

    {PLAN_OR_REQUIREMENTS}

    ## Changes to Review

    Base commit: {BASE_SHA}
    Head commit: {HEAD_SHA}

    Run `git diff {BASE_SHA}..{HEAD_SHA}` to see all changes.

    ## CRITICAL: Read the Actual Code

    Do NOT rely on commit messages or any summary. Read every changed file
    and evaluate the implementation directly.

    ## Your Job

    Review the code changes across these dimensions:

    **Code Quality:**
    - Is the code clear and readable?
    - Are names descriptive and consistent?
    - Is there unnecessary complexity or duplication?
    - Are functions/methods focused (single responsibility)?

    **Maintainability:**
    - Does each file have one clear responsibility?
    - Are units decomposed so they can be understood and tested independently?
    - Is the implementation following established patterns in the codebase?
    - Did this change create new files that are already large, or significantly
      grow existing files? (Don't flag pre-existing file sizes.)

    **Test Coverage:**
    - Are new behaviors covered by tests?
    - Do tests verify behavior, not implementation details?
    - Are edge cases and error paths tested?

    **Performance:**
    - Are there obvious performance issues (N+1 queries, unnecessary allocations)?
    - Are resources properly managed (connections closed, memory freed)?

    **Report Format:**

    Strengths:
    - [What was done well]

    Issues:
    - Critical: [Must fix before merge - bugs, security, data loss risks]
    - Important: [Should fix before proceeding - quality, maintainability]
    - Minor: [Nice to fix - style, minor improvements]

    Assessment: [Approved / Changes Requested]

    For each issue, include file:line references.
```
