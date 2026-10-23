# Karnataka Yatra AI

An AI-assisted travel planner for Karnataka, built for the Kannada Digital Innovation Hackathon 2026.

## Features

* Personalized trip planning based on starting location, budget, duration, number of travellers, interests, transport, and travel style.
* Destination recommendations from a curated Karnataka-only dataset.
* Budget breakdown for transport, accommodation, food, activities, and buffer.
* Warnings and low-cost suggestions when the estimated trip cost exceeds the budget.
* Accommodation and hostel search shortcuts.
* Restaurant and local cuisine search suggestions.
* Destination ordering using a geographic heuristic.
* Optional AI-generated travel notes, with a fallback when no API key is configured.
* Interactive map using Leaflet and OpenStreetMap.
* Kannada travel phrase guide.
* External travel tools for trip planning, transport, accommodation, and maps.
* SQLite storage for generated itineraries.
* Export itinerary as JSON and print or save as PDF.

**Note:** Accommodation and restaurant cards are search shortcuts, not verified live listings. Costs are estimates, not live quotes. External travel services are not fully integrated booking APIs.

## Technology Stack

**Frontend**

* React
* Vite
* Leaflet and React Leaflet
* CSS

**Backend**

* Python
* FastAPI
* Pydantic
* SQLite

**Optional AI**

* OpenAI-compatible Chat Completions API

## Run Locally

### 1. Backend

Python 3.10 or newer is recommended.

Open a terminal:

```bash
cd backend
python -m venv venv
```

On Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

On macOS or Linux:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the backend:

```bash
uvicorn main:app --reload
```

Backend API documentation:

http://127.0.0.1:8000/docs

Optional AI setup: Copy `.env.example` to `.env` and configure the required API settings. Never publish API keys.

### 2. Frontend

Open a second terminal:

```bash
cd frontend
npm install
npm run dev
```

If required, create `frontend/.env` and set:

```env
VITE_API_URL=http://127.0.0.1:8000
```

Open the local URL printed in the terminal, usually:

http://localhost:5173

## Deployment

### Backend

Deploy the `backend` directory to a Python hosting service such as Render.

Example start command:

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

Configure CORS and any optional AI credentials in the hosting service's environment settings.

### Frontend

Deploy the `frontend` directory to Vercel or another static hosting service.

Set `VITE_API_URL` to the deployed backend URL and rebuild the frontend.

**Important:** SQLite data may not persist on hosting services with ephemeral storage unless persistent storage is configured.

## Limitations

* Destination costs are illustrative estimates.
* Route ordering is a geographic heuristic, not live road navigation.
* Hotel availability, restaurant opening hours, transport fares, weather, and permits are not fetched live.
* AI-generated travel notes do not guarantee that a trip fits the requested budget.
* No bookings are made by this application.
* Verify prices, opening hours, and travel information before visiting.

## Hackathon Submission Checklist

* [ ] Public GitHub repository
* [ ] Presentation explaining the problem, solution, innovation, technology stack, and architecture
* [ ] Deployed application URL
* [ ] Three-to-five-minute project explanation video
* [ ] Final testing of the deployed application
