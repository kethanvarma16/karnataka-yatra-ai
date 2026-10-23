def estimate_budget(destinations, total_budget, days, travelers, transport, travel_style):
    """Illustrative estimates only. Flag low-cost planning when budget is insufficient."""
    if not destinations:
        destinations = [{"name":"Karnataka","daily_cost_per_person":1200}]
    transport_factor = {"bus/train": 1.0, "car": 1.8, "flight": 2.8}.get(transport.lower(), 1.0)
    style_factor = {"budget": 0.8, "standard": 1.0, "comfort": 1.45}.get(travel_style.lower(), 0.8)
    daily = []
    for day in range(days):
        dest = destinations[day % len(destinations)]
        per_person = float(dest.get("daily_cost_per_person", 1200)) * style_factor
        transport_cost = 180 * transport_factor * travelers
        lodging = per_person * 0.32 * travelers
        food = per_person * 0.28 * travelers
        activities = per_person * 0.12 * travelers
        local_transport = per_person * 0.08 * travelers
        buffer = per_person * 0.05 * travelers
        total = transport_cost + lodging + food + activities + local_transport + buffer
        daily.append({"day":day+1,"destination":dest.get("name","Karnataka"),
          "transport":round(transport_cost,2),"accommodation":round(lodging,2),
          "food":round(food,2),"activities":round(activities,2),
          "local_transport":round(local_transport,2),"buffer":round(buffer,2),"total":round(total,2)})
    estimated_total = round(sum(row["total"] for row in daily), 2)
    remaining = round(total_budget-estimated_total, 2)
    low_budget_mode = total_budget < estimated_total
    guidance = ("Try free public parks/viewpoints, walking routes and local public transport. A ₹1,000 total budget may not cover intercity travel, food and accommodation for multiple travellers. Consider a nearby day trip, fewer travellers, or increasing the budget. Verify current fees and fares."
      if low_budget_mode else "Keep a contingency reserve and verify current prices before travel.")
    return {"estimated_total":estimated_total,"budget":round(total_budget,2),"remaining":remaining,
      "over_budget":estimated_total>total_budget,"low_budget_mode":low_budget_mode,
      "budget_status":"over_budget" if low_budget_mode else "within_estimate",
      "low_cost_guidance":guidance,"currency":"INR","daily_breakdown":daily,
      "categories":{"transport":round(sum(x["transport"]+x["local_transport"] for x in daily),2),
        "accommodation":round(sum(x["accommodation"] for x in daily),2),
        "food":round(sum(x["food"] for x in daily),2),
        "activities":round(sum(x["activities"] for x in daily),2),
        "buffer":round(sum(x["buffer"] for x in daily),2)},
      "note":"Illustrative estimates only; no live fare, hotel or ticket prices are retrieved."}
