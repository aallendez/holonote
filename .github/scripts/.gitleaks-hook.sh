#!/bin/bash
if command -v gitleaks >/dev/null 2>&1; then
  gitleaks detect --source . --no-banner
elif command -v docker >/dev/null 2>&1; then
  docker run --rm -v "$(pwd):/path" -w /path zricethezav/gitleaks:latest detect --source /path --no-banner
else
  echo "Warning: gitleaks not found and docker not available. Skipping secret scan."
  exit 0
fi
