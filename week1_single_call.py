"""Week 1: make one observable Chat Completions API request."""

import json
import os

import requests

API_URL = "https://integrate.api.nvidia.com/v1/chat/completions"
MODEL = "minimaxai/minimax-m3.1-flash"
QUESTION = "用一句話說明什麼是 HTTP"


def call_model(messages):
    """Send one request and display its HTTP status and result."""
    api_key = os.environ["NVIDIA_API_KEY"]
    response = requests.post(
        API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": MODEL,
            "messages": messages,
            "max_tokens": 512,
            "temperature": 1,
            "top_p": 0.95,
        },
        timeout=60,
    )

    print("status:", response.status_code)
    data = response.json()
    print(json.dumps(data, ensure_ascii=False, indent=2))

    if response.ok:
        print("reply:", data["choices"][0]["message"]["content"])
    else:
        print("error:", data.get("error", data))

    return data


if __name__ == "__main__":
    try:
        call_model([{"role": "user", "content": QUESTION}])
    except KeyError as error:
        if error.args == ("NVIDIA_API_KEY",):
            raise SystemExit(
                "Please set NVIDIA_API_KEY before running."
            ) from None
        raise SystemExit("Unexpected API response structure.") from None
    except requests.exceptions.Timeout:
        raise SystemExit("API request timed out after 60 seconds.") from None
    except requests.exceptions.RequestException as error:
        raise SystemExit(
            f"API request failed: {type(error).__name__}"
        ) from None
    except (ValueError, IndexError, TypeError):
        raise SystemExit("Unexpected API response structure.") from None
