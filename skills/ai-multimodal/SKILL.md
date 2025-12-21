---
name: ai-multimodal
description: Process and generate multimedia content using Google Gemini API. Analyze audio (9.5 hours), understand images, process videos (6 hours), extract from documents, generate images. Use when working with audio/video files, analyzing images, processing PDFs, or implementing multimodal AI features.
license: MIT
---

# AI Multimodal Processing

Process and generate multimedia content using Google Gemini API with context windows up to 2M tokens.

## Core Capabilities

| Capability | Max Size | Use Cases |
|-----------|----------|-----------|
| Audio | 9.5 hours | Transcription, summarization, speech analysis |
| Images | Multiple | Captioning, OCR, object detection, visual Q&A |
| Video | 6 hours | Scene detection, Q&A, temporal analysis, YouTube |
| Documents | 1,000 pages | PDF tables, forms, charts, diagrams |
| Image Gen | - | Text-to-image, editing, composition |

## Model Selection

**Recommended:**
- `gemini-2.5-flash` - Fast, cost-effective
- `gemini-2.5-pro` - Complex reasoning

## Quick Start

```bash
# Set API key
export GOOGLE_API_KEY="your-api-key"

# Install SDK
pip install google-generativeai
```

## Common Usage Patterns

### Image Analysis
```python
import google.generativeai as genai
model = genai.GenerativeModel('gemini-2.5-flash')
response = model.generate_content([image, "Describe this image"])
```

### Audio Transcription
```python
response = model.generate_content([audio_file, "Transcribe with timestamps"])
```

### Video Analysis
```python
response = model.generate_content([video_file, "Summarize key scenes"])
```

## Supported Formats

- **Audio:** WAV, MP3, FLAC, AAC, OGG
- **Images:** PNG, JPEG, GIF, WebP
- **Video:** MP4, MOV, AVI, MKV
- **Documents:** PDF

## Cost Optimization

- Use `gemini-2.5-flash` for routine tasks
- Batch similar requests
- Cache results where possible
- Request only needed data

## Resources

- API Docs: https://ai.google.dev/docs
- Get API Key: https://aistudio.google.com/apikey

## Credits

Source: https://github.com/mrgoonie/claudekit-skills
