import json
import tempfile
from pathlib import Path

from gopro_overlay.config import Config
from gopro_overlay.ffmpeg_profile import load_ffmpeg_profile

simple = {
    "simple": {
        "input": ["i1", "i2"],
        "output": ["o1", "o2"]
    },
    "filter": {
        "input": ["a"],
        "output": ["b"],
        "filter": "c"
    }
}


class TestProfiles:
    
    def test_loading_a_profile(self):
        with tempfile.TemporaryDirectory() as tempdir:
            config = Path(tempdir) / "ffmpeg-profiles.json"
            config.write_text(json.dumps(simple))

            loader = Config(Path(tempdir))
            profile = load_ffmpeg_profile(loader, "simple")

            assert profile.input == ["i1", "i2"]
            assert profile.output == ["o1", "o2"]

            profile_2 = load_ffmpeg_profile(loader, "filter")
            assert profile_2.filter_complex == "c"

    def test_loading_builtin_profile(self):
        loader = Config(Path("/tmp/nonexistent"))
        profile = load_ffmpeg_profile(loader, "nnvgpu-60fps")

        assert profile.input == ["-hwaccel", "cuda", "-hwaccel_output_format", "cuda"]
        assert profile.output == [
            "-vcodec", "h264_nvenc",
            "-rc:v", "cbr",
            "-b:v", "25M",
            "-bf:v", "3",
            "-profile:v", "main",
            "-spatial-aq", "true",
            "-movflags", "faststart",
            "-r", "60"
        ]
        assert profile.filter_complex == "[0:v]scale_cuda=format=yuv420p[mp4_stream];[1:v]format=yuva420p,hwupload[overlay_stream];[mp4_stream][overlay_stream]overlay_cuda"
