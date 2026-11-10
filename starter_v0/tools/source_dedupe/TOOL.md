---
name: source_dedupe
track: bonus
kind: local_formatter
requires_env: []
inputs: [items]
outputs: [items, removed_count]
side_effect: false
---
# source_dedupe

Removes duplicate research items by URL while preserving the first occurrence.
It only processes items already retrieved by another research tool.
