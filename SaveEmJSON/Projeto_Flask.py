from flask import Flask, render_template, request
import random
import json  # <<< 1. IMPORTADO JSON

app = Flask(__name__)


# <<< 2. CLASSE DE PERSONAGEM CRIADA >>>
# (Como o exercício pedia para criar uma "instância de objeto",
#  nós criamos esta classe para guardar os dados do personagem)
class Personagem:
    def __init__(self, nome, raca, classe, atributos, habilidades, estilo):
        self.nome = nome
        self.raca = raca
        self.classe = classe
        self.atributos = atributos
        self.habilidades = habilidades
        self.estilo_criacao = estilo


# ---------- Funções de Atributos (sem mudança) ----------
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


# ---------- Habilidades extras (sem mudança) ----------
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

        # --- IMPLEMENTAÇÃO DO EXERCÍCIO (JSON SAVE) ---
        # 1. Criar a instância do objeto
        personagem_final = Personagem(
            nome=nome,
            raca=raca_escolhida,
            classe=classe_escolhida,
            atributos=atributos,
            habilidades=habilidades,
            estilo=estilo,
        )

        # 2. Salvar a instância em JSON usando .__dict__
        # (O nome do arquivo será baseado no nome do personagem, ex: "krom_save.json")
        nome_arquivo_json = f"{nome.lower().replace(' ', '_')}_save.json"
        try:
            with open(nome_arquivo_json, "w", encoding="utf-8") as f:
                # Usamos __dict__ para converter o objeto em dicionário
                json.dump(personagem_final.__dict__, f, ensure_ascii=False, indent=4)
            print(f"Personagem '{nome}' salvo em {nome_arquivo_json}")
        except Exception as e:
            print(f"Erro ao salvar personagem: {e}")
        # --- FIM DA IMPLEMENTAÇÃO ---

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
            estilo=estilo,  # Passa o estilo adiante
            valores=valores,
            habilidades=habilidades,
        )


@app.route("/distribuir", methods=["POST"])
def distribuir():
    nome = request.form["nome"]
    classe = request.form["classe"]
    raca = request.form["raca"]
    estilo = request.form.get("estilo", "aventureiro")  # Recupera o estilo

    atributos = {
        "Força": int(request.form["forca"]),
        "Destreza": int(request.form["destreza"]),
        "Constituição": int(request.form["constituicao"]),
        "Inteligência": int(request.form["inteligencia"]),
        "Sabedoria": int(request.form["sabedoria"]),
        "Carisma": int(request.form["carisma"]),
    }

    # Gera habilidades DE NOVO aqui para garantir que temos a lista
    habilidades = gerar_habilidades(classe, raca, estilo)

    # --- IMPLEMENTAÇÃO DO EXERCÍCIO (JSON SAVE) ---
    # 1. Criar a instância do objeto com os dados finais
    personagem_final = Personagem(
        nome=nome,
        raca=raca,
        classe=classe,
        atributos=atributos,
        habilidades=habilidades,
        estilo=estilo,
    )

    # 2. Salvar a instância em JSON usando .__dict__
    nome_arquivo_json = f"{nome.lower().replace(' ', '_')}_save.json"
    try:
        with open(nome_arquivo_json, "w", encoding="utf-8") as f:
            # Usamos __dict__ para converter o objeto em dicionário
            json.dump(personagem_final.__dict__, f, ensure_ascii=False, indent=4)
        print(f"Personagem '{nome}' salvo em {nome_arquivo_json}")
    except Exception as e:
        print(f"Erro ao salvar personagem: {e}")
    # --- FIM DA IMPLEMENTAÇÃO ---

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
