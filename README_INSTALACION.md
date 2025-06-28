# Sumaq Yaku - Sistema de Distribución de Agua

## Descripción
Sistema web para optimización de rutas de distribución de agua en Arequipa, Perú. Utiliza algoritmos de grafos (Dijkstra y Ford-Fulkerson) para calcular rutas óptimas y flujos máximos.

## Instalación

### Requisitos
- Python 3.8+
- PostgreSQL (opcional, puede usar SQLite)

### Pasos de instalación

1. **Extraer archivos**
   ```bash
   tar -xzf sumaq_yaku_proyecto.tar.gz
   cd sumaq_yaku_proyecto
   ```

2. **Instalar dependencias**
   ```bash
   pip install flask flask-sqlalchemy networkx pandas geopy osmnx psycopg2-binary gunicorn email-validator
   ```

3. **Configurar base de datos**
   - Para PostgreSQL: Configurar DATABASE_URL en variables de entorno
   - Para SQLite: El sistema creará automáticamente una base de datos local

4. **Ejecutar aplicación**
   ```bash
   python main.py
   ```
   O con gunicorn:
   ```bash
   gunicorn --bind 0.0.0.0:5000 --reload main:app
   ```

5. **Acceder al sistema**
   - Abrir navegador en: http://localhost:5000

## Funcionalidades

- **Visualización de red**: Mapa interactivo con embalses, nodos y puntos críticos
- **Generación de red**: Crear red completa de 100+ nodos de distribución
- **Cálculo de rutas**: Algoritmo Dijkstra para rutas óptimas
- **Cálculo de flujos**: Algoritmo Ford-Fulkerson para capacidades máximas en L/h
- **Gestión de obstáculos**: Puntos críticos bloquean el flujo de agua
- **Interfaz intuitiva**: Agregar nodos y puntos críticos mediante formularios

## Estructura de archivos

- `app.py` - Aplicación principal Flask
- `grafo_agua.py` - Algoritmos de optimización
- `models.py` - Modelos de base de datos
- `generar_red_completa_arequipa.py` - Generador de red completa
- `data/` - Archivos CSV con datos de infraestructura
- `static/` - CSS y JavaScript
- `templates/` - Plantillas HTML

## Datos incluidos

- 5 embalses principales de Arequipa
- 200+ nodos de distribución
- 15+ puntos críticos (obstáculos)
- 250+ conexiones de red

## Soporte

Sistema desarrollado para gestión de agua en Arequipa, Perú.
Algoritmos optimizados para redes de distribución urbana.