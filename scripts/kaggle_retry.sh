#!/usr/bin/env bash
set -euo pipefail
max_attempts="${KAGGLE_RETRY_ATTEMPTS:-8}"
delay="${KAGGLE_RETRY_DELAY:-30}"
attempt=1
while true; do
  set +e
  output=$(kaggle "$@" 2>&1)
  status=$?
  set -e
  printf '%s\n' "$output"
  if [ "$status" -eq 0 ]; then
    exit 0
  fi
  if ! grep -qi 'Too Many Requests\|429' <<<"$output"; then
    exit "$status"
  fi
  if [ "$attempt" -ge "$max_attempts" ]; then
    exit "$status"
  fi
  sleep_for=$((delay * attempt))
  printf 'Kaggle API rate-limited; retrying in %ss (attempt %s/%s)\n' "$sleep_for" "$attempt" "$max_attempts" >&2
  sleep "$sleep_for"
  attempt=$((attempt + 1))
done
