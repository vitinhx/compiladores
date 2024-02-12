# Importações das bibliotecas necessárias
import re
import pandas as pd

# Regex para separar o programa em linhas
separador_de_linhas = r"^.+$"
# Regex para encontrar os itens em identificador, literal e símbolo
tokenizador = r"(\(|\)|\<\=|\<|\>\=|\>|\={2}|\!\=|\=|\:|\;|\{|\}|\[|\]|\+|\-|and|or|xor|not)|(\w+|\'\w+\')|(\s{4}|\s)"
# Regex para identificar se é numero, booleano ou string (literal)
literal = r"\d+|\'\w+\'|true|false"

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
    global tokenizador, linhas_programa, palavras_chaves, terminador_de_linha, literal

    # Laço para pegar cada linha da lista de linhas do programa (entrada)
    for linha in linhas_programa:
        matches = re.finditer(tokenizador, linha, re.MULTILINE)
        for matchNum, match in enumerate(matches, start=1):
            for groupNum in range(0, len(match.groups())):
                groupNum = groupNum + 1

                # Verifica a ocorrência de literais, identificadores e palavras chaves do programa (entrada)
                if groupNum == 2:
                    # Verifica se a correspondência é diferente de vazia
                    if match.group(2) != None:
                        # Verifica se a correspondência é um literal
                        if re.fullmatch(literal, match.group(2)):
                            tokenizar_categoria('literais', match.group(2))
                            tokenizar_geral('lt', match.group(2))
                        # Verifica se a correspondência é uma palavra-chave da linguagem
                        elif match.group(2) in palavras_chaves:
                            tokenizar_categoria('palavras_chaves', match.group(2))
                            tokenizar_geral('kw', match.group(2))
                        # Caso não haja correspondência com as condições anteriores, é um identificador
                        else:
                            tokenizar_categoria('identificadores', match.group(2))
                            tokenizar_geral('id', match.group(2))

                # Verifica a ocorrência de espaços
                if groupNum == 3:
                    # Verifica se a correspondência é diferente de vazia
                    if match.group(3) != None:
                        # Verifica se é apenas um espaço em branco
                        if match.group(3) == ' ':
                            tokenizar_categoria('espacos', f"'{match.group(3)}'")
                            tokenizar_geral('sp', f"'{match.group(3)}'")

                        elif re.fullmatch(r'\s{4}', match.group(3)):
                            tokenizar_categoria('espacos', f"'{match.group(3)}'")
                            tokenizar_geral('tb', f"'{match.group(3)}'")

                # Verifica a ocorrência de terminador de linha ';' ou outros símbolos
                if groupNum == 1:
                    # Verifica se a correspondência é diferente de vazia
                     if match.group(1) != None:
                        # Verifica se a correspondência é um terminador de linha
                        if match.group(1) == terminador_de_linha:
                            tokenizar_categoria('terminadores', match.group(1))
                            tokenizar_geral('tr', match.group(1))
                        # Caso não haja correspondência com as condições anteriores, é um símbolo qualquer
                        else:
                            tokenizar_categoria('simbolos', match.group(1))
                            tokenizar_geral('sb', match.group(1))
        # Termino do laço, ou seja, adição de quebra de linha e tokenização do mesmo
        tokenizar_categoria('espacos', f'\\n')
        tokenizar_geral('ql', f'\\n')


# Função para mostrar tokens por categoria do programa (entrada)
def mostrar_token_categoria():
    global tokens
    print("\tTokens por categorias:\n")
    for i in tokens:
        print(f'{i}:', end='\n\t')
        print(f'id:\t\tnome:', end='\n\t')
        for k in range(len(tokens[i]['id'])):
            print(f'{tokens[i]['id'][k]}\t\t{tokens[i]['nome'][k]}', end='\n\t')
        print()
    print()


# Função para mostrar tokens gerais do programa (entrada)
def mostrar_token_geral():
    global tokens_gerais
    print("\n\tTokens gerais:\n")
    print(f"id\t\ttipo\t\tconteudo")
    for i in range(len(tokens_gerais['id'])):
        print(f"{tokens_gerais['id'][i]}\t\t{tokens_gerais['tipo'][i]}\t\t\t{tokens_gerais['nome'][i]}")
    print()


# Função para mostrar o conteudo e tokens por linhas do programa (entrada)
def mostrar_token_linha():
    global tokens_gerais
    print("\n\tPrograma tokenizado:")
    lim, it, line = 0, 0, 0
    for i, j in zip(tokens_gerais['nome'], range(len(tokens_gerais['nome']))):
        if lim == 0:
            print(f"\n\tLinha {line + 1}:")
            print(f"original:\n{linhas_programa[line]}\n\ntokenizado:")
            line += 1
        print(f'{i:<15}', end='')
        lim = lim + 1
        if i == "\\n":
            print()
            for k in range(3):
                for l in range(lim):
                    if k == 0:
                        print(f"{'^':<15}", end='')
                    elif k == 1:
                        print(f"{'|':<15}", end='')
                    elif k == 2:
                        print(f"{(tokens_gerais['id'][it], tokens_gerais['tipo'][it])}", end=f'{"":<5}')
                        it = it + 1
                print()
            lim = 0
    print()


#Função para mostrar informações gerais do programa (entrada)
def mostrar_informacoes():
    global tokens_gerais
    df = pd.DataFrame(tokens_gerais)
    print(f"\n\tInformações gerais do programa (entrada)\n\n"
          f"Quantidades de tokens: {len(df.index)}")
    for tipo in tipos_tokens:
        print(f"Quantidades de {tipos_tokens[tipo]} ({tipo}): {df['tipo'].value_counts()[tipo]}")
    print()


# fazer uma função para mostrar a estruturas disponíveis da linguagem STM
def mostrar_estrutura_stm():
    print(f"\n\tEstrutura básica da linguagem STM 0.2\n\n"
          "desvio condicional:\n"
          "if(<exp_rl>){\n\t<cmd>;\n};\n\n"
          "desvio incondicional:\n"
          "<label>:\n\t<cmd>;\n\n"
          "comandos:\n"
          "<cmd>[;]\n\tshow(<string> | <exp_m> | id)\n\tgoto(<label>)\n\tend\n\t<exp_m>\n\n"
          "expressão relacional:\n"
          "<exp_rl>\n\t[const | id][== | != | < | > | and | or | not | xor][const | id]\n\n"
          "expressão matemática:\n"
          "<exp_m>\n\tid = [const | id][+ | - | * | / | ^][const | id]\n\n")


# Função para mostrar as siglas dos tokens
def mostrar_siglas():
    global tipos_tokens
    print("\n\tSiglas usadas para atribuir aos tokens:\n")
    for id, (tipo, valor) in enumerate(tipos_tokens.items(), start=1):
        print(f"{id}:\t{tipo} -> {valor}")
    print()



def main():
    global tokens_gerais

    # Leitura do programa (entrada) da linguagem STM através de um arquivo .txt
    with open('programa_entrada.txt', 'r') as arquivo:
        programa = arquivo.read()
    separar_linhas(programa)

    # Leitura de opções
    escolha = 1
    while escolha != 0:
        print("Opções:\n\t"
              "1 -> Mostrar o programa\n\t"
              "2 -> Mostrar informações gerais\n\t"
              "3 -> Mostrar as siglas dos tokens\n\t"
              "4 -> Mostrar a estrutura básica da linguagem STM 0.2\n\t"
              "5 -> Mostrar os tokens por categoria\n\t"
              "6 -> Mostrar os tokens gerais\n\t"
              "7 -> Mostrar o programa original e tokenizado por linha\n\t"
              "0 -> Parar a execução\n")
        escolha = int(input("Digite sua opção: "))
        while escolha < 0 or escolha > 7:
            print("Opção inválida, digite uma opção válida!")
            escolha = int(input("Digite sua opção: "))
        if escolha == 1:
            print(f"\n\tPrograma de entrada:\n\n{programa}\n\n")
        elif escolha == 2:
            mostrar_informacoes()
        elif escolha == 3:
            mostrar_siglas()
        elif escolha == 4:
            mostrar_estrutura_stm()
        elif escolha == 5:
            mostrar_token_categoria()
        elif escolha == 6:
            mostrar_token_geral()
        elif escolha == 7:
            mostrar_token_linha()

    # Transformando os tokens para um arquivo .csv para ser usado posteriormente em análise sintática
    tokens_gerais_df = pd.DataFrame(tokens_gerais)
    tokens_gerais_df.to_csv('tokens_do_programa.csv', index=False)


if __name__ == "__main__":
    main()
