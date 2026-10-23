
import os
import json
import urllib.request
import urllib.error

def generate_ai_notes(preferences, itinerary, budget):
    """Optional OpenAI-compatible chat completions integration; deterministic fallback otherwise."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return {
            "mode":"smart-fallback",
            "summary":f"Your {preferences['days']}-day trip is tailored to {', '.join(preferences.get('interests') or ['popular Karnataka experiences'])}.",
            "tips":[
                "Book intercity transport and accommodation early during weekends and holidays.",
                "Check official attraction timings and weather before departure.",
                "Keep a small buffer for local transport and unexpected costs.",
                "The itinerary uses estimated costs; confirm actual prices before booking."
            ]
        }
    endpoint = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1/chat/completions")
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    prompt = {
      "preferences": preferences,
      "itinerary": itinerary,
      "budget_summary": budget,
      "instruction":"Return concise JSON with keys summary (string), tips (array of strings), and local_experience (string). Use only the supplied destinations and costs. Do not invent live prices or claim bookings are made. Warn if budget is exceeded."
    }
    payload = json.dumps({"model":model,"messages":[
      {"role":"system","content":"You are a careful Karnataka travel planning assistant. Be practical, budget-aware, culturally respectful, and transparent about estimates."},
      {"role":"user","content":json.dumps(prompt, ensure_ascii=False)}
    ],"temperature":0.4,"response_format":{"type":"json_object"}}).encode("utf-8")
    req = urllib.request.Request(endpoint, data=payload, headers={"Authorization":f"Bearer {api_key}","Content-Type":"application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            data = json.loads(response.read().decode("utf-8"))
        content = data["choices"][0]["message"]["content"]
        parsed = json.loads(content)
        parsed["mode"] = "llm"
        return parsed
    except Exception:
        return {
            "mode":"smart-fallback",
            "summary":"Your itinerary has been generated using destination preferences and budget estimates. AI text generation was unavailable, so the planner used its built-in fallback.",
            "tips":["Verify transport and accommodation prices before booking.","Check weather, opening hours and local advisories.","Keep a contingency buffer for unexpected costs."]
        }
