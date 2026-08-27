---
name: atlas-cloud-image
description: Generate images through Atlas Cloud with live model and input-schema validation. Use when the user asks to create an image with Atlas Cloud or needs an optional API-based text-to-image provider.
license: Apache-2.0
compatibility: Python 3.10+ with network access
metadata:
  author: binyangzhu000-sudo
  version: "1.0.0"
---

# Atlas Cloud Image

Use Atlas Cloud as an optional image-generation provider. Keep an application's
existing provider and defaults unchanged unless the user explicitly requests a
switch.

## Setup

Set the API key in the environment. Never pass it as a command-line argument or
write it to project files.

```bash
export ATLASCLOUD_API_KEY="..."
```

## Discover a Model

Always query the live catalog before generation. The helper lists only visible
image models:

```bash
python3 {baseDir}/scripts/generate.py list --search image
```

Choose an exact model ID from that output. The helper then downloads the model's
current OpenAPI schema and rejects unsupported input fields or enum values.

## Generate

```bash
python3 {baseDir}/scripts/generate.py generate \
  --model "MODEL_ID_FROM_LIST" \
  --prompt "A clean product launch image with one focal point" \
  --size 1024x1024 \
  --output launch.png
```

Optional `--quality` and `--output-format` values must be supported by the live
schema. Without `--output`, the helper prints the generated media URL.

## Operational Rules

1. Fetch the live catalog and selected model schema for every generation.
2. Submit the billable generation POST exactly once; never retry it automatically.
3. Retry only transient prediction GET failures, within the configured poll limit.
4. Treat failed or canceled predictions as terminal.
5. Keep credentials in environment variables and out of logs and commits.
