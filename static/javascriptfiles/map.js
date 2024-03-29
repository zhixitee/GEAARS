var map = L.map('map').setView([55.8609, -4.2514], 13);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
maxZoom: 19,
attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

var barrowlandsLocation = L.marker([55.8553, -4.2367]).addTo(map);
    barrowlandsLocation.bindPopup("<b>Barrowland Ballrom:</b> Extremely iconic venue in Glasgow<br>").openPopup();

var hydroLocation = L.marker([55.8601, -4.2876]).addTo(map);
    hydroLocation.bindPopup("<b>SEC Hydro:</b> One of the biggest music venues in Glasgow<br>").openPopup();

var kingsTutsLocation = L.marker([55.8645, -4.2648]).addTo(map);
    kingsTutsLocation.bindPopup("<b> King Tut's Wah Wah Hut:</b><br>Iconic music venue in Glasgow.").openPopup();

var bellahoustonParkLocation = L.marker([55.8474, -4.3151]).addTo(map);
    bellahoustonParkLocation.bindPopup("<b>Bellahouston Park:</b><br> A beautiful public park in Glasgow.").openPopup();