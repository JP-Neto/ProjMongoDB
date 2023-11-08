from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__,template_folder='template')

client = MongoClient("localhost", 27017)
db = client['veiculos']
collection_carros = db.carros

@app.route("/", methods=['GET'])
def index():
    carros = db.carros.find().sort("_id",-1)

    return render_template("index.html", carros = carros) 

@app.route("/listar", methods=['GET', 'POST'])
def list_carro():
    carros = db.carros.find().sort("_id", -1)
    return render_template("listar.html", carros = carros) 

@app.route("/<id>/editar")
def editar_carro(id):
    carros = collection_carros.find_one({"_id": ObjectId(id)})
    return render_template("/edit.html", carros = carros)

@app.route("/atualizar_bd", methods=["POST"])
def atualiza_carro():
    id = request.form['id']
    carros = {
        "marca": request.form['marca'],
        "modelo": request.form['modelo'],
        "ano": request.form['ano'],
        "preco": request.form['preco'],
        "categoria": request.form['categoria'],
        "cambio": request.form['cambio']
    }
    collection_carros.update_one({"_id": ObjectId(id)}, {"$set": carros})

    return redirect("/listar")

@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == "GET":
        return render_template("add.html")
    else:
        # obtendo carros
        Marca = request.form['marca']
        Modelo = request.form['modelo']
        Preco = request.form['preco']
        Ano = request.form['ano']
        Categoria = request.form['categoria']
        Cambio = request.form['cambio']

        carro = {
            'marca': Marca,
            'modelo': Modelo,
            'preco': Preco,
            'ano': Ano,
            'categoria': Categoria,
            'cambio': Cambio
        }

        db.carros.insert_one(carro)

        return redirect("/listar")
    
@app.route("/<id>/excluir")
def excluir_veiculo(id):
    collection_carros.delete_one({"_id": ObjectId(id)})
 
    return redirect("/listar")
     
if __name__ == "__main__":
    app.run(port=8085, debug = True)