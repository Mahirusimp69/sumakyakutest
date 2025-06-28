import pandas as pd
import networkx as nx
from geopy.distance import geodesic

def cargar_datos():
    embalses = pd.read_csv('data/embalses.csv')
    puntos = pd.read_csv('data/puntos_criticos.csv')
    nodos = pd.read_csv('data/nodos.csv')
    aristas = pd.read_csv('data/aristas.csv')
    return embalses, puntos, nodos, aristas

def construir_grafo(embalses, puntos, nodos, aristas):
    G = nx.DiGraph()
    for _, e in embalses.iterrows():
        G.add_node(e['Nombre'], pos=(e['Latitud'], e['Longitud']), tipo='embalse', capacidad=e['Volumen_Almacenado_m3'])
    for _, p in puntos.iterrows():
        G.add_node(p['Nombre'], pos=(p['Latitud'], p['Longitud']), tipo='punto_critico')
    for _, n in nodos.iterrows():
        G.add_node(n['id_nodo'], pos=(n['latitud'], n['longitud']), tipo=n['tipo'], estado=n['estado'])
    for _, a in aristas.iterrows():
        if a['origen'] in G.nodes and a['destino'] in G.nodes:
            pos1 = G.nodes[a['origen']]['pos']
            pos2 = G.nodes[a['destino']]['pos']
            dist = geodesic(pos1, pos2).kilometers
            color = 'red' if a['estado'] == 'bloqueado' else 'blue'
            G.add_edge(a['origen'], a['destino'], weight=dist, estado=a['estado'], color=color)
    return G

def calcular_rutas_y_flujos(G, fuente):
    rutas = {}
    flujos = {}
    destinos = [n for n, d in G.nodes(data=True) if d.get("tipo") == "punto_critico"]
    for destino in destinos:
        try:
            rutas[destino] = nx.dijkstra_path(G, fuente, destino, weight='weight')
        except:
            rutas[destino] = None
        try:
            flujos[destino] = nx.maximum_flow_value(G, fuente, destino, capacity='capacidad')
        except:
            flujos[destino] = 0
    return rutas, flujos