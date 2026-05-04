---
name: deploy
description: Deploy the API to a target environment. Manual-only — never auto-invoked.
argument-hint: "<env> — staging | production"
disable-model-invocation: true
allowed-tools: Bash, Read
---

# Deploy

Tags a release and triggers the deployment workflow. Manual-only because it has irreversible side effects.

## Steps

1. Validate `$ARGUMENTS` is exactly `staging` or `production`. Reject anything else.
2. Confirm the working tree is clean (`git status --porcelain` empty). Reject if not.
3. For `production`: require we're on `main`. For `staging`: any branch is OK.
4. For `production`: show the diff between the latest tag and HEAD, require an explicit "yes, deploy" from the user.
5. Tag: `v$(date +%Y.%m.%d-%H%M)-<env>` and push the tag.
6. Trigger the deploy workflow: `gh workflow run deploy.yml -f env=<env>`.
7. Tail the workflow run until it finishes or fails.
8. Print the deployed URL and the commit SHA.

## Why `disable-model-invocation: true`

Deploys are irreversible. We never want Claude to fire this on its own based on a description match. The user types `/deploy staging` deliberately or it doesn't happen.
