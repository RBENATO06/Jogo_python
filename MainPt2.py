import random

class RoladorDeDados:
    @staticmethod
    def rolar_4d6_descartar_menor():
        dados = [random.randint(1, 6) for _ in range(4)]
        dados.remove(min(dados))
        return sum(dados)

    @staticmethod
    def rolar_3d6():
        return sum(random.randint(1, 6) for _ in range(3))

class Raca:
    def __init__(self, nome, movimento, infravisao, alinhamento, habilidade):
        self.nome = nome
        self.movimento = movimento
        self.infravisao = infravisao
        self.alinhamento = alinhamento
        self.habilidade = habilidade

    def exibir(self):
        return (f"Raça: {self.nome}\n"
                f"  Movimento: {self.movimento}\n"
                f"  Infravisão: {self.infravisao}\n"
                f"  Alinhamento: {self.alinhamento}\n"
                f"  Habilidade: {self.habilidade}")


class Humano(Raca):
    def __init__(self):
        super().__init__("Humano", "9m", "Nenhuma", "Qualquer",
                         "Versátil (+1 em um atributo à escolha)")


class Anao(Raca):
    def __init__(self):
        super().__init__("Anão", "6m", "18m", "Ordeiro",
                         "Resistência (+2 PV extras)")


class Elfo(Raca):
    def __init__(self):
        super().__init__("Elfo", "9m", "18m", "Caótico",
                         "Sentidos élficos (detecção de portas secretas, imunidade a sono/paralisia)")


class Halfling(Raca):
    def __init__(self):
        super().__init__("Halfling", "6m", "Nenhuma", "Ordeiro",
                         "Sortudo (pode rerrolar 1 dado ruim)")

class ClassePersonagem:
    def __init__(self, nome, habilidade_especial):
        self.nome = nome
        self.habilidade_especial = habilidade_especial

    def exibir(self):
        return f"Classe: {self.nome}\n  Habilidade: {self.habilidade_especial}"

class Mago(ClassePersonagem):
    def __init__(self):
        super().__init__("Mago", "Magia arcana (lançar feitiços)")

class Guerreiro(ClassePersonagem):
    def __init__(self):
        super().__init__("Guerreiro", "Ataque poderoso (+2 em Força)")

class Ladrao(ClassePersonagem):
    def __init__(self):
        super().__init__("Ladrão", "Furtividade (desarmar armadilhas)")

class Personagem:
    def __init__(self, nome, classe, raca, atributos):
        self.nome = nome
        self.classe = classe
        self.raca = raca
        self.atributos = atributos

    def exibir(self):
        print("\n=== Personagem Criado com Sucesso! ===")
        print(f"Nome: {self.nome}")
        print(self.classe.exibir())
        print(self.raca.exibir())
        print("Atributos:")
        for atributo, valor in self.atributos.items():
            print(f"  {atributo}: {valor}")

class DistribuidorDeAtributos:
    atributos = ["Força", "Destreza", "Constituição",
                 "Inteligência", "Sabedoria", "Carisma"]

    @staticmethod
    def estilo_classico():
        atributos_final = {}
        for atributo in DistribuidorDeAtributos.atributos:
            rolagens = [RoladorDeDados.rolar_3d6() for _ in range(3)]
            melhor = max(rolagens)
            print(f"{atributo}: rolagens {rolagens} → escolhido {melhor}")
            atributos_final[atributo] = melhor
        return atributos_final

    @staticmethod
    def estilo_aventureiro():
        return [RoladorDeDados.rolar_3d6() for _ in range(6)]

    @staticmethod
    def estilo_heroico():
        return [RoladorDeDados.rolar_4d6_descartar_menor() for _ in range(6)]

    @classmethod
    def distribuir(cls, valores):
        atributos_final = {}
        for atributo in cls.atributos:
            print(f"\nValores restantes: {valores}")
            escolha = int(input(f"Escolha um valor para {atributo}: "))
            if escolha in valores:
                atributos_final[atributo] = escolha
                valores.remove(escolha)
            else:
                print("Valor inválido, tente novamente!")
                return cls.distribuir(valores)
        return atributos_final

def main():
    print("Bem vindo ao jogo!")
    nome = input("Digite o nome do seu personagem: ")

    classes = {"1": Mago(), "2": Guerreiro(), "3": Ladrao()}
    print("\nEscolha a classe do seu personagem:")
    for chave, valor in classes.items():
        print(f"{chave}: {valor.nome}")
    classe = classes.get(input("Digite o número da classe escolhida: "), None)

    if not classe:
        print("Classe inválida. Reinicie o jogo.")
        return

    racas = {"1": Humano(), "2": Anao(), "3": Elfo(), "4": Halfling()}
    print("\nEscolha a raça do seu personagem:")
    for chave, raca in racas.items():
        print(f"{chave}: {raca.nome}")
    raca = racas.get(input("Digite o número da raça escolhida: "), None)

    if not raca:
        print("Raça inválida. Reinicie o jogo.")
        return

    estilos = {"1": "Clássico", "2": "Aventureiro", "3": "Heróico"}
    print("\nEscolha o estilo de distribuição de atributos:")
    for chave, valor in estilos.items():
        print(f"{chave}: {valor}")
    escolha_estilo = input("Digite o número do estilo: ")

    if escolha_estilo == "1":
        atributos = DistribuidorDeAtributos.estilo_classico()
    elif escolha_estilo == "2":
        valores = DistribuidorDeAtributos.estilo_aventureiro()
        print(f"\nValores disponíveis: {valores}")
        atributos = DistribuidorDeAtributos.distribuir(valores)
    elif escolha_estilo == "3":
        valores = DistribuidorDeAtributos.estilo_heroico()
        print(f"\nValores disponíveis: {valores}")
        atributos = DistribuidorDeAtributos.distribuir(valores)
    else:
        print("Estilo inválido. Reinicie o jogo.")
        return

    personagem = Personagem(nome, classe, raca, atributos)
    personagem.exibir()


if __name__ == "__main__":
    main()
