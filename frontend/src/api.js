const API_BASE = (import.meta.env.VITE_API_URL || 'https://karnataka-yatra-ai.onrender.com').replace(/\/+$/, '');
export async function fetchDestinations() {
  const res = await fetch(`${API_BASE}/api/destinations`);
  if (!res.ok) throw new Error('Could not load destinations');
  return (await res.json()).destinations;
}
export async function generateTrip(payload) {
  const res = await fetch(`${API_BASE}/api/plan-trip`, {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
  const data = await res.json().catch(()=>({detail:'Unexpected server response'}));
  if (!res.ok) throw new Error(data.detail || 'Could not generate trip');
  return data;
}
export async function fetchPhrases() {
  const res = await fetch(`${API_BASE}/api/kannada-phrases`);
  if (!res.ok) throw new Error('Could not load Kannada phrases');
  return (await res.json()).phrases;
}
