from flask import Flask

app = Flask(__name__)

@app.route("/")
def homePage():
  return "<h2>Minha Pagina com Flash</h2>"

app.run()