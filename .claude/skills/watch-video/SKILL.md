---
name: watch-video
description: Transcribe, inspect, and summarize videos on Windows using PowerShell. Use for YouTube, Loom, Vimeo, Riverside, Zoom recordings, social-video URLs supported by yt-dlp, and local MP4/MOV/WebM/MKV files. Supports transcript, visual, and multimodal depth modes; uses platform captions first, faster-whisper locally when needed, FFmpeg frame extraction for visual analysis, and an available native-video provider only when explicitly configured.
---

# Watch video on Windows

Transcribe or analyze a video from PowerShell without assuming Bash, Homebrew,
MLX, macOS paths, Claude-specific tools, or a configured cloud provider.

Adapted for Windows from Corey Haines's `makerskills/watch-video` v0.2.2.

## 1. Parse the request

Accept:

- YouTube URLs, Shorts URLs, `youtu.be` links, or raw video IDs
- Loom, Vimeo, Riverside, X, Instagram, or TikTok URLs supported by `yt-dlp`
- Local `.mp4`, `.mov`, `.webm`, or `.mkv` files

Choose one depth:

| Request | Mode | Result |
|---|---|---|
| `watch-video <source>` | transcript | Transcript, metadata, and a brief report |
| `watch-video <source> transcript` | transcript | Same as the default |
| `watch-video <source> visual` | visual | Transcript plus sampled frames and key moments |
| `watch-video <source> multimodal` | multimodal | Native-video analysis when a provider is configured; otherwise dense frames |

If the user omits depth for a video longer than 10 minutes, use transcript
mode unless visual content is essential. Ask before a paid visual or
multimodal provider call. Never upload a local/private recording without the
user's approval.

## 2. Check Windows prerequisites

Run read-only checks first:

```powershell
Get-Command yt-dlp, ffmpeg, ffprobe, python, py, winget -ErrorAction SilentlyContinue |
    Select-Object Name, Source
```

Install only with the user's approval when a dependency is missing:

```powershell
winget install --id yt-dlp.yt-dlp --exact
winget install --id Gyan.FFmpeg --exact
python -m pip install --upgrade faster-whisper
```

Restart the terminal after `winget` installation if PATH has not refreshed.
`faster-whisper` downloads its selected model on first use and may require
several GB of disk space.

If `faster-whisper` does not support the machine's newest Python version,
install Python 3.12 side by side and use it for the helper:

```powershell
winget install --id Python.Python.3.12 --exact
py -3.12 -m pip install --upgrade faster-whisper
```

## 3. Create a Windows work directory

Use the actual Documents known folder, sanitize the title, and preserve the
path in variables rather than rebuilding command strings:

```powershell
$skillDir = Split-Path -Parent '<resolved absolute path to this SKILL.md>'
$documents = [Environment]::GetFolderPath('MyDocuments')
$videoRoot = Join-Path $documents 'videos'
$sourceKind = 'youtube'  # loom, vimeo, riverside, zoom, social, or local
$title = 'replace with discovered title'
$slug = (($title.ToLowerInvariant() -replace '[^a-z0-9]+', '-').Trim('-'))
if ($slug.Length -gt 50) { $slug = $slug.Substring(0, 50).Trim('-') }
$date = Get-Date -Format 'yyyy-MM-dd'
$workDir = Join-Path $videoRoot "$sourceKind-$slug-$date"
New-Item -ItemType Directory -Path $workDir -Force | Out-Null
```

Use `-LiteralPath` for local input files. Keep URL and path values in separate
variables. Do not interpolate untrusted values into `Invoke-Expression`.

## 4. Capture metadata

For a URL:

```powershell
$sourceUrl = '<url>'
& yt-dlp --dump-single-json --skip-download --no-warnings $sourceUrl |
    Set-Content -LiteralPath (Join-Path $workDir 'metadata.json') -Encoding utf8
```

Read the JSON to obtain title, uploader, duration, upload date, description,
and chapters. For a local file:

```powershell
$videoPath = 'C:\path\recording.mp4'
& ffprobe -v error -show_entries format=filename,duration,format_name,size `
    -of json $videoPath |
    Set-Content -LiteralPath (Join-Path $workDir 'metadata.json') -Encoding utf8
```

## 5. Obtain the transcript

Use these backends in order.

### A. Platform captions

Try provided and automatic English captions before downloading video or
running local speech recognition:

```powershell
& yt-dlp --skip-download --write-subs --write-auto-subs `
    --sub-langs 'en.*,en' --sub-format vtt `
    -o (Join-Path $workDir 'source.%(ext)s') $sourceUrl
$vtt = Get-ChildItem -LiteralPath $workDir -Filter '*.vtt' |
    Sort-Object Length -Descending | Select-Object -First 1
```

If a complete VTT exists, clean it with the bundled script:

```powershell
& (Join-Path $skillDir 'scripts\clean-vtt.ps1') `
    -InputPath $vtt.FullName `
    -OutputPath (Join-Path $workDir 'transcript.txt')
