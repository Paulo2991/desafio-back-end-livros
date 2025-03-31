from flask import Flask,request,jsonify,render_template
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def init_db():
  with sqlite3.connect('database.db') as conn:
    conn.execute(""" CREATE TABLE IF NOT EXISTS livros(
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 titulo TEXT NOT NULL,
                 categoria TEXT NOT NULL,
                 autor TEXT NOT NULL,
                 imagem_url TEXT NOT NULL
                 )""")
    print("Banco de dados criado!")

init_db()

@app.route("/")
def homePage():
  return render_template("index.html")

@app.route('/doar', methods=['POST'])
def doar():
  dados = request.get_json()

  titulo = dados.get('titulo')
  categoria = dados.get('categoria')
  autor = dados.get('autor')
  imagem_url = dados.get('imagem_url')

  if not titulo or not categoria or not autor or not imagem_url:
    return jsonify({"erro":"Todos os campos são obrigatorios"}),400
  
  with sqlite3.connect('database.db') as conn:
    conn.execute(f""" INSERT INTO livros(titulo,categoria,autor,imagem_url) 
                 VALUES (?,?,?,?)""", (titulo,categoria,autor,imagem_url))

    conn.commit()

    return jsonify({"mensagem":"Livros cadastrados com sucesso"}, 201)
  
@app.route("/listar",methods=["GET"])
def listarLivros():
  with sqlite3.connect('database.db') as conn:
    livros = conn.execute("SELECT * FROM livros").fetchall()
  livrosAdicionados = []

  for livro in livros:
    dicionarioLivros = {
      "id":livro[0],
      "titulo":livro[1],
      "categoria":livro[2],
      "autor":livro[3],
      "imagem_url":livro[4],
    }
    livrosAdicionados.append(dicionarioLivros)
  
  return jsonify(livrosAdicionados)


if __name__ == '__main__':
  app.run(debug=True)