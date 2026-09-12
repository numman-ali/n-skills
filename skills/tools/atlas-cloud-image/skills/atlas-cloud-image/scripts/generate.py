#!/usr/bin/env python3
"""Discover Atlas Cloud image models and submit one image generation job."""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


DEFAULT_BASE_URL = "https://api.atlascloud.ai"


class AtlasError(RuntimeError):
    def __init__(self, message: str, *, retryable: bool = False) -> None:
        super().__init__(message)
        self.retryable = retryable


def request_json(
    method: str,
    url: str,
    *,
    api_key: str | None = None,
    payload: dict[str, Any] | None = None,
    timeout: float = 30,
) -> dict[str, Any]:
    headers = {
        "Accept": "application/json",
        "User-Agent": "atlas-cloud-image-skill/1.0",
    }
    data = None
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    if payload is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(payload).encode("utf-8")

    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise AtlasError(
            f"Atlas HTTP {exc.code}: {detail}",
            retryable=exc.code == 429 or exc.code >= 500,
        ) from exc
    except urllib.error.URLError as exc:
        raise AtlasError(f"Atlas request failed: {exc.reason}", retryable=True) from exc

    try:
        result = json.loads(body)
    except json.JSONDecodeError as exc:
        raise AtlasError("Atlas returned invalid JSON") from exc
    if not isinstance(result, dict):
        raise AtlasError("Atlas returned an unexpected response shape")
    return result


def unwrap(payload: dict[str, Any]) -> dict[str, Any]:
    code = payload.get("code")
    if code is not None and str(code) not in {"0", "200"}:
        raise AtlasError(str(payload.get("message") or f"Atlas API error {code}"))
    data = payload.get("data", payload)
    if not isinstance(data, dict):
        raise AtlasError("Atlas response data is not an object")
    return data


def fetch_models(base_url: str) -> list[dict[str, Any]]:
    payload = request_json("GET", f"{base_url}/api/v1/models")
    code = payload.get("code")
    if code is not None and str(code) not in {"0", "200"}:
        raise AtlasError(str(payload.get("message") or f"Atlas API error {code}"))
    models = payload.get("data")
    if not isinstance(models, list):
        raise AtlasError("Atlas model catalog is not a list")
    return [model for model in models if isinstance(model, dict)]


def visible_image_models(models: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        model
        for model in models
        if (model.get("display_console") is True or model.get("displayConsole") is True)
        and str(model.get("type", "")).lower() == "image"
    ]


def find_model(models: list[dict[str, Any]], model_id: str) -> dict[str, Any]:
    for model in visible_image_models(models):
        if model.get("model") == model_id:
            return model
    raise AtlasError(f"Model is not a visible Atlas image model: {model_id}")


def fetch_input_schema(model: dict[str, Any]) -> dict[str, Any]:
    schema_url = model.get("schema")
    if not isinstance(schema_url, str) or not schema_url.startswith("https://"):
        raise AtlasError("Selected model does not expose an HTTPS schema URL")
    document = request_json("GET", schema_url)
    try:
        schema = document["components"]["schemas"]["Input"]
    except (KeyError, TypeError) as exc:
        raise AtlasError("Selected model schema has no components.schemas.Input") from exc
    if not isinstance(schema, dict):
        raise AtlasError("Selected model input schema is invalid")
    return schema


def build_payload(args: argparse.Namespace, schema: dict[str, Any]) -> dict[str, Any]:
    properties = schema.get("properties", {})
    if not isinstance(properties, dict) or "prompt" not in properties:
        raise AtlasError("Selected model schema does not support prompt")

    payload: dict[str, Any] = {"model": args.model, "prompt": args.prompt}
    for name, value in {
        "size": args.size,
        "quality": args.quality,
        "output_format": args.output_format,
    }.items():
        if value is None:
            continue
        if name not in properties:
            raise AtlasError(f"Selected model schema does not support {name}")
        allowed = properties[name].get("enum")
        if isinstance(allowed, list) and value not in allowed:
            raise AtlasError(f"Invalid {name}: {value}. Allowed: {', '.join(map(str, allowed))}")
        payload[name] = value
    if "enable_sync_mode" in properties:
        payload["enable_sync_mode"] = False
    if "enable_base64_output" in properties:
        payload["enable_base64_output"] = False
    return payload


