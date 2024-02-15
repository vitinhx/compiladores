# Importação das bibliotecas necessárias
import pandas as pd
import re

# alterar o caminho do .csv para que funcione no seu ambiente (se necessário)
caminho = 'tokens_do_programa.csv'
programa_csv = pd.read_csv(caminho)
df = pd.DataFrame(programa_csv)

# Regex para identificar espaços
regex_espaco = r"'(\s{1,})\'"

# Regex para identificar tipos de identificadores
label = r"(\w+\-identificador):"
var_num = r"(\w+\-identificador)\=constante"
var_bool = r"(\w+\-identificador)=booleano"
var_string = r"(\w+\-identificador)=string"
regex_id = rf"{label}|{var_num}|{var_bool}|{var_string}"

# Regex para identificar expressões matemáticas
regex_exp = r"(\w+\-identificador)(?=\=(identificador-numerico|constante)\+(identificador-numerico|constante))"

tokens_especificados = {}

# Variável para guardas os tipos de dados do programa
alfabeto_programa = {
        'id': [],
        'tipo': [],
        'conteudo': []
}

# Variável para guardar o programa
programa = ""

# Função para inserir os tipos e conteudos de identificadores
def inserir_alfabeto(tipo, conteudo):
    global alfabeto_programa
    alfabeto_programa['id'].append(len(alfabeto_programa['id']))
    alfabeto_programa['tipo'].append(tipo)
    alfabeto_programa['conteudo'].append(conteudo)


# Função para identificar e categorizar os tipos de identificadores
def guardar_identificadores():
    global programa, alfabeto_programa

    matches = re.finditer(regex_id, programa, re.MULTILINE)

    for matchNum, match in enumerate(matches, start=1):
        for groupNum in range(0, len(match.groups())):
            groupNum = groupNum + 1
            if match.group(groupNum) != None:
                if groupNum == 1:
                    inserir_alfabeto('label', match.group(groupNum))
                if groupNum == 2:
                    inserir_alfabeto('identificador-numerico', match.group(groupNum))
                if groupNum == 3:
                    inserir_alfabeto('identificador-booleano', match.group(groupNum))
                if groupNum == 4:
                    inserir_alfabeto('string', match.group(groupNum))


# Função que identifica e substitue tipos de identificadores numericos, booleanos ou string
def substituir_identificadores():
    global programa

    for id, tipo, conteudo in zip(alfabeto_programa['id'],alfabeto_programa['tipo'], alfabeto_programa['conteudo']):
        programa = re.sub(conteudo, tipo,
                                     programa, 0, re.MULTILINE)


# Função para identificar expressão matemática
def identificar_expressao():
    global programa

    matches = re.finditer(regex_exp, programa, re.MULTILINE)

    for matchNum, match in enumerate(matches, start=1):
        for groupNum in range(0, len(match.groups())):
            groupNum = groupNum + 1
            if match.group(groupNum) != None:
                if groupNum == 1:
                    inserir_alfabeto('identificador-numerico', match.group(1))


# Função para identificar padrões de tokens e substituir
def substituir_tokens():
    global alfabeto_programa, programa

    # chamada de função para categorizar os identificadores
    guardar_identificadores()

    # identifica e substitue idenditificador para 'label'
    programa = re.sub(r"(\w+\-identificador)(?=\:)", "label",
                                 programa, 0, re.MULTILINE)

    # identifica e substitue para idenditificador
    programa = re.sub(r"(\w+\-identificador)(?=\:)", "identificador",
                                 programa, 0, re.MULTILINE)

    # chamada de função para substituir tipos de identificadores numericos, booleanos ou string
    substituir_identificadores()

    # chamada de função que identifica expressões matemáticas
    identificar_expressao()

    # chamada de função para incluir identificadores numericos após de identificar expressões matemáticas
    substituir_identificadores()

    # substituição de identificador na ocorrência de atribuição de valor
    programa = re.sub(r"(?<!if\()(identificador-\w+|string)(?=\=)", "identificador",
                                 programa, 0, re.MULTILINE)

    # exclusão do simbolo $ no final do programa para ser aceito no autômato
    programa = re.sub(r"\$$", "", programa, 0, re.MULTILINE)


# Função para especificar os tokens a nível de tipos de dados para programação
def especificar_tokens():
    global df, regex_espaco, tokens_especificados, programa
    tokens_especificados = df

    for id, tipo, conteudo in zip(tokens_especificados['id'], tokens_especificados['tipo'],
                                  tokens_especificados['nome']):
        if tipo != 'sp':
            if tipo == 'lt':
                if re.fullmatch(r'\d+', conteudo):
                    programa = programa + "constante"
                elif re.fullmatch(r'\'\w+\'', conteudo):
                    programa = programa + "string"
                elif re.fullmatch(r'true|false', conteudo):
                    programa = programa + "booleano"
                else:
                    programa = programa + conteudo
            elif tipo == 'sb' or tipo == 'tr':
                if re.fullmatch(r'and|or|xor|not|\=\=|\!\=|\<\=|\<|\>\=|\>', conteudo):
                    programa = programa + conteudo
                elif re.fullmatch(r'\+|\-|\*|\^|\/', conteudo):
                    programa = programa + conteudo
                elif re.fullmatch(r'\=|\{|\}|\(|\)|\;|\:', conteudo):
                    programa = programa + conteudo
                else:
                    print("Conteudo inválido: ", conteudo)
            elif tipo == 'id':
                programa = programa + conteudo + "-" + "identificador"
            elif tipo == 'kw':
                programa = programa + conteudo

            elif tipo == 'ql':
                programa = programa + conteudo

    # substituição de '\n' para $
    programa = re.sub(r"\\n", "$", programa, 0, re.MULTILINE)

    substituir_tokens()


# Função main do programa do gerador de código
def main():
    global programa

    especificar_tokens()

    print(f"\t\tPrograma intermediário gerado:\n\t"
          f"Copie o conteudo gerado abaixo na entrada do Jflap:\n"
          f"{programa}")

    # criação de um arquivo .txt para ser usado no Jflap
    with open("programa_intermediario.txt", 'w') as arquivo:
        arquivo.write(programa)


if __name__ == "__main__":
    main()
