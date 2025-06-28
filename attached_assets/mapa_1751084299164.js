let map = L.map('map').setView([-16.2300, -71.2100], 13);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

function procesar() {
    fetch("/procesar", { method: "POST", headers: {'Content-Type': 'application/json'} })
    .then(res => res.json())
    .then(data => {
        data.nodos.forEach(n => {
            let color = n.estado === 'obstaculo' ? 'red' : n.tipo === 'embalse' ? 'green' : 'blue';
            L.circleMarker([n.pos[0], n.pos[1]], {
                radius: 6, color: color, fillOpacity: 0.8
            }).addTo(map).bindPopup(`${n.id} (${n.tipo})`);
        });
        data.aristas.forEach(a => {
            let n1 = data.nodos.find(n => n.id === a.origen);
            let n2 = data.nodos.find(n => n.id === a.destino);
            if (n1 && n2) {
                L.polyline([n1.pos, n2.pos], { color: a.color, weight: 2 }).addTo(map);
            }
        });
        let html = "<h3>Resultados</h3><b>Rutas:</b><br>";
        for (let k in data.rutas_optimas) {
            html += `${k}: ${data.rutas_optimas[k] ? data.rutas_optimas[k].join(" → ") : "No hay ruta"}<br>`;
        }
        html += "<br><b>Flujos:</b><br>";
        for (let k in data.flujos_maximos) {
            html += `${k}: ${data.flujos_maximos[k]}<br>`;
        }
        document.getElementById("resultados").innerHTML = html;
    });
}