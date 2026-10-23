
import React from 'react';
import { MapContainer, TileLayer, Marker, Popup, Polyline } from 'react-leaflet';
import L from 'leaflet';
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl:'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png',
  iconUrl:'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png',
  shadowUrl:'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png'
});
export default function MapView({itinerary=[]}) {
  const points = itinerary.map(x=>[x.coordinates.lat,x.coordinates.lon]);
  const center = points[0] || [14.5,76.0];
  return <div className="map-wrap"><MapContainer center={center} zoom={6} scrollWheelZoom={false} style={{height:'360px',width:'100%'}}>
    <TileLayer attribution='&copy; OpenStreetMap contributors' url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"/>
    {itinerary.map((item,i)=><Marker key={`${item.day}-${item.destination}`} position={[item.coordinates.lat,item.coordinates.lon]}><Popup><b>Day {item.day}: {item.destination}</b><br/>{item.suggested_plan}</Popup></Marker>)}
    {points.length>1 && <Polyline positions={points}/>}
  </MapContainer></div>;
}
