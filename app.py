# =========================================================
# app.py - Servidor Flask da Agenda de Contatos
# =========================================================

# Importações necessárias
from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os

# Cria a aplicação Flask
app = Flask(__name__)

# Chave necessária para usar "flash messages" (mensagens temporárias)
app.secret_key = "chave-secreta-da-agenda"

# Caminho completo do arquivo JSON que guardará os contatos
ARQUIVO_JSON = os.path.join(os.path.dirname(__file__), "contatos.json")


# ---------------------------------------------------------
# Funções auxiliares para ler e escrever no JSON
# ---------------------------------------------------------
def carregar_contatos():
    """Lê o arquivo JSON e devolve uma lista de contatos.
    Se o arquivo não existir ou estiver corrompido, devolve lista vazia."""
    if not os.path.exists(ARQUIVO_JSON):
        return []
    try:
        with open(ARQUIVO_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def salvar_contatos(contatos):
    """Grava a lista de contatos no arquivo JSON com formatação legível."""
    with open(ARQUIVO_JSON, "w", encoding="utf-8") as f:
        json.dump(contatos, f, indent=4, ensure_ascii=False)


# ---------------------------------------------------------
# Rota principal: mostra o formulário + lista de contatos
# ---------------------------------------------------------
@app.route("/")
def index():
    contatos = carregar_contatos()
    return render_template("index.html", contatos=contatos)


# ---------------------------------------------------------
# Rota para ADICIONAR um novo contato
# ---------------------------------------------------------
@app.route("/adicionar", methods=["POST"])
def adicionar():
    # Pega os dados do formulário e remove espaços em branco
    nome = request.form.get("nome", "").strip()
    telefone = request.form.get("telefone", "").strip()
    email = request.form.get("email", "").strip()

    # Validação: nenhum campo pode estar vazio
    if not nome or not telefone or not email:
        flash("⚠️ Preencha todos os campos antes de adicionar!", "erro")
        return redirect(url_for("index"))

    # Carrega a lista atual, adiciona o novo contato e salva
    contatos = carregar_contatos()
    novo_contato = {
        "id": len(contatos) + 1 if not contatos else max(c["id"] for c in contatos) + 1,
        "nome": nome,
        "telefone": telefone,
        "email": email,
    }
    contatos.append(novo_contato)
    salvar_contatos(contatos)

    flash("✅ Contato adicionado com sucesso!", "sucesso")
    return redirect(url_for("index"))


# ---------------------------------------------------------
# Rota para EXCLUIR um contato pelo ID
# ---------------------------------------------------------
@app.route("/excluir/<int:contato_id>", methods=["POST"])
def excluir(contato_id):
    contatos = carregar_contatos()

    # Filtra a lista, mantendo apenas os contatos com ID diferente
    nova_lista = [c for c in contatos if c["id"] != contato_id]

    # Se nada foi removido, o ID não existia
    if len(nova_lista) == len(contatos):
        flash("❌ Contato não encontrado.", "erro")
    else:
        salvar_contatos(nova_lista)
        flash("🗑️ Contato excluído com sucesso!", "sucesso")

    return redirect(url_for("index"))


# ---------------------------------------------------------
# Executa o servidor quando rodamos o arquivo diretamente
# ---------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)