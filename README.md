
# Karnataka Yatra AI

An AI-assisted travel planner for Karnataka, built for the Kannada Digital Innovation Hackathon 2026 problem statement **AI Travel Planner for Karnataka**.

## Features
- Personalized trip planning from starting location, budget, days, party size, interests, transport and travel style.
- Destination recommendations from a curated Karnataka-only dataset.
- Hostel/guesthouse search-area and local restaurant/cuisine suggestions for each destination (not verified live listings).
- Budget breakdown for transport, accommodation, food, activities and buffer.
- Low-budget warning and free/low-cost alternative guidance when the requested budget is insufficient.
- Curated destination recommendations restricted to Karnataka, India.
- Greedy nearest-neighbour ordering between selected destination coordinates.
- Optional LLM-generated travel notes, with a built-in fallback when no API key is configured.
- Interactive map using Leaflet and OpenStreetMap.
- Kannada travel phrase guide.
- Karnataka-focused accommodation and restaurant search cards.
- External travel toolkit links for trip organization, transport, stays and maps.
- Stay and restaurant area suggestions for each curated Karnataka destination (not live business listings).
- SQLite storage for recent generated plans.
- Print/save as PDF through browser print and export itinerary JSON.

## Stack
- Frontend: React, Vite, Leaflet, React Leaflet, CSS
- Backend: Python, FastAPI, Pydantic, SQLite
- Optional AI: OpenAI-compatible Chat Completions API

## Run locally

### 1. Backend
Python 3.10+ recommended.

```bash
cd backend
python -m venv venv
```

Windows PowerShell:
```powershell
.\venv\Scripts\Activate.ps1
```

macOS/Linux:
```bash
source venv/bin/activate
```

Install dependencies and run:
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Backend docs: http://127.0.0.1:8000/docs

Optional AI setup: copy `.env.example` to `.env` and add an API key. Never commit `.env` or API keys.

### 2. Frontend
Open a second terminal:
```bash
cd frontend
npm install
```

Create `frontend/.env` if needed:
```env
VITE_API_URL=http://127.0.0.1:8000
```

Start:
```bash
npm run dev
```

Open the Vite URL printed in the terminal, usually http://localhost:5173.

## Deployment outline
- Deploy `backend/` to a Python host such as Render. Build/install command: `pip install -r requirements.txt`; start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`.
- Set `CORS_ORIGINS` to the deployed frontend origin and configure optional AI environment variables in the host's environment settings.
- Deploy `frontend/` to Vercel or another static frontend host. Set `VITE_API_URL` to the deployed backend URL, then rebuild.
- SQLite on ephemeral hosting may not persist across deploys unless a persistent disk is configured. For a judged demo, verify saved-trip persistence on the chosen host.
- Test the live application and all API routes before submitting.

## External travel services
The travel-tool links open third-party services. They are not private API integrations and do not provide live availability, verified prices, bookings, or confirmation. Stay and restaurant cards are search shortcuts, not verified individual listings.

## Important limitations
- Destination costs are illustrative planning estimates, not live quotes.
- The route ordering is a simple geographic heuristic, not a live road-routing service; it does not geocode the starting location.
- Opening hours, transport schedules, hotel availability, weather and permits are not fetched live.
- The optional LLM provides text notes only. Budget calculations and route ordering are performed by backend code.
- Do not claim bookings are made. Confirm all details from official sources before travelling.

## Hackathon submission checklist
- [ ] Public GitHub repository with this README
- [ ] PPT explaining problem, existing system, differentiation, approach, stack/architecture and conclusion
- [ ] Deployed working application URL
- [ ] 3–5 minute voice-over explanation video
