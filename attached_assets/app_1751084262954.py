from flask import Flask, render_template, jsonify
from grafo_agua import cargar_datos, construir_grafo, calcular_rutas_y_flujos

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("interfaz.html")

@app.route("/procesar", methods=["POST"])
def procesar():
    embalses, puntos, nodos, aristas = cargar_datos()
    G = construir_grafo(embalses, puntos, nodos, aristas)
    fuente = embalses.iloc[0]['Nombre']
    rutas, flujos = calcular_rutas_y_flujos(G, fuente)

    nodos_json = [{"id": n, **d} for n, d in G.nodes(data=True)]
    aristas_json = [{"origen": u, "destino": v, **d} for u, v, d in G.edges(data=True)]

    return jsonify({
        "rutas_optimas": rutas,
        "flujos_maximos": flujos,
        "nodos": nodos_json,
        "aristas": aristas_json
    })

if __name__ == "__main__":
    app.run(debug=True)