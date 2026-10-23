
import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from ai_engine import generate_ai_notes
from budget_optimizer import estimate_budget
from route_planner import order_destinations
from database import init_db, save_trip, list_saved_trips

load_dotenv()
app = FastAPI(title="Karnataka Yatra AI", description="Karnataka-only personalized travel planning, budget estimates, stays and restaurant search shortcuts", version="1.0.0")
origins = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",")
app.add_middleware(CORSMiddleware, allow_origins=[x.strip() for x in origins], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

DESTINATIONS = [{'id': 'mysuru', 'name': 'Mysuru', 'region': 'South Karnataka', 'lat': 12.2958, 'lon': 76.6394, 'tags': ['history', 'culture', 'architecture', 'family'], 'daily_cost_per_person': 1800, 'suggested_days': 1, 'description': "Explore Mysore Palace, markets and the city's cultural heritage.", 'highlights': ['Mysore Palace', 'Devaraja Market', 'Chamundi Hill'], 'best_for': 'Culture, architecture and families', 'hostels': [{'name': 'Budget stays near Mysuru city centre', 'type': 'hostel/guesthouse', 'note': 'Suggested search area, not a verified property. Check current listings, prices and availability.'}], 'restaurants': [{'name': 'Mysuru local vegetarian eateries', 'type': 'local food', 'note': 'Cuisine/search suggestion, not a verified restaurant listing. Check current listings and opening hours.'}]}, {'id': 'coorg', 'name': 'Coorg (Kodagu)', 'region': 'Western Ghats', 'lat': 12.3375, 'lon': 75.8069, 'tags': ['nature', 'mountains', 'coffee', 'adventure', 'relaxation'], 'daily_cost_per_person': 2300, 'suggested_days': 2, 'description': 'Coffee estates, misty hills and scenic viewpoints.', 'highlights': ['Coffee estate visit', "Raja's Seat", 'Abbey Falls'], 'best_for': 'Nature and relaxed getaways', 'hostels': [{'name': 'Budget stays in Madikeri', 'type': 'hostel/guesthouse', 'note': 'Suggested search area, not a verified property. Check current listings, prices and availability.'}], 'restaurants': [{'name': 'Kodagu local cuisine restaurants', 'type': 'local food', 'note': 'Cuisine/search suggestion, not a verified restaurant listing. Check current listings and opening hours.'}]}, {'id': 'hampi', 'name': 'Hampi', 'region': 'North Karnataka', 'lat': 15.335, 'lon': 76.46, 'tags': ['history', 'architecture', 'culture', 'photography'], 'daily_cost_per_person': 1900, 'suggested_days': 2, 'description': 'Discover the remarkable ruins and landscape of the Vijayanagara Empire.', 'highlights': ['Virupaksha Temple', 'Vittala Temple complex', 'Hampi Bazaar'], 'best_for': 'History and architecture', 'hostels': [{'name': 'Budget stays near Hampi Bazaar / Hospet', 'type': 'hostel/guesthouse', 'note': 'Suggested search area, not a verified property. Check current listings, prices and availability.'}], 'restaurants': [{'name': 'Hampi local cafes and eateries', 'type': 'local food', 'note': 'Cuisine/search suggestion, not a verified restaurant listing. Check current listings and opening hours.'}]}, {'id': 'gokarna', 'name': 'Gokarna', 'region': 'Coastal Karnataka', 'lat': 14.5479, 'lon': 74.3188, 'tags': ['beaches', 'nature', 'relaxation', 'adventure'], 'daily_cost_per_person': 2100, 'suggested_days': 2, 'description': 'Coastal scenery, beaches and a laid-back atmosphere.', 'highlights': ['Om Beach', 'Kudle Beach', 'Mahabaleshwar Temple'], 'best_for': 'Beaches and relaxation', 'hostels': [{'name': 'Budget stays around Gokarna town', 'type': 'hostel/guesthouse', 'note': 'Suggested search area, not a verified property. Check current listings, prices and availability.'}], 'restaurants': [{'name': 'Gokarna local seafood and vegetarian eateries', 'type': 'local food', 'note': 'Cuisine/search suggestion, not a verified restaurant listing. Check current listings and opening hours.'}]}, {'id': 'jog-falls', 'name': 'Jog Falls', 'region': 'Malnad', 'lat': 14.2294, 'lon': 74.812, 'tags': ['nature', 'waterfalls', 'photography', 'adventure'], 'daily_cost_per_person': 1500, 'suggested_days': 1, 'description': 'Visit the dramatic Sharavathi River waterfall viewpoint; seasonal flow varies.', 'highlights': ['Jog Falls viewpoints', 'Sharavathi valley scenery'], 'best_for': 'Waterfalls and photography', 'hostels': [{'name': 'Budget stays in Sagara / nearby towns', 'type': 'hostel/guesthouse', 'note': 'Suggested search area, not a verified property. Check current listings, prices and availability.'}], 'restaurants': [{'name': 'Local eateries around Sagara', 'type': 'local food', 'note': 'Cuisine/search suggestion, not a verified restaurant listing. Check current listings and opening hours.'}]}, {'id': 'badami', 'name': 'Badami', 'region': 'North Karnataka', 'lat': 15.9149, 'lon': 75.6768, 'tags': ['history', 'architecture', 'culture', 'photography'], 'daily_cost_per_person': 1600, 'suggested_days': 1, 'description': 'Sandstone cave temples and historic Chalukyan architecture.', 'highlights': ['Badami Cave Temples', 'Agastya Lake', 'Badami Fort'], 'best_for': 'History and architecture', 'hostels': [{'name': 'Budget stays near Badami town', 'type': 'hostel/guesthouse', 'note': 'Suggested search area, not a verified property. Check current listings, prices and availability.'}], 'restaurants': [{'name': 'Badami local restaurants', 'type': 'local food', 'note': 'Cuisine/search suggestion, not a verified restaurant listing. Check current listings and opening hours.'}]}, {'id': 'belur-halebidu', 'name': 'Belur & Halebidu', 'region': 'Central Karnataka', 'lat': 13.1629, 'lon': 75.865, 'tags': ['history', 'architecture', 'culture'], 'daily_cost_per_person': 1500, 'suggested_days': 1, 'description': 'Intricate Hoysala temple architecture and heritage sites.', 'highlights': ['Chennakeshava Temple', 'Hoysaleswara Temple'], 'best_for': 'Heritage and architecture', 'hostels': [{'name': 'Budget stays near Belur / Halebidu', 'type': 'hostel/guesthouse', 'note': 'Suggested search area, not a verified property. Check current listings, prices and availability.'}], 'restaurants': [{'name': 'Local restaurants around Belur and Halebidu', 'type': 'local food', 'note': 'Cuisine/search suggestion, not a verified restaurant listing. Check current listings and opening hours.'}]}, {'id': 'udupi', 'name': 'Udupi', 'region': 'Coastal Karnataka', 'lat': 13.3409, 'lon': 74.7421, 'tags': ['beaches', 'food', 'culture', 'family'], 'daily_cost_per_person': 1900, 'suggested_days': 1, 'description': 'Temple heritage, coastal attractions and celebrated local cuisine.', 'highlights': ['Sri Krishna Matha', 'Malpe Beach', "St. Mary's Island (check access)"], 'best_for': 'Food, culture and coast', 'hostels': [{'name': 'Budget stays near Udupi city centre', 'type': 'hostel/guesthouse', 'note': 'Suggested search area, not a verified property. Check current listings, prices and availability.'}], 'restaurants': [{'name': 'Udupi vegetarian restaurants', 'type': 'local food', 'note': 'Cuisine/search suggestion, not a verified restaurant listing. Check current listings and opening hours.'}]}, {'id': 'bengaluru', 'name': 'Bengaluru', 'region': 'South Karnataka', 'lat': 12.9716, 'lon': 77.5946, 'tags': ['food', 'culture', 'family', 'technology', 'parks'], 'daily_cost_per_person': 2000, 'suggested_days': 1, 'description': 'A lively city with gardens, museums, food and technology culture.', 'highlights': ['Lalbagh', 'Cubbon Park', 'Bengaluru Palace'], 'best_for': 'City breaks and food', 'hostels': [{'name': 'Budget hostels around central Bengaluru / transit hubs', 'type': 'hostel/guesthouse', 'note': 'Suggested search area, not a verified property. Check current listings, prices and availability.'}], 'restaurants': [{'name': 'Bengaluru local eateries and darshinis', 'type': 'local food', 'note': 'Cuisine/search suggestion, not a verified restaurant listing. Check current listings and opening hours.'}]}, {'id': 'chikkamagaluru', 'name': 'Chikkamagaluru', 'region': 'Western Ghats', 'lat': 13.3161, 'lon': 75.772, 'tags': ['nature', 'mountains', 'coffee', 'adventure'], 'daily_cost_per_person': 2200, 'suggested_days': 2, 'description': 'Coffee country, mountain views and scenic drives.', 'highlights': ['Mullayanagiri area', 'Coffee estates', 'Hirekolale Lake'], 'best_for': 'Mountains and nature', 'hostels': [{'name': 'Budget stays in Chikkamagaluru town', 'type': 'hostel/guesthouse', 'note': 'Suggested search area, not a verified property. Check current listings, prices and availability.'}], 'restaurants': [{'name': 'Chikkamagaluru local restaurants', 'type': 'local food', 'note': 'Cuisine/search suggestion, not a verified restaurant listing. Check current listings and opening hours.'}]}]
DEST_BY_ID = {d["id"]: d for d in DESTINATIONS}


STAYS = [
 {"id":"stay-mysuru","name":"Budget stays in Mysuru","city":"Mysuru","type":"Budget hotel / guesthouse","price_hint":"Check current rates","note":"Search shortcut, not a verified property listing.","search_url":"https://www.booking.com/searchresults.html?ss=Mysuru%2C+Karnataka"},
 {"id":"stay-coorg","name":"Hostels and guesthouses in Coorg","city":"Madikeri, Coorg","type":"Hostel / guesthouse","price_hint":"Check current rates","note":"Confirm location, reviews, taxes and cancellation terms.","search_url":"https://www.hostelworld.com/"},
 {"id":"stay-hampi","name":"Stays near Hampi","city":"Hampi","type":"Guesthouse / budget stay","price_hint":"Check current rates","note":"Check the exact location and transport access before booking.","search_url":"https://www.booking.com/searchresults.html?ss=Hampi%2C+Karnataka"},
 {"id":"stay-gokarna","name":"Hostels and stays in Gokarna","city":"Gokarna","type":"Hostel / guesthouse","price_hint":"Check current rates","note":"Check seasonal pricing and beach access.","search_url":"https://www.hostelworld.com/"},
 {"id":"stay-bengaluru","name":"Hostels and stays in Bengaluru","city":"Bengaluru","type":"Hostel / hotel","price_hint":"Check current rates","note":"Choose accommodation near your transit or sightseeing area.","search_url":"https://www.booking.com/searchresults.html?ss=Bengaluru%2C+Karnataka"}
]
RESTAURANTS = [
 {"id":"food-mysuru","name":"Restaurants in Mysuru","city":"Mysuru","cuisine":"Mysuru / Karnataka cuisine","note":"Verify current opening hours, prices and reviews.","search_url":"https://www.google.com/maps/search/restaurants+in+Mysuru+Karnataka"},
 {"id":"food-coorg","name":"Restaurants in Coorg","city":"Madikeri, Coorg","cuisine":"Kodava / Karnataka cuisine","note":"Check opening hours and dietary options.","search_url":"https://www.google.com/maps/search/restaurants+in+Madikeri+Karnataka"},
 {"id":"food-hampi","name":"Restaurants in Hampi","city":"Hampi","cuisine":"Local and traveller-friendly food","note":"Check current opening hours and location.","search_url":"https://www.google.com/maps/search/restaurants+in+Hampi+Karnataka"},
 {"id":"food-gokarna","name":"Restaurants in Gokarna","city":"Gokarna","cuisine":"Coastal Karnataka cuisine","note":"Check seasonal hours and food preferences.","search_url":"https://www.google.com/maps/search/restaurants+in+Gokarna+Karnataka"},
 {"id":"food-bengaluru","name":"Restaurants in Bengaluru","city":"Bengaluru","cuisine":"Kannada, South Indian and international","note":"Verify opening hours, prices and recent reviews.","search_url":"https://www.google.com/maps/search/restaurants+in+Bengaluru+Karnataka"}
]
TRAVEL_TOOLS = [
 {"category":"Trip organization","name":"Wanderlog","description":"Organize trip days, places and notes","url":"https://wanderlog.com/"},
 {"category":"Trip organization","name":"Google Travel","description":"Explore travel information and trip ideas","url":"https://www.google.com/travel/"},
 {"category":"Trip organization","name":"GuideGeek","description":"AI travel assistant","url":"https://guidegeek.com/"},
 {"category":"Transportation","name":"Rome2Rio","description":"Compare possible transport routes","url":"https://www.rome2rio.com/"},
 {"category":"Transportation","name":"MakeMyTrip","description":"Search travel options and bookings","url":"https://www.makemytrip.com/"},
 {"category":"Transportation","name":"ixigo","description":"Search train, bus and flight options","url":"https://www.ixigo.com/"},
 {"category":"Transportation","name":"Skyscanner","description":"Compare flight options","url":"https://www.skyscanner.co.in/"},
 {"category":"Transportation","name":"Hopper","description":"Travel price-tracking app; availability varies by region","url":"https://hopper.com/"},
 {"category":"Accommodation","name":"Booking.com","description":"Search hotels and guesthouses","url":"https://www.booking.com/"},
 {"category":"Accommodation","name":"Hostelworld","description":"Search hostels","url":"https://www.hostelworld.com/"},
 {"category":"Maps & outdoors","name":"Google Maps","description":"Search places, directions and opening hours","url":"https://maps.google.com/"},
 {"category":"Maps & outdoors","name":"AllTrails","description":"Explore hiking routes and trail information","url":"https://www.alltrails.com/"},
 {"category":"Maps & outdoors","name":"Roadtrippers","description":"Plan road trips and stops","url":"https://roadtrippers.com/"}
]

class TripRequest(BaseModel):
    starting_location: str = Field(min_length=2, max_length=100)
    budget: float = Field(gt=0, le=10000000)
    days: int = Field(ge=1, le=30)
    travelers: int = Field(ge=1, le=50)
    interests: List[str] = []
    travel_style: str = "budget"
    transport: str = "bus/train"
    include_ai: bool = True

@app.on_event("startup")
def startup():
    init_db()

@app.get("/")
def root():
    return {"message":"Karnataka Yatra AI API is running","docs":"/docs","status":"ok"}

@app.get("/api/health")
def health():
    return {"status":"ok","ai_configured":bool(os.getenv("OPENAI_API_KEY"))}

@app.get("/api/destinations")
def get_destinations():
    return {"count":len(DESTINATIONS),"destinations":DESTINATIONS}


@app.get("/api/places")
def get_places():
    return {
        "scope": "Karnataka, India only",
        "destinations": [
            {
                "id": d["id"], "name": d["name"], "region": d["region"],
                "lat": d["lat"], "lon": d["lon"], "description": d["description"],
                "hostels": d.get("hostels", []), "restaurants": d.get("restaurants", [])
            } for d in DESTINATIONS
        ],
        "note": "Hostel and restaurant entries are suggested search areas/cuisine categories, not verified businesses or live availability."
    }

@app.post("/api/plan-trip")
def plan_trip(req: TripRequest):
    interests = {x.strip().lower() for x in req.interests if x.strip()}
    # Score Karnataka destinations by interest match and affordability.
    # Costs in DESTINATIONS are illustrative daily per-person estimates, not live prices.
    daily_budget_per_person = req.budget / max(req.days * req.travelers, 1)
    scored = []
    for d in DESTINATIONS:
        overlap = len(interests.intersection(set(t.lower() for t in d.get("tags", []))))
        interest_score = overlap * 3 if interests else 1
        estimated_daily = float(d.get("daily_cost_per_person", 2000))
        # Prefer cheaper destinations when the requested budget is tight.
        if daily_budget_per_person <= 1000:
            affordability_score = max(0, (1800 - estimated_daily) / 300)
        elif daily_budget_per_person <= 2000:
            affordability_score = max(0, (2400 - estimated_daily) / 600)
        else:
            affordability_score = 0
        style_score = 0.5 if req.travel_style.lower() == "comfort" else 0
        score = interest_score + affordability_score + style_score
        scored.append((score, estimated_daily, d))
    scored.sort(key=lambda item: (-item[0], item[1], item[2]["name"].lower()))
    candidates = [d for _, _, d in scored] or DESTINATIONS[:]
    # Choose distinct destinations first. Repeat a base destination only when the trip is longer.
    selected = candidates[:min(req.days, len(candidates))]
    if not selected:
        selected = DESTINATIONS[:1]
    selected = order_destinations(selected, req.starting_location)
    if not selected:
        selected = DESTINATIONS[:1]
    budget = estimate_budget(selected, req.budget, req.days, req.travelers, req.transport, req.travel_style)
    itinerary = []
    for day in range(req.days):
        d = selected[day % len(selected)]
        activities = d["highlights"][:]
        itinerary.append({
            "day": day + 1,
            "destination": d["name"],
            "region": d["region"],
            "activities": activities,
            "suggested_plan": d["description"],
            "estimated_cost": budget["daily_breakdown"][day]["total"],
            "coordinates": {"lat": d["lat"], "lon": d["lon"]}
        })
    ai_notes = None
    if req.include_ai:
        request_data = req.model_dump() if hasattr(req, "model_dump") else req.dict()
        ai_notes = generate_ai_notes(request_data, itinerary, budget)
    result = {
        "project":"Karnataka Yatra AI",
        "starting_location":req.starting_location,
        "budget":req.budget,
        "days":req.days,
        "travelers":req.travelers,
        "interests":req.interests,
        "transport":req.transport,
        "itinerary":itinerary,
        "budget_summary":budget,
        "budget_guidance":budget["low_cost_guidance"],
        "destination_scope":"Karnataka, India only",
        "ai_notes":ai_notes,
        "disclaimer":"Costs are planning estimates, not live quotes. Verify transport, opening hours, weather, permits and accommodation before travelling."
    }
    trip_id = save_trip(result)
    result["trip_id"] = trip_id
    return result


@app.get("/api/local-recommendations")
def local_recommendations(destination: str = ""):
    """Curated Karnataka-only stay and food ideas. These are category suggestions, not verified live listings."""
    normalized = destination.strip().lower()
    matches = [d for d in DESTINATIONS if not normalized or normalized in d["name"].lower() or normalized in d["id"].lower()]
    return {
        "scope": "Karnataka, India only",
        "note": "These are curated area/category suggestions, not verified individual business listings or live availability. Check current reviews, prices, opening hours and safety before booking.",
        "destinations": [
            {"id":d["id"],"name":d["name"],"region":d["region"],"stays":d.get("hostels",[]),"restaurants":d.get("restaurants",[])}
            for d in matches
        ]
    }


@app.get("/api/stays")
def get_stays(city: Optional[str] = None):
    results = STAYS
    if city:
        results = [x for x in STAYS if city.lower() in x["city"].lower()]
    return {"scope":"Karnataka, India only","count":len(results),"stays":results}

@app.get("/api/restaurants")
def get_restaurants(city: Optional[str] = None):
    results = RESTAURANTS
    if city:
        results = [x for x in RESTAURANTS if city.lower() in x["city"].lower()]
    return {"scope":"Karnataka, India only","count":len(results),"restaurants":results}

@app.get("/api/travel-tools")
def get_travel_tools():
    return {"tools":TRAVEL_TOOLS,"note":"External links only; live availability and bookings are not integrated."}

@app.get("/api/saved-trips")
def get_saved_trips():
    return {"trips":list_saved_trips()}

@app.get("/api/kannada-phrases")
def get_kannada_phrases():
    return {"phrases":[
      {"english":"Hello","kannada":"ನಮಸ್ಕಾರ","pronunciation":"Namaskāra"},
      {"english":"How much does this cost?","kannada":"ಇದು ಎಷ್ಟು?","pronunciation":"Idu eshtu?"},
      {"english":"Where is the bus stand?","kannada":"ಬಸ್ ನಿಲ್ದಾಣ ಎಲ್ಲಿದೆ?","pronunciation":"Bus nildāṇa ellide?"},
      {"english":"Please help me","kannada":"ದಯವಿಟ್ಟು ನನಗೆ ಸಹಾಯ ಮಾಡಿ","pronunciation":"Dayaviṭṭu nanage sahāya māḍi"},
      {"english":"I need water","kannada":"ನನಗೆ ನೀರು ಬೇಕು","pronunciation":"Nanage neeru beku"},
      {"english":"Thank you","kannada":"ಧನ್ಯವಾದಗಳು","pronunciation":"Dhanyavādagaḷu"}
    ]}
