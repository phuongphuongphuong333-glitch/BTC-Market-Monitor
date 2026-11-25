import os
import sys
import requests

MODEL = "gemini-flash-latest"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"

def main() -> int:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY secret is missing.")
        return 2
    prompt = (
        "You are the analysis component of BTC Market Monitor. "
        "This is a connectivity test, not a market signal. "
        "Do not invent market data. Reply in Vietnamese with exactly: "
        "GEMINI_OK - Kết nối API thành công. Chưa phân tích thị trường."
    )
    try:
        response = requests.post(
            API_URL,
            headers={"Content-Type": "application/json", "X-goog-api-key": api_key},
            json={"contents": [{"parts": [{"text": prompt}]}]},
            timeout=30,
        )
        if response.status_code != 200:
            print(f"ERROR: Gemini API returned HTTP {response.status_code}.")
            try:
                error = response.json().get("error", {}).get("message", "")
                if error:
                    print(f"Gemini message: {error[:500]}")
            except ValueError:
                pass
            return 1
        data = response.json()
        parts = data.get("candidates", [{}])[0].get("content", {}).get("parts", [])
        answer = "\n".join(p.get("text", "") for p in parts if p.get("text")).strip()
        if not answer:
            print("ERROR: Gemini returned no text.")
            return 1
        print(answer[:900])
        return 0
    except requests.RequestException as exc:
        print(f"ERROR: Network/API request failed: {type(exc).__name__}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
