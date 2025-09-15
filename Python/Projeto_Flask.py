from flask import Flask, render_template, request
import random

app = Flask(__name__)



def rolar_dado(qtd, lados=6):
    return [random.randint(1, lados) for _ in range(qtd)]


def classico():
    atributos = {}
    for atributo in [
        "Força",
        "Destreza",
        "Constituição",
        "Inteligência",
        "Sabedoria",
        "Carisma",
    ]:
        rolagens = rolar_dado(3)
        atributos[atributo] = sum(rolagens)
    return atributos


def aventureiro():
    valores = []
    for _ in range(6):
        rolagens = rolar_dado(3)
        valores.append(sum(rolagens))
    return valores

 
def heroico():
    valores = []
    for _ in range(6):
        rolagens = rolar_dado(4)
        rolagens.remove(min(rolagens))
        valores.append(sum(rolagens))
    return valores


# ---------- Habilidades extras ----------
def gerar_habilidades(classe, raca, estilo):
    habilidades = []

    # Base de cada classe
    if classe == "Mago":
        habilidades.extend(["Bola de Fogo", "Escudo Arcano"])
    elif classe == "Guerreiro":
        habilidades.extend(["Golpe Poderoso", "Resistência de Ferro"])
    elif classe == "Ladrão":
        habilidades.extend(["Ataque Furtivo", "Evasão Rápida"])

    # Base de cada raça
    if raca == "Humano":
        habilidades.append("Versatilidade Humana")
    elif raca == "Anão":
        habilidades.append("Resistência de Pedra")
    elif raca == "Elfo":
        habilidades.append("Visão Aguçada")

    # Combinação classe + raça
    combinacoes = {
        ("Mago", "Humano"): "Sabedoria Ancestral",
        ("Mago", "Anão"): "Runas Rúnicas",
        ("Mago", "Elfo"): "Magia Natural",
        ("Guerreiro", "Humano"): "Liderança em Batalha",
        ("Guerreiro", "Anão"): "Fúria da Montanha",
        ("Guerreiro", "Elfo"): "Espada Elegante",
        ("Ladrão", "Humano"): "Astúcia Urbana",
        ("Ladrão", "Anão"): "Mãos Rápidas",
        ("Ladrão", "Elfo"): "Sombra da Floresta",
    }

    habilidade_extra = combinacoes.get((classe, raca))
    if habilidade_extra:
        habilidades.append(habilidade_extra)

    # Estilo
    if estilo == "classico":
        habilidades.append("Equilíbrio dos Antigos")
    elif estilo == "aventureiro":
        habilidades.append("Exploração Sem Medo")
    elif estilo == "heroico":
        habilidades.append("Coragem Heroica")

    return habilidades


# ---------- Rotas ----------
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/criar_personagem", methods=["POST"])
def criar_personagem():
    nome = request.form["nome"]
    classe_escolhida = request.form["classe"]
    raca_escolhida = request.form["raca"]
    estilo = request.form["estilo"]

    habilidades = gerar_habilidades(classe_escolhida, raca_escolhida, estilo)

    if estilo == "classico":
        atributos = classico()
        return render_template(
            "resultado.html",
            nome=nome,
            classe=classe_escolhida,
            raca=raca_escolhida,
            atributos=atributos,
            habilidades=habilidades,
        )

    elif estilo in ["aventureiro", "heroico"]:
        valores = aventureiro() if estilo == "aventureiro" else heroico()
        return render_template(
            "distribuir.html",
            nome=nome,
            classe=classe_escolhida,
            raca=raca_escolhida,
            valores=valores,
            habilidades=habilidades,
        )


@app.route("/distribuir", methods=["POST"])
def distribuir():
    nome = request.form["nome"]
    classe = request.form["classe"]
    raca = request.form["raca"]
    estilo = request.form.get("estilo", "aventureiro")  # garante que não perca o estilo

    atributos = {
        "Força": int(request.form["forca"]),
        "Destreza": int(request.form["destreza"]),
        "Constituição": int(request.form["constituicao"]),
        "Inteligência": int(request.form["inteligencia"]),
        "Sabedoria": int(request.form["sabedoria"]),
        "Carisma": int(request.form["carisma"]),
    }

    habilidades = gerar_habilidades(classe, raca, estilo)

    return render_template(
        "resultado.html",
        nome=nome,
        classe=classe,
        raca=raca,
        atributos=atributos,
        habilidades=habilidades,
    )


if __name__ == "__main__":
    app.run(debug=True)