def submit_generation(base_url: str, api_key: str, payload: dict[str, Any]) -> dict[str, Any]:
    # Intentionally one POST only. A failed submission is never retried automatically.
    return unwrap(
        request_json(
            "POST",
            f"{base_url}/api/v1/model/generateImage",
            api_key=api_key,
            payload=payload,
            timeout=60,
        )
    )


def poll_generation(
    base_url: str,
    api_key: str,
    prediction_id: str,
    *,
    attempts: int,
    interval: float,
) -> dict[str, Any]:
    for attempt in range(attempts):
        try:
            prediction = unwrap(
                request_json(
                    "GET",
                    f"{base_url}/api/v1/model/result/{prediction_id}",
                    api_key=api_key,
                )
            )
        except AtlasError as exc:
            if not exc.retryable or attempt + 1 >= attempts:
                raise
            time.sleep(min(interval * (2**attempt), 8))
            continue

        status = str(prediction.get("status", "")).lower()
        if status in {"completed", "succeeded"}:
            return prediction
        if status in {"failed", "canceled", "cancelled"}:
            raise AtlasError(str(prediction.get("error") or f"Prediction {status}"))
        if attempt + 1 < attempts:
            time.sleep(interval)
    raise AtlasError(f"Prediction did not complete after {attempts} polls")


def extract_output_url(prediction: dict[str, Any]) -> str:
    outputs = prediction.get("outputs")
    if isinstance(outputs, list) and outputs and isinstance(outputs[0], str):
        return outputs[0]
    output = prediction.get("output")
    if isinstance(output, str):
        return output
    raise AtlasError("Completed prediction has no output URL")


def download(url: str, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    try:
        with urllib.request.urlopen(url, timeout=60) as response:
            output.write_bytes(response.read())
    except urllib.error.URLError as exc:
        raise AtlasError(f"Could not download generated image: {exc.reason}") from exc


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--base-url",
        default=os.environ.get("ATLASCLOUD_BASE_URL", DEFAULT_BASE_URL),
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    list_parser = subparsers.add_parser("list", help="List current visible image models")
    list_parser.add_argument("--search", default="")

    generate = subparsers.add_parser("generate", help="Generate one image")
    generate.add_argument("--model", required=True)
    generate.add_argument("--prompt", required=True)
    generate.add_argument("--size")
    generate.add_argument("--quality")
    generate.add_argument("--output-format")
    generate.add_argument("--output", type=Path)
    generate.add_argument("--poll-attempts", type=int, default=100)
    generate.add_argument("--poll-interval", type=float, default=3)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    base_url = args.base_url.rstrip("/")
    try:
        models = fetch_models(base_url)
        if args.command == "list":
            query = args.search.lower()
            for model in visible_image_models(models):
                model_id = str(model.get("model", ""))
                display_name = str(model.get("displayName", ""))
                if not query or query in f"{model_id} {display_name}".lower():
                    print(f"{model_id}\t{display_name}")
            return 0

        if args.poll_attempts < 1 or args.poll_interval < 0:
            raise AtlasError("Polling limits must be positive")
        api_key = os.environ.get("ATLASCLOUD_API_KEY")
        if not api_key:
            raise AtlasError("ATLASCLOUD_API_KEY is required for generation")

        model = find_model(models, args.model)
        payload = build_payload(args, fetch_input_schema(model))
        prediction = submit_generation(base_url, api_key, payload)
        if str(prediction.get("status", "")).lower() not in {"completed", "succeeded"}:
            prediction_id = prediction.get("id")
            if not isinstance(prediction_id, str) or not prediction_id:
                raise AtlasError("Generation response has no prediction ID")
            prediction = poll_generation(
                base_url,
                api_key,
                prediction_id,
                attempts=args.poll_attempts,
                interval=args.poll_interval,
            )

        output_url = extract_output_url(prediction)
        if args.output:
            download(output_url, args.output)
            print(args.output)
        else:
            print(output_url)
        return 0
    except AtlasError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
