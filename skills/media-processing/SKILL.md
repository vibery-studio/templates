---
name: media-processing
description: Process multimedia files with FFmpeg (video/audio encoding, conversion, streaming, filtering, hardware acceleration), ImageMagick (image manipulation, format conversion, batch processing, effects), and RMBG (AI-powered background removal). Use when converting media formats, encoding videos, or processing images.
license: MIT
---

# Media Processing

Process video, audio, and images using FFmpeg and ImageMagick command-line tools.

## Tool Selection

| Task | Tool |
|------|------|
| Video/audio encoding | FFmpeg |
| Video streaming (HLS/DASH) | FFmpeg |
| Image format conversion | ImageMagick |
| Image resizing/cropping | ImageMagick |
| Video frame extraction | FFmpeg |
| Batch image processing | ImageMagick |
| Background removal | RMBG |

## Installation

```bash
# macOS
brew install ffmpeg imagemagick

# Ubuntu/Debian
sudo apt install ffmpeg imagemagick
```

## FFmpeg Quick Start

### Video Conversion
```bash
ffmpeg -i input.mp4 -c:v libx264 -crf 23 output.mp4
```

### Audio Extraction
```bash
ffmpeg -i video.mp4 -vn -acodec libmp3lame audio.mp3
```

### HLS Streaming
```bash
ffmpeg -i input.mp4 -c:v libx264 -hls_time 10 -hls_list_size 0 output.m3u8
```

### Thumbnail Generation
```bash
ffmpeg -i video.mp4 -ss 00:00:05 -vframes 1 thumb.jpg
```

### Watermark
```bash
ffmpeg -i input.mp4 -i logo.png -filter_complex "overlay=10:10" output.mp4
```

## ImageMagick Quick Start

### Image Conversion
```bash
convert input.png output.jpg
```

### Resize Image
```bash
convert input.jpg -resize 800x600 output.jpg
```

### Batch Processing
```bash
mogrify -resize 50% *.jpg
```

### Composite Images
```bash
composite -gravity center overlay.png background.png result.png
```

### Create GIF
```bash
convert -delay 100 -loop 0 *.png animation.gif
```

## Advanced Techniques

### Multi-pass Video Encoding
```bash
ffmpeg -i input.mp4 -c:v libx264 -b:v 2M -pass 1 -f null /dev/null
ffmpeg -i input.mp4 -c:v libx264 -b:v 2M -pass 2 output.mp4
```

### GPU Acceleration (NVIDIA)
```bash
ffmpeg -hwaccel cuda -i input.mp4 -c:v h264_nvenc output.mp4
```

## Performance Tips

1. Use hardware acceleration when available
2. Choose appropriate codec for use case
3. Balance quality vs file size with CRF
4. Use multi-threading
5. Process in batches for large operations

## Credits

Source: https://github.com/mrgoonie/claudekit-skills
