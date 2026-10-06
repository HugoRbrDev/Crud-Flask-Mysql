from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = "troque-por-uma-chave-qualquer"

# --- Configuração do banco -------------------------------------------------
DB = dict(
    host="127.0.0.1",
    user="root",
    password="",            # Homebrew: root sem senha por padrão
    database="crud_flask",
)


def query(sql, params=None, fetch=False):
    """Abre conexão, executa, fecha. fetch=True devolve as linhas."""
    conn = mysql.connector.connect(**DB)
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql, params or ())
    if fetch:
        resultado = cursor.fetchall()
    else:
        conn.commit()
        resultado = None
    cursor.close()
    conn.close()
    return resultado


# --- READ (listar) ---------------------------------------------------------
@app.get("/")
def listar():
    pessoas = query("SELECT id, nome, idade FROM pessoas ORDER BY id", fetch=True)
    return render_template("index.html", pessoas=pessoas)


# --- CREATE ----------------------------------------------------------------
@app.route("/novo", methods=["GET", "POST"])
def novo():
    if request.method == "POST":
        nome = request.form["nome"].strip()
        idade = request.form["idade"].strip()

        if not nome or not idade:
            flash("Preencha nome e idade.", "erro")
            return render_template("form.html", pessoa=None, action=url_for("novo"))

        query("INSERT INTO pessoas (nome, idade) VALUES (%s, %s)", (nome, idade))
        flash("Pessoa cadastrada com sucesso!", "ok")
        return redirect(url_for("listar"))

    return render_template("form.html", pessoa=None, action=url_for("novo"))


# --- UPDATE ----------------------------------------------------------------
@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    if request.method == "POST":
        nome = request.form["nome"].strip()
        idade = request.form["idade"].strip()
        query("UPDATE pessoas SET nome=%s, idade=%s WHERE id=%s", (nome, idade, id))
        flash("Cadastro atualizado!", "ok")
        return redirect(url_for("listar"))

    linhas = query("SELECT id, nome, idade FROM pessoas WHERE id=%s", (id,), fetch=True)
    if not linhas:
        flash("Pessoa não encontrada.", "erro")
        return redirect(url_for("listar"))

    return render_template("form.html", pessoa=linhas[0], action=url_for("editar", id=id))


# --- DELETE ----------------------------------------------------------------
@app.post("/excluir/<int:id>")
def excluir(id):
    query("DELETE FROM pessoas WHERE id=%s", (id,))
    flash("Registro excluído.", "ok")
    return redirect(url_for("listar"))


if __name__ == "__main__":
    app.run(debug=True, port=5001)