
import nltk
from typing import List


class CorretorOrtografico():
    def __init__(self):

        # Abrindo o arquivo txt onde contém o corpus e armazenando o seu conteúdo em uma variável
        with open(r'treinamento.txt', 'r') as f:
            treinamento = f.read()

        self.treinamento = treinamento

        # Variável que irá conter as palavras que o corretor irá se basear para a correção
        self.vocabulario: List[str] = []

        # Letras utilizado para corrigir as palavras
        self.letras = 'abcedfghijklmnopqrstuvwxyz'

        # baixando pacote punkt para realizar a tokenização das palavras
        nltk.download('punkt')

    def configurar_corretor(self):
        # Transformar as palavras do txt em tokens com nltk (palavras separadas)
        tokens = nltk.tokenize.word_tokenize(self.treinamento)

        # Chamando a função separa_palavras para remover os caracteres especiais e manter apenas as palavras
        lista_palavras = self.__separa_palavras(tokens)

        # A função normalizar irá padronizar as palavras deixando todas em minisculo.
        # Isso facilita o trabalho do corretor.
        lista_normalizada = self.__normalizar(lista_palavras)

        self.vocabulario = lista_normalizada


    def corrigir(self, palavra_errada: str):

        correta = ''

        candidatos: List[str] = []

        # todas as palavras geradas pelo gerador de palavras são candidatas à serem a correta
        palavras_geradas = self.__gerador_palavras(palavra_errada)

        # Chamando a função gerador_inception() e armazenando o seu retorno
        # em uma variável
        palavras_inception = self.__gerador_inception(palavras_geradas)

        todas_palavras = set(palavras_inception + palavras_geradas)

        for palavra in todas_palavras:
            if(palavra in self.vocabulario):
                candidatos.append(palavra)

        # percorre a lista e candidatos e escolhe aquela que estiver contida no self.vocabulario do corretor
        for candidato in candidatos:
            if(candidato in self.vocabulario):
                correta = candidato
                break

        return correta

    def __separa_palavras(self, tokens) -> list[str]:

        # lista que irá conter as palavras separadas dos caracteres especiais
        somente_palavras: List[str] = []

        # Iterando por toda a lista de tokens
        for token in tokens:

            # Separando as palavras dos caracteres especiais com tamanho maior que 1
            if token.isalpha() and len(token) != 1:

                # Armazenando somente as palavras
                somente_palavras.append(token)

        # Retornando uma lista somente com as palavras
        return somente_palavras

    def __normalizar(self, lista_palavras: list[str]) -> list[str]:

        palavras_normalizadas: List[str] = []

        for palavra in lista_palavras:
            palavras_normalizadas.append(palavra.lower())

        return palavras_normalizadas

    # Recebe uma lista de tuplas (esquerdo, direito) que corresponde aos lados
        # esquerdo e direito da palavra fatiada em dois

    def __insere_letras(self, fatias: list[tuple[str, str]]) -> list[str]:

        # Criando uma lista vazia para armazenar as palavras corrigidas
        novas_palavras: List[str] = []

        # Iterando por todas as tuplas da lista recebida
        for esquerdo, direito in fatias:

            # Iterando por toda letra da variável self.vocabulario
            for letra in self.letras:

                # Acrescentando todas as possibilidades de palavras possíveis
                novas_palavras.append(esquerdo + letra + direito)

        # Retornando uma lista de possíveis palavras
        return novas_palavras

    # Deleta letra a mais

    def __deletando_caracter(self, fatias: list[tuple[str, str]]) -> list[str]:

        novas_palavras: List[str] = []

        # Iterando por todas as tuplas da lista recebida
        for esquerdo, direito in fatias:

            # Acrescentando todas as possibilidades de palavras possíveis
            # Remove a primeira letra da fatia da direita, onde está o erro.
            novas_palavras.append(esquerdo + direito[1:])

        return novas_palavras

    # Troca caracter digitado errado

    def __troca_caracter(self, fatias: list[tuple[str, str]]) -> list[str]:

        novas_palavras: List[str] = []

        # Iterando por todas as tuplas da lista recebida
        for esquerdo, direito in fatias:

            # Iterando por toda letra das variável self.vocabulario
            for letra in self.letras:

                # Acrescentando todas as possibilidades de palavras possíveis
                # Substitui a primeira letra da fatia da direita
                novas_palavras.append(esquerdo + letra + direito[1:])

        return novas_palavras

    # Inverte caracteres que foram digitados errados

    def __invertendo_caracter(self, fatias: list[tuple[str, str]]) -> list[str]:

        novas_palavras: List[str] = []

        # Iterando por todas as tuplas da lista recebida
        for esquerdo, direito in fatias:

            # Selecionando apenas as fatias da direita que têm mais de uma letra,
            # pois, se não, não há o que inverter
            if len(direito) > 1:

                # Acrescentando todas as possibilidades de palavras possíveis
                # inverte o primeiro caracter da direita com o segundo
                novas_palavras.append(
                    esquerdo + direito[1] + direito[0] + direito[2:])

        # Retornando uma lista de possíveis palavras
        return novas_palavras

    def __gerador_palavras(self, palavra: str) -> list[str]:

        # Criando uma lista vazia para armazenar as duas fatias de cada palavra
        fatias: List[str] = []

        # Iterando por cada letra de cada palavra
        for i in range(len(palavra) + 1):

            # Armazenando as duas fatias em uma tupla e essa tupla em uma lista
            fatias.append((palavra[:i], palavra[i:]))

        palavras_geradas = self.__insere_letras(fatias)

        palavras_geradas += self.__deletando_caracter(fatias)

        palavras_geradas += self.__troca_caracter(fatias)

        palavras_geradas += self.__invertendo_caracter(fatias)

        # Retornando a lista de possíveis palavras. A palavra correta estará aí no meio
        return palavras_geradas

    def __gerador_inception(self, palavras_geradas: list[str]) -> List[str]:

        # Criando uma nova lista para armazenar as novas palavras
        novas_palavras: List[str] = []

        # Iterando em cada palavra da lista recebida
        for palavra in palavras_geradas:

            # Chamando a função self.__gerador_palavras() para realizar correções nas correções
            # reparando palavras com erros de 2 letras de distância
            novas_palavras += self.__gerador_palavras(palavra)

        # Retornando as novas palavras
        return novas_palavras
