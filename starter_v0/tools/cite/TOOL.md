---
name: cite
track: core
kind: local_formatter
provider:
requires_env: []
inputs: [sources, style]
outputs: [markdown, citations, citation_count]
side_effect: false
---
# cite

Formats a list of sources (`title`, `url`) into a numbered citation block.
Local only — does not fetch the web. Use after research tools when the user
asks for citations / bibliography / nguồn trích dẫn.
