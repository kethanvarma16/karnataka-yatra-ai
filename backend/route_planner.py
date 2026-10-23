
import math

def haversine(a, b):
    lat1, lon1 = math.radians(a["lat"]), math.radians(a["lon"])
    lat2, lon2 = math.radians(b["lat"]), math.radians(b["lon"])
    dlat, dlon = lat2-lat1, lon2-lon1
    h = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    return 6371 * 2 * math.asin(math.sqrt(h))

def order_destinations(destinations, starting_location=""):
    """Greedy nearest-neighbour ordering between selected destination coordinates.
    Starting location is retained as user context; geocoding is not performed."""
    if len(destinations) < 2:
        return destinations
    remaining = destinations[:]
    ordered = [remaining.pop(0)]
    while remaining:
        current = ordered[-1]
        next_dest = min(remaining, key=lambda d: haversine(current, d))
        ordered.append(next_dest)
        remaining.remove(next_dest)
    return ordered
