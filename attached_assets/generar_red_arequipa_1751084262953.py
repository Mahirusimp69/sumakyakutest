pip install osmnx networkx pandas

import osmnx as ox
import pandas as pd

# Define la zona de interés
place_name = "Arequipa, Peru"
G = ox.graph_from_place(place_name, network_type='drive')
G = ox.simplify_graph(G)

# Listas para nodos y aristas
nodos = []
aristas = []

# Mapeo de ID personalizado
id_map = {}
for i, (node, data) in enumerate(G.nodes(data=True)):
    node_id = f"N{i+1:05}"
    id_map[node] = node_id
    nodos.append({
        "id_nodo": node_id,
        "latitud": data['y'],
        "longitud": data['x'],
        "tipo": "tubo",
        "estado": "transitable"
    })

for u, v, data in G.edges(data=True):
    aristas.append({
        "origen": id_map[u],
        "destino": id_map[v],
        "distancia": round(data.get('length', 0), 2),
        "estado": "transitable"
    })

# Guardar como CSV
pd.DataFrame(nodos).to_csv("nodos_arequipa.csv", index=False)
pd.DataFrame(aristas).to_csv("aristas_arequipa.csv", index=False)
print("✅ Nodos y aristas generados correctamente.")
