from flask import Flask
from flask import render_template
from flask import Response, request, jsonify
from flask import send_file
import condicionalesLetra
from captureVideo  import generate, save_variables_to_json 
from exportarPDF import generate_pdf
import json, os

app = Flask(__name__, template_folder='templates', 
            static_folder='static')
entrada=""
@app.route("/")
def index():
     return render_template('index.html')

@app.route('/menu')
def menu():
    return render_template('menu.html') 

@app.route('/monitoreo')
def monitoreo():
    return render_template('monitoreo.html') 

@app.route('/letra')
def letra():
    return render_template('letra.html') 

# Variable global para almacenar el estado de tiempo_guardado
var= False

prev_json_size = 0

# Ruta para obtener el tamaño y contenido del archivo JSON
@app.route('/get_json_size_<letra>', methods=['GET'])
def get_json_info(letra):
    json_file_path = f"./static/json/tiempo_{letra}.json"  
    json_size = os.path.getsize(json_file_path)
    return jsonify({'json_size': json_size})




@app.route("/video_feed_<letra>")
def video_feed(letra):
    condicionales_por_letra = {
        "A": condicionalesLetra.condicionalesLetrasA,
        "B": condicionalesLetra.condicionalesLetrasB,
        "C": condicionalesLetra.condicionalesLetrasC,
        "CH": condicionalesLetra.condicionalesLetrasCH,
        "D": condicionalesLetra.condicionalesLetrasD,
        "E": condicionalesLetra.condicionalesLetrasE,
        "F": condicionalesLetra.condicionalesLetrasF,
        "G": condicionalesLetra.condicionalesLetrasG,
        "H": condicionalesLetra.condicionalesLetrasH,
        "I": condicionalesLetra.condicionalesLetrasI,
        "K": condicionalesLetra.condicionalesLetrasK,
        "L": condicionalesLetra.condicionalesLetrasL,
        "M": condicionalesLetra.condicionalesLetrasM,
        "N": condicionalesLetra.condicionalesLetrasN,
        "O": condicionalesLetra.condicionalesLetrasO,
        "P": condicionalesLetra.condicionalesLetrasP,
        "Q": condicionalesLetra.condicionalesLetrasQ,
        "R": condicionalesLetra.condicionalesLetrasR,
        "S": condicionalesLetra.condicionalesLetrasS,
        "T": condicionalesLetra.condicionalesLetrasT,
        "U": condicionalesLetra.condicionalesLetrasU,
        "V": condicionalesLetra.condicionalesLetrasV,
        "W": condicionalesLetra.condicionalesLetrasW,
        "X": condicionalesLetra.condicionalesLetrasX,
        "Y": condicionalesLetra.condicionalesLetrasY,
    }
    condicionales_letra = condicionales_por_letra.get(letra, condicionalesLetra.condicionalesLetrasA)
   
   
    return Response(generate(condicionales_letra,letra), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route('/Resultado')
def resultado():
    return render_template("resultado.html")

@app.route('/procesar', methods=['POST'])
def procesar():
    global entrada
    entrada = request.form.get('entrada', '')  # Obtener el texto ingresado
    return render_template('index.html')

def formato_time(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    formatted_time = f"{int(hours)} horas, {int(minutes)} minutos y {seconds:.2f} segundos"
    return formatted_time

@app.route('/generate_pdf', methods=['GET'])
def generate_pdf_route():
    global entrada
    # Cargar un JSON externo y convertirlo en un diccionario
    with open("./static/json/historial.json", "r") as json_file:
        json_data = json.load(json_file)
 
        # Obtener el diccionario "historial" del archivo cargado
        historial = json_data["historial"]

        # Calcular la sumatoria de los valores
        suma = sum(historial.values())
    dec_sum = "{:.2f}".format(suma)
    time_medida = formato_time(int(suma))  # Obtener la sumatoria formateada en horas, minutos y segundos



    # Llamar a la función para generar el PDF con los datos del JSON
    generate_pdf(json_data, "Sistema de Aprendizaje del Abecedario en Lengua de Señas Ecuatoriano",
                 "./static/access/elementosV/titulo.png", time_medida)
    # Limpiar el historial en el JSON cargado
    json_data["historial"] = {}
    # Guardar el JSON nuevamente con el historial vacío
    with open("./static/json/historial.json", "w") as json_file:
     json.dump(json_data, json_file)

    return send_file("HistorialSALSEC.pdf", as_attachment=True)

if __name__ == "__main__":
     app.run(debug=True)



if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
