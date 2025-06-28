"""
Generador de red completa de distribución de agua para Arequipa
Crea 100 nodos de distribución, puntos críticos como obstáculos, y aristas conectando la red
"""

import pandas as pd
import numpy as np
import random
from geopy.distance import geodesic

def generar_coordenadas_arequipa():
    """Genera coordenadas dentro del área urbana de Arequipa"""
    # Límites aproximados de Arequipa urbana
    lat_min, lat_max = -16.45, -16.35
    lng_min, lng_max = -71.60, -71.50
    
    return random.uniform(lat_min, lat_max), random.uniform(lng_min, lng_max)

def calcular_distancia(coord1, coord2):
    """Calcula distancia en km entre dos coordenadas"""
    return geodesic(coord1, coord2).kilometers

def generar_nodos_distribucion(num_nodos=100):
    """Genera nodos de distribución de agua por toda Arequipa"""
    nodos = []
    
    # Tipos de nodos de distribución
    tipos_distribucion = ['cuadra', 'tubo', 'bomba', 'valvula']
    estados = ['transitable', 'transitable', 'transitable', 'obstaculo']  # 75% transitable, 25% obstáculo
    
    for i in range(1, num_nodos + 1):
        lat, lng = generar_coordenadas_arequipa()
        
        nodo = {
            'id_nodo': f'D{i:03d}',  # D001, D002, etc. (D = Distribución)
            'latitud': round(lat, 6),
            'longitud': round(lng, 6),
            'tipo': random.choice(tipos_distribucion),
            'estado': random.choice(estados)
        }
        nodos.append(nodo)
    
    return nodos

def generar_puntos_criticos_obstaculos(num_puntos=15):
    """Genera puntos críticos que actúan como obstáculos donde NO puede pasar el agua"""
    puntos = []
    
    tipos_obstaculo = ['inundacion', 'deslizamiento', 'hundimiento', 'obra', 'contaminacion']
    prioridades = ['alta', 'media', 'baja']
    
    for i in range(1, num_puntos + 1):
        lat, lng = generar_coordenadas_arequipa()
        
        punto = {
            'nombre': f'PC_{i:03d}',  # PC_001, PC_002, etc.
            'latitud': round(lat, 6),
            'longitud': round(lng, 6),
            'tipo': random.choice(tipos_obstaculo),
            'prioridad': random.choice(prioridades),
            'poblacion_afectada': random.randint(100, 5000)
        }
        puntos.append(punto)
    
    return puntos

def generar_aristas_red(nodos_existentes, nodos_nuevos, puntos_criticos):
    """Genera aristas conectando toda la red, evitando puntos críticos"""
    aristas = []
    todos_nodos = nodos_existentes + nodos_nuevos
    
    # Crear un mapa de coordenadas para búsqueda rápida
    coords_nodos = {}
    for nodo in todos_nodos:
        coords_nodos[nodo['id_nodo']] = (nodo['latitud'], nodo['longitud'])
    
    # Agregar embalses también
    embalses = [
        {'id': 'Embalse_Chilina', 'coords': (-16.3969, -71.5375)},
        {'id': 'Embalse_Aguada_Blanca', 'coords': (-16.4091, -71.5875)},
        {'id': 'Embalse_Aguada_Pillones', 'coords': (-16.3969, -71.5175)},
        {'id': 'Embalse_Aguada_Chalhuanca', 'coords': (-16.4291, -71.5275)},
        {'id': 'Embalse_El_Frayle', 'coords': (-16.4191, -71.5675)}
    ]
    
    for embalse in embalses:
        coords_nodos[embalse['id']] = embalse['coords']
    
    # Conectar cada nodo a sus vecinos más cercanos
    for nodo in todos_nodos:
        if nodo['estado'] == 'obstaculo':
            continue  # Los nodos obstáculo no se conectan
            
        nodo_coords = (nodo['latitud'], nodo['longitud'])
        nodo_id = nodo['id_nodo']
        
        # Buscar los 3-5 nodos más cercanos
        distancias = []
        for otro_id, otras_coords in coords_nodos.items():
            if otro_id == nodo_id:
                continue
                
            dist = calcular_distancia(nodo_coords, otras_coords)
            if dist < 5.0:  # Solo conectar si está a menos de 5km
                distancias.append((otro_id, dist))
        
        # Ordenar por distancia y tomar los más cercanos
        distancias.sort(key=lambda x: x[1])
        num_conexiones = min(random.randint(2, 4), len(distancias))
        
        for i in range(num_conexiones):
            destino_id, distancia = distancias[i]
            
            # Verificar que el destino no sea un obstáculo
            destino_es_obstaculo = False
            for n in todos_nodos:
                if n['id_nodo'] == destino_id and n['estado'] == 'obstaculo':
                    destino_es_obstaculo = True
                    break
            
            if destino_es_obstaculo:
                continue
            
            # Verificar que no pase cerca de puntos críticos
            pasa_por_critico = False
            for pc in puntos_criticos:
                pc_coords = (pc['latitud'], pc['longitud'])
                dist_origen = calcular_distancia(nodo_coords, pc_coords)
                dist_destino = calcular_distancia(coords_nodos[destino_id], pc_coords)
                
                if min(dist_origen, dist_destino) < 0.5:  # A menos de 500m del punto crítico
                    pasa_por_critico = True
                    break
            
            if pasa_por_critico:
                continue
            
            # Crear la arista
            estado_arista = 'transitable'
            capacidad = 1000
            
            # Algunas aristas pueden estar bloqueadas por mantenimiento
            if random.random() < 0.1:  # 10% de probabilidad
                estado_arista = 'bloqueado'
                capacidad = 0
            
            arista = {
                'origen': nodo_id,
                'destino': destino_id,
                'distancia': round(distancia, 2),
                'estado': estado_arista,
                'capacidad': capacidad
            }
            aristas.append(arista)
    
    return aristas

def main():
    """Función principal para generar toda la red"""
    print("🚰 Generando red completa de distribución de agua para Arequipa...")
    
    # Cargar nodos existentes
    try:
        nodos_existentes = pd.read_csv('data/nodos.csv').to_dict('records')
        print(f"✓ Cargados {len(nodos_existentes)} nodos existentes")
    except FileNotFoundError:
        nodos_existentes = []
        print("✓ No hay nodos existentes, empezando desde cero")
    
    # Generar nuevos nodos de distribución
    print("📍 Generando 100 nodos de distribución...")
    nodos_nuevos = generar_nodos_distribucion(100)
    
    # Combinar todos los nodos
    todos_nodos = nodos_existentes + nodos_nuevos
    
    # Generar puntos críticos como obstáculos
    print("⚠️ Generando 15 puntos críticos (obstáculos)...")
    puntos_criticos = generar_puntos_criticos_obstaculos(15)
    
    # Generar aristas conectando toda la red
    print("🔗 Generando conexiones de la red...")
    aristas = generar_aristas_red(nodos_existentes, nodos_nuevos, puntos_criticos)
    
    # Guardar en archivos CSV
    print("💾 Guardando archivos...")
    
    # Nodos
    df_nodos = pd.DataFrame(todos_nodos)
    df_nodos.to_csv('data/nodos.csv', index=False)
    print(f"✓ Guardados {len(todos_nodos)} nodos en data/nodos.csv")
    
    # Puntos críticos
    df_puntos = pd.DataFrame(puntos_criticos)
    df_puntos.to_csv('data/puntos_criticos.csv', index=False)
    print(f"✓ Guardados {len(puntos_criticos)} puntos críticos en data/puntos_criticos.csv")
    
    # Aristas
    df_aristas = pd.DataFrame(aristas)
    df_aristas.to_csv('data/aristas.csv', index=False)
    print(f"✓ Guardadas {len(aristas)} conexiones en data/aristas.csv")
    
    print("\n🎉 Red completa generada exitosamente!")
    print(f"📊 Resumen:")
    print(f"   • {len(todos_nodos)} nodos de distribución")
    print(f"   • {len(puntos_criticos)} puntos críticos (obstáculos)")
    print(f"   • {len(aristas)} conexiones de red")
    print(f"   • ~{len([n for n in todos_nodos if n['estado'] == 'obstaculo'])} nodos obstáculo")

if __name__ == "__main__":
    main()