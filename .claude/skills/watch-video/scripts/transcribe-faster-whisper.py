"""Transcribe a local media file with faster-whisper on Windows."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path


def register_cuda_dll_dirs() -> None:
    """Add pip-installed NVIDIA runtime lib dirs (cuBLAS/cuDNN/nvrtc) to the
    Windows DLL search path so CTranslate2 can load the GPU backend. Without
    this, `pip install nvidia-cublas-cu12 nvidia-cudnn-cu12` puts the DLLs in
    site-packages\\nvidia\\*\\bin where CTranslate2 can't find them, and a
    cuda run fails with "cublas64_12.dll is not found". No-op off Windows or
    when the wheels aren't installed."""
    if os.name != "nt" or not hasattr(os, "add_dll_directory"):
        return
    roots: list[str] = []
    try:
        import site

        roots.extend(site.getsitepackages())
        user = site.getusersitepackages()
        if user:
            roots.append(user)
    except Exception:
        pass
    roots.append(str(Path(sys.prefix) / "Lib" / "site-packages"))
    seen: set[str] = set()
    found: list[str] = []
    for root in roots:
        nvidia = Path(root) / "nvidia"
        if not nvidia.is_dir():
            continue
        for bin_dir in nvidia.glob("*/bin"):
            key = str(bin_dir).lower()
            if bin_dir.is_dir() and key not in seen:
                seen.add(key)
                found.append(str(bin_dir))
                try:
                    os.add_dll_directory(str(bin_dir))
                except OSError:
                    pass
    # CTranslate2 loads cuBLAS/cuDNN lazily via the process PATH, which
    # os.add_dll_directory alone does not cover for that load path, so prepend
    # the dirs to PATH too.
    if found:
        os.environ["PATH"] = os.pathsep.join(found + [os.environ.get("PATH", "")])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Local video or audio file")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--model", default="large-v3-turbo")
    parser.add_argument("--language", default=None)
    parser.add_argument("--device", choices=("auto", "cpu", "cuda"), default="auto")
    return parser.parse_args()


def select_runtime(requested_device: str) -> tuple[str, str]:
    if requested_device == "cpu":
        return "cpu", "int8"
    if requested_device == "cuda":
        return "cuda", "float16"
    try:
        import ctranslate2

        if ctranslate2.get_cuda_device_count() > 0:
            return "cuda", "float16"
    except (ImportError, RuntimeError):
        pass
    return "cpu", "int8"


def timestamp(seconds: float) -> str:
    milliseconds = round(max(0.0, seconds) * 1000)
    hours, remainder = divmod(milliseconds, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    secs, millis = divmod(remainder, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"


def main() -> int:
    args = parse_args()
    input_path = args.input.resolve(strict=True)
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    register_cuda_dll_dirs()

    try:
        from faster_whisper import WhisperModel
    except ImportError as exc:
        raise SystemExit(
            "faster-whisper is not installed; run: "
            "python -m pip install --upgrade faster-whisper"
        ) from exc

    device, compute_type = select_runtime(args.device)
    model = WhisperModel(args.model, device=device, compute_type=compute_type)
    segments_iter, info = model.transcribe(
        str(input_path),
        language=args.language,
        vad_filter=True,
        beam_size=5,
    )
    segments = [
        {
            "start": segment.start,
            "end": segment.end,
            "text": segment.text.strip(),
        }
        for segment in segments_iter
        if segment.text.strip()
    ]

    transcript_lines = [
        f"[{timestamp(segment['start'])}] {segment['text']}"
        for segment in segments
    ]
    (output_dir / "transcript.txt").write_text(
        "\n".join(transcript_lines) + ("\n" if transcript_lines else ""),
        encoding="utf-8",
    )
    payload = {
        "source": str(input_path),
        "model": args.model,
        "device": device,
        "compute_type": compute_type,
        "language": info.language,
        "language_probability": info.language_probability,
        "duration": info.duration,
        "segments": segments,
    }
    (output_dir / "transcript-raw.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(output_dir / "transcript.txt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
