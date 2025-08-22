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

    @staticmethod
    def rolar_valor_fixo():

        return [15, 14, 13, 12, 10, 8]

class Personagem:
    def __init__(self, nome, classe, atributos):
        self.nome = nome
        self.classe = classe
        self.atributos = atributos

    def exibir(self):
        print("\n=== Personagem Criado com Sucesso! ===")
        print(f"Nome: {self.nome}")
        print(f"Classe: {self.classe}")
        print("Atributos:")
        for atributo, valor in self.atributos.items():
            print(f"  {atributo}: {valor}")

class DistribuidorDeAtributos:
    atributos = ["Força", "Destreza", "Constituição",
                 "Inteligência", "Sabedoria", "Carisma"]

    @staticmethod
    def estilo_classico():
        return [RoladorDeDados.rolar_4d6_descartar_menor() for _ in range(6)]

    @staticmethod
    def estilo_aventureiro():
        return [RoladorDeDados.rolar_3d6() for _ in range(6)]

    @staticmethod
    def estilo_heroico():
        return RoladorDeDados.rolar_valor_fixo()

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

    classes = {"1": "Mago", "2": "Guerreiro", "3": "Ladrão"}
    print("\nEscolha a classe do seu personagem:")
    for chave, valor in classes.items():
        print(f"{chave}: {valor}")
    classe = classes.get(input("Digite o número da classe escolhida: "), "Inválida")

    if classe == "Inválida":
        print("Classe inválida. Reinicie o jogo.")
        return

    estilos = {"1": "Clássico", "2": "Aventureiro", "3": "Heróico"}
    print("\nEscolha o estilo de distribuição de atributos:")
    for chave, valor in estilos.items():
        print(f"{chave}: {valor}")
    escolha_estilo = input("Digite o número do estilo: ")

    if escolha_estilo == "1":
        valores = DistribuidorDeAtributos.estilo_classico()
    elif escolha_estilo == "2":
        valores = DistribuidorDeAtributos.estilo_aventureiro()
    elif escolha_estilo == "3":
        valores = DistribuidorDeAtributos.estilo_heroico()
    else:
        print("Estilo inválido. Reinicie o jogo.")
        return

    print(f"\nValores disponíveis: {valores}")
    atributos = DistribuidorDeAtributos.distribuir(valores)

    personagem = Personagem(nome, classe, atributos)
    personagem.exibir()


if __name__ == "__main__":
    main()