```

Set `$skillDir` from the actual skill location loaded by the agent; do not
assume the current working directory is the skill directory.

### B. Local faster-whisper

If captions are absent or clearly incomplete, download a 720p-or-smaller MP4
for URL sources:

```powershell
& yt-dlp -f 'bv*[height<=720]+ba/b[height<=720]' `
    --merge-output-format mp4 `
    -o (Join-Path $workDir 'video.%(ext)s') $sourceUrl
$videoPath = (Get-ChildItem -LiteralPath $workDir -Filter 'video.*' |
    Select-Object -First 1).FullName
```

Then run the bundled cross-platform Python helper:

```powershell
python (Join-Path $skillDir 'scripts\transcribe-faster-whisper.py') `
    $videoPath --output-dir $workDir --model large-v3-turbo
```

The helper writes `transcript.txt` and `transcript-raw.json`, selects CUDA when
available, and otherwise uses CPU/int8. Use `small` or `medium` on systems
where the large model is too slow or memory constrained. Substitute
`py -3.12` for `python` when using the side-by-side Python installation.

### C. Last-resort transcript

If neither captions nor local transcription is available, stop and report the
missing dependency. Do not invent a transcript from metadata or sparse frames.

## 6. Finish transcript mode

Verify that `transcript.txt` is nonempty. Report title, source, duration, word
count, and the work-directory path. Provide a concise summary only when the
user requested one; preserve the complete transcript as an artifact.

## 7. Visual mode

Ensure a local video exists, then select cadence by content:

| Content | Cadence |
|---|---|
| Screen share, Loom, or UI demo | every 5 seconds |
| Slide presentation | every 10 seconds plus scene changes |
| General/unknown | every 15 seconds |
| Talking head or podcast | every 30 seconds |

Extract interval frames:

```powershell
$framesDir = Join-Path $workDir 'frames'
New-Item -ItemType Directory -Path $framesDir -Force | Out-Null
& ffmpeg -i $videoPath -vf 'fps=1/15' `
    (Join-Path $framesDir 'frame-%04d.png') -y
```

For slides, add scene-change frames:

```powershell
& ffmpeg -i $videoPath -vf "select='gt(scene,0.3)',showinfo" `
    -fps_mode vfr (Join-Path $framesDir 'scene-%04d.png') -y `
    2> (Join-Path $workDir 'scene-detection.log')
```

Inspect frames in timestamp order with the agent's available image-viewing
tool. Pair each frame with the corresponding transcript window. Batch no more
than about ten frames at once. Record `moments.md` entries with timestamp,
on-screen content, nearby transcript, UI/slide changes, decisions, and notable
actions. Do not claim details that are unreadable in the frame.

Create `summary.md` with:

- TL;DR
- key moments with timestamps
- action items
- decisions
- short noteworthy quotations
- open questions

Respect source quotation limits and do not reproduce copyrighted material
beyond what the user needs.

## 8. Multimodal mode

Prefer a native-video provider only when its CLI/API is actually available,
credentials are configured, and the user approves uploading the video and any
material cost. Do not assume a Gemini, Claude, or OpenAI video API exists from
an environment-variable name alone. Verify current provider documentation
before forming requests.

If no approved native-video provider is available, use dense visual fallback:

```powershell
& ffmpeg -i $videoPath -vf 'fps=1/3' `
    (Join-Path $framesDir 'dense-%05d.png') -y
```

Warn before dense analysis of videos longer than 10 minutes. Process frames in
batches and produce the visual-mode summary plus body language/delivery,
pacing, visual style, and audio-atmosphere observations when supported by the
evidence. Never infer speaker identity from appearance alone.

## 9. Optional knowledge capture

Offer to copy the summary into a user-designated knowledge base only after the
analysis completes. Ask for the destination if it is not configured. Do not
assume `second-brain` or another companion skill exists.

## 10. Report

Return:

- source, title, duration, mode, and word count
- clickable paths to `transcript.txt`, `metadata.json`, and any visual outputs
- top key moments for visual/multimodal modes
- action items or decisions requiring follow-up
- limitations, missing captions, degraded frames, or transcription confidence

## Failure handling

| Failure | Response |
|---|---|
| Private, removed, or region-locked URL | Report and stop; do not bypass access controls |
| `yt-dlp` missing | Offer the exact `winget` command |
| FFmpeg/ffprobe missing | Offer the exact `winget` command |
| Captions absent | Use faster-whisper if installed and approved |
| CUDA unavailable | Use CPU/int8 and warn that long videos may be slow |
| Output path contains spaces | Pass paths as argument values; never concatenate a command string |
| Visual frames are unclear | Reduce cadence, add scene detection, or report uncertainty |
| Cloud upload not approved | Use local transcript/frames only |
| Paid mode requested for a long video | State likely cost/latency and ask before proceeding |

## Quality rules

- Prefer platform captions, then local transcription, then explicitly approved
  cloud processing.
- Keep downloads at 720p unless the user needs small on-screen text.
- Use transcript timestamps to guide frame inspection.
- Treat private recordings and API keys as sensitive; never commit them.
- Preserve uncertainty and distinguish transcript evidence from visual
  inference.
