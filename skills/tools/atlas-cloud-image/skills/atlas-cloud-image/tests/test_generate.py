from __future__ import annotations

import argparse
import importlib.util
import unittest
from pathlib import Path
from unittest.mock import patch


MODULE_PATH = Path(__file__).parents[1] / "scripts" / "generate.py"
SPEC = importlib.util.spec_from_file_location("atlas_generate", MODULE_PATH)
assert SPEC and SPEC.loader
atlas_generate = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(atlas_generate)


class GenerateTest(unittest.TestCase):
    def test_visible_image_models_excludes_hidden_and_video(self) -> None:
        models = [
            {"model": "visible", "type": "Image", "display_console": True},
            {"model": "hidden", "type": "Image", "display_console": False},
            {"model": "video", "type": "Video", "display_console": True},
        ]
        self.assertEqual(
            ["visible"],
            [model["model"] for model in atlas_generate.visible_image_models(models)],
        )

    def test_build_payload_uses_schema_supported_values(self) -> None:
        args = argparse.Namespace(
            model="provider/model",
            prompt="A launch image",
            size="1024x1024",
            quality="high",
            output_format="png",
        )
        schema = {
            "properties": {
                "prompt": {"type": "string"},
                "size": {"enum": ["1024x1024"]},
                "quality": {"enum": ["medium", "high"]},
                "output_format": {"enum": ["jpeg", "png"]},
                "enable_sync_mode": {"type": "boolean"},
            }
        }
        self.assertEqual(
            {
                "model": "provider/model",
                "prompt": "A launch image",
                "size": "1024x1024",
                "quality": "high",
                "output_format": "png",
                "enable_sync_mode": False,
            },
            atlas_generate.build_payload(args, schema),
        )

    def test_submit_generation_posts_once(self) -> None:
        with patch.object(
            atlas_generate,
            "request_json",
            return_value={"code": 200, "data": {"id": "prediction-1", "status": "starting"}},
        ) as request:
            result = atlas_generate.submit_generation(
                "https://example.test", "secret", {"prompt": "x"}
            )
        self.assertEqual("prediction-1", result["id"])
        self.assertEqual(1, request.call_count)
        self.assertEqual("POST", request.call_args.args[0])

    def test_polling_is_bounded(self) -> None:
        responses = [
            {"code": 200, "data": {"status": "processing"}},
            {"code": 200, "data": {"status": "completed", "outputs": ["https://cdn/image.png"]}},
        ]
        with (
            patch.object(atlas_generate, "request_json", side_effect=responses) as request,
            patch.object(atlas_generate.time, "sleep"),
        ):
            result = atlas_generate.poll_generation(
                "https://example.test", "secret", "prediction-1", attempts=3, interval=0
            )
        self.assertEqual("completed", result["status"])
        self.assertEqual(2, request.call_count)


if __name__ == "__main__":
    unittest.main()
