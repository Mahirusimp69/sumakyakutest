# Sumaq Yaku - Water Distribution System

## Overview

Sumaq Yaku is a Flask-based web application designed to optimize water distribution routes and flows in Arequipa, Peru. The system uses graph theory and network analysis to calculate optimal paths from water reservoirs to critical consumption points, providing real-time visualization of the water distribution network on an interactive map.

## System Architecture

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **Database**: PostgreSQL with SQLAlchemy ORM for data persistence
- **Graph Processing**: NetworkX library for graph algorithms and route optimization
- **Geospatial Calculations**: Geopy for distance calculations between geographic points
- **Data Processing**: Pandas for CSV data manipulation
- **Network Data**: OSMnx for road network data generation from OpenStreetMap

### Frontend Architecture
- **Template Engine**: Jinja2 (Flask's default templating)
- **CSS Framework**: Bootstrap 5 with dark theme
- **Interactive Maps**: Leaflet.js for geographic visualization
- **Icons**: Font Awesome for UI elements
- **JavaScript**: Vanilla JS for map interactions and API calls

### Data Architecture
- **Primary Storage**: PostgreSQL database with relational tables
- **Secondary Storage**: CSV files for initial data loading and backup
- **Database Models**: Embalses, PuntosCriticos, Nodos, Aristas, Procesamientos, HistorialRutas
- **Processing**: In-memory graph construction using NetworkX DiGraph
- **Persistence**: Automatic saving of processing results and route calculations

## Key Components

### Core Application Files
- `app.py`: Main Flask application with route handlers
- `main.py`: Application entry point
- `grafo_agua.py`: Core graph construction and optimization algorithms
- `generar_red_arequipa.py`: Network data generation utility

### Data Components
- Reservoirs (embalses.csv): Water storage facilities with capacity data
- Critical Points (puntos_criticos.csv): High-priority consumption locations
- Nodes (nodos.csv): Network junction points with geographic coordinates
- Edges (aristas.csv): Connections between nodes with distance and status

### Frontend Components
- Interactive map visualization using Leaflet
- Real-time route and flow calculation display
- Bootstrap-based responsive UI
- Status monitoring and system verification

## Data Flow

1. **Data Loading**: CSV files are loaded and validated using pandas
2. **Graph Construction**: NetworkX directed graph is built from infrastructure data
3. **Route Calculation**: Dijkstra's algorithm finds optimal paths from reservoirs to critical points
4. **Flow Analysis**: Maximum flow algorithms calculate water distribution capacity
5. **Visualization**: Results are rendered on an interactive map with route overlays
6. **User Interaction**: Real-time processing triggered by user actions

## External Dependencies

### Python Libraries
- Flask: Web framework and routing
- NetworkX: Graph algorithms and network analysis
- Pandas: Data manipulation and CSV processing
- Geopy: Geographic distance calculations
- OSMnx: OpenStreetMap network data extraction

### Frontend Libraries
- Leaflet.js: Interactive mapping functionality
- Bootstrap 5: UI framework and responsive design
- Font Awesome: Icon library

### Data Sources
- OpenStreetMap: Road network data for Arequipa
- CSV files: Water infrastructure data (reservoirs, critical points, network topology)

## Deployment Strategy

### Development Environment
- Flask development server with debug mode enabled
- Hot reloading for rapid development iterations
- Environment variable configuration for secrets

### Production Considerations
- Host: 0.0.0.0 for container compatibility
- Port: 5000 (configurable)
- Secret key management through environment variables
- Static file serving through Flask (consider CDN for production)

### Data Requirements
- Ensure data/ directory exists with required CSV files
- Validate CSV schema compatibility before deployment
- Consider data backup and versioning strategies

## User Preferences

Preferred communication style: Simple, everyday language in Spanish.

## Changelog

- Junio 28, 2025: Configuración inicial del sistema Sumaq Yaku
- Junio 28, 2025: Integración completa de base de datos PostgreSQL
  - Modelos de datos para embalses, puntos críticos, nodos y aristas
  - Historial de procesamientos con timestamps
  - Almacenamiento automático de resultados de rutas
  - Nuevos endpoints API para consultar datos históricos
  - Funcionalidad de importación de datos CSV a BD
- Junio 28, 2025: Funcionalidades extendidas de gestión de infraestructura
  - Formulario completo para agregar nodos con validación de IDs únicos
  - Formulario para agregar puntos críticos con tipos específicos
  - Integración con clic en mapa para coordenadas automáticas
  - Visualización mejorada de rutas calculadas en el mapa con líneas de colores
  - Endpoints API para /api/agregar-nodo y /api/agregar-punto-critico
  - Estilos CSS mejorados para formularios y visualización de rutas