# Importações das bibliotecas necessárias
import re
import pandas as pd

# Regex para separar o programa em linhas
separador_de_linhas = r"^.+$"
# Regex para encontrar os itens em identificador, literal e símbolo
tokenizador = r"(\w+|\'\w+\')|(\s{4}|\s)|(\(|\)|\<|\>|\=|\:|\;|\{|\}|\[|\]|\+|\-)"
# Regex para identificar se é numero ou string (literal)
numero_ou_string = r"\d+|\'\w+\'"

# Lista de palavras chaves da linguagem
palavras_chaves = ["if", "show", "goto", "end"]

# Símbolo para determinar o fim de linha
terminador_de_linha = ";"

# Variável para guardar todas as informações do programa (entrada) por categoria
tokens = {
    'identificadores': {
        'id': [],
        'nome': []
    },
    'literais': {
        'id': [],
        'nome': []
    },
    'palavras_chaves': {
        'id': [],
        'nome': []
    },
    'terminadores': {
        'id': [],
        'nome': []
    },
    'simbolos': {
        'id': [],
        'nome': []
    },
    'espacos': {
        'id': [],
        'nome': []
    }
}

# Variável para guardar os tokens gerais em ordem do programa (entrada)
tokens_gerais = {
    'id': [],
    'tipo': [],
    'nome': []
}

# Variável para correspondência de siglas usadas para tokenização
tipos_tokens = {
    'lt': 'literal',
    'kw': 'palavra-chave',
    'id': 'identificador',
    'sp': 'espaço',
    'tb': 'tabulação',
    'ql': 'quebra-linha',
    'tr': 'terminador-linha',
    'sb': 'simbolo'
}

# Variável para guardar todas as linhas do programa (entrada)
linhas_programa = []


# Função para separar o programa (entrada) em linhas
def separar_linhas(programa):
    global separador_de_linhas
    global linhas_programa
    matches = re.finditer(separador_de_linhas, programa, re.MULTILINE)

    # Laço para percorrer o programa e guardar na variável
    for matchNum, match in enumerate(matches, start=1):
        linhas_programa.append(match.group())

    # Chamada de função para próxima etapa de análise
    tokenizar_linhas()


# Função para tokenizar os itens do programa (entrada) de maneira geral
def tokenizar_geral(tipo, conteudo):
    global tokens_gerais
    tokens_gerais['id'].append(len(tokens_gerais['id']))
    tokens_gerais['tipo'].append(tipo)
    tokens_gerais['nome'].append(conteudo)


# Função para tokenizar os itens do programa (entrada) por categoria
def tokenizar_categoria(categoria, conteudo):
    global tokens
    tokens[categoria]['id'].append(len(tokens[categoria]['id']))
    tokens[categoria]['nome'].append(conteudo)


# Função para tokenizar cada item das linhas obtidas do programa (entrada)
def tokenizar_linhas():
    global tokenizador, linhas_programa, palavras_chaves, terminador_de_linha, numero_ou_string

    # Laço para pegar cada linha da lista de linhas do programa (entrada)
    for linha in linhas_programa:
        matches = re.finditer(tokenizador, linha, re.MULTILINE)
        for matchNum, match in enumerate(matches, start=1):
            for groupNum in range(0, len(match.groups())):
                groupNum = groupNum + 1

                # Verifica a ocorrência de literais, identificadores e palavras chaves do programa (entrada)
                if groupNum == 1:
                    # Verifica se a correspondência é diferente de vazia
                    if match.group(1) != None:
                        # Verifica se a correspondência é um literal
                        if re.fullmatch(numero_ou_string, match.group(1)):
                            tokenizar_categoria('literais', match.group(1))
                            tokenizar_geral('lt', match.group(1))
                        # Verifica se a correspondência é uma palavra-chave da linguagem
                        elif match.group(1) in palavras_chaves:
                            tokenizar_categoria('palavras_chaves', match.group(1))
                            tokenizar_geral('kw', match.group(1))
                        # Caso não haja correspondência com as condições anteriores, é um identificador
                        else:
                            tokenizar_categoria('identificadores', match.group(1))
                            tokenizar_geral('id', match.group(1))

                # Verifica a ocorrência de espaços
                if groupNum == 2:
                    # Verifica se a correspondência é diferente de vazia
                    if match.group(2) != None:
                        # Verifica se é apenas um espaço em branco
                        if match.group(2) == ' ':
                            tokenizar_categoria('espacos', f"'{match.group(2)}'")
                            tokenizar_geral('sp', f"'{match.group(2)}'")

                        elif re.fullmatch(r'\s{4}', match.group(2)):
                            tokenizar_categoria('espacos', f"'{match.group(2)}'")
                            tokenizar_geral('tb', f"'{match.group(2)}'")

                # Verifica a ocorrência de terminador de linha ';' ou outros símbolos
                if groupNum == 3:
                    # Verifica se a correspondência é diferente de vazia
                     if match.group(3) != None:
                        # Verifica se a correspondência é um terminador de linha
                        if match.group(3) == terminador_de_linha:
                            tokenizar_categoria('terminadores', match.group(3))
                            tokenizar_geral('tr', match.group(3))
                        # Caso não haja correspondência com as condições anteriores, é um símbolo qualquer
                        else:
                            tokenizar_categoria('simbolos', match.group(3))
                            tokenizar_geral('sb', match.group(3))
        # Termino do laço, ou seja, adição de quebra de linha e tokenização do mesmo
        tokenizar_categoria('espacos', f'\\n')
        tokenizar_geral('ql', f'\\n')


def main():
    global tokens, tokens_gerais

    # Leitura do programa (entrada) da linguagem STM através de um arquivo .txt
    with open('programa_entrada.txt', 'r') as arquivo:
        programa = arquivo.read()
    print(f"\tPrograma de entrada:\n\n{programa}\n")
    separar_linhas(programa)

    print("\tTokens por categorias:\n")
    for i in tokens:
        print(f'{i}:', end='\n\t')
        print(f'id:\t\tnome:', end='\n\t')
        for k in range(len(tokens[i]['id'])):
            print(f'{tokens[i]['id'][k]}\t\t{tokens[i]['nome'][k]}', end='\n\t')
        print()

    print("\n\tTokens gerais:\n")
    print(f"id\t\ttipo\t\tconteudo")
    for i in range(len(tokens_gerais['id'])):
        print(f"{tokens_gerais['id'][i]}\t\t{tokens_gerais['tipo'][i]}\t\t\t{tokens_gerais['nome'][i]}")

    # Transformando os tokens para um arquivo .csv para ser usado posteriormente em análise sintática
    tokens_gerais_df = pd.DataFrame(tokens_gerais)
    tokens_gerais_df.to_csv('tokens_do_programa.csv', index=False)


if __name__ == "__main__":
    main()
