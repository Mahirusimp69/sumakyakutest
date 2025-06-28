"""
Script to generate road network data for Arequipa, Peru using OSMnx.
This script creates nodes and edges CSV files for the water distribution system.
"""

import osmnx as ox
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

def generar_red_arequipa():
    """Generate road network data for Arequipa, Peru."""
    try:
        # Define the area of interest
        place_name = "Arequipa, Peru"
        logging.info(f"Downloading road network data for {place_name}")
        
        # Download and process the road network
        G = ox.graph_from_place(place_name, network_type='drive')
        G = ox.simplify_graph(G)
        
        logging.info(f"Downloaded network with {len(G.nodes)} nodes and {len(G.edges)} edges")
        
        # Lists for nodes and edges
        nodos = []
        aristas = []
        
        # Custom ID mapping
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
        
        # Process edges
        for u, v, data in G.edges(data=True):
            aristas.append({
                "origen": id_map[u],
                "destino": id_map[v],
                "distancia": round(data.get('length', 0), 2),
                "estado": "transitable"
            })
        
        # Save as CSV files
        nodos_df = pd.DataFrame(nodos)
        aristas_df = pd.DataFrame(aristas)
        
        nodos_df.to_csv("data/nodos_arequipa.csv", index=False)
        aristas_df.to_csv("data/aristas_arequipa.csv", index=False)
        
        logging.info("✅ Nodes and edges generated successfully.")
        logging.info(f"Generated {len(nodos)} nodes and {len(aristas)} edges")
        
        return nodos_df, aristas_df
        
    except Exception as e:
        logging.error(f"Error generating network data: {e}")
        raise

if __name__ == "__main__":
    # Note: This script requires osmnx to be installed
    # pip install osmnx networkx pandas
    generar_red_arequipa()
