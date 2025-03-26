from flask import Flask, request, jsonify
from flask_cors import CORS

import sqlite3

app = Flask(__name__)
CORS(app)




# route -->

@app.route("/")
def messagem_personalizada():
    
    return "<h1>API de Livros Vai na Web criada com sucesso Obrigado Professor João Pedro Belo pelo excelente curso!!!</h1>"


@app.route("/pague")
def pagar_pessoas():

    return "<h1>Começar a semana, pagando suas dívidas, é bom demais!!!</h1>"


@app.route("/pix")
def mande_o_pix():
    return "<h3>Pagar as pessoas faz bem pras pessoas!!!</h3>"


@app.route("/comidas")
def feijoada():
    return "<h3>Feijoada com bacon e linguiça!!!</h3>"


def init_db():

    with sqlite3.connect("database.db") as conn:
        conn.execute(
            """
        CREATE TABLE IF NOT EXISTS LIVROS(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            categoria TEXT NOT NULL,
            autor TEXT NOT NULL,
            imagem_url TEXT NOT NULL
        )
        """
        )


init_db()


@app.route("/doar", methods=["POST"])
def doar():

    dados = request.get_json()

    titulo = dados.get("titulo")
    categoria = dados.get("categoria")
    autor = dados.get("autor")
    image_url = dados.get("image_url")

    if not titulo or not categoria or not autor or not image_url:
        return jsonify({"erro": "Todos os campos são obrigatórios"}), 400

    with sqlite3.connect("database.db") as conn:
        conn.execute(f"""
        INSERT INTO LIVROS (titulo, categoria, autor, imagem_url)
        VALUES ("{titulo}", "{categoria}", "{autor}", "{image_url}")
        """)

        conn.commit()
        return jsonify({"message": "Livro cadastrado com sucesso"}), 201


@app.route("/livros", methods=["GET"])
def listar_livros():

    with sqlite3.connect("database.db") as conn:
        livros = conn.execute("SELECT * FROM LIVROS").fetchall()

    livros_formatados = []

    for item in livros:
            dicionario_livros = {
                "id": item[0],
                "titulo": item[1],
                "categoria": item[2],
                "autor": item[3],
                "image_url": item[4]
            }
            livros_formatados.append(dicionario_livros)

    return jsonify(livros_formatados)


if __name__ == "__main__":

    app.run(debug=True)
