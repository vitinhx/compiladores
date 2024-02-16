# Avaliação 1 (Individual)
Esta pasta é dedicada para a avaliação 1 da disciplina contendo 1 artefato como solicitado.

## Discente:

  - Victor Ivan Silva Silveira


## Analisador léxico para linguagem STM v0.2:

Programa em python que por meio de uso de expressões regulares, que tem como entrada um arquivo .txt renomeado por
'programa_entrada.txt', tokeniza os itens do programa e no final de sua execução é gerado um arquivo .csv, 
renomeado por 'tokens_do_programa.csv', para ser usada na etapa seguinte (Análise Sintática).


## Estrutura básica da linguagem STM v0.2:

```c
// Desvio condicional:
    if(<exp_rl>){
        <cmd>;
    };

// Desvio incondicional:
    <label>:
        <cmd>;

// Comandos:
    <cmd>[;]
        show(<string> | <exp_m> | id)
        goto(<label>)
        end
        <exp_m>

// Expressão relacional:
    <exp_rl>
        [const | id][== | != | <= | < | >= | > | and | or | not | xor][const | id]

// Expressão matemática:
    <exp_m>
        id = [const | id][+ | - | * | / | ^][const | id]
```

## Etapas para executar o programa:

1. Certificar-se de que a versão do Python instalada é a versão 3.12 ou superior
   - No Windows: ```python -m pip install –upgrade python```
   - No MacOS ou Linux: `pip install –upgrade python`

2. Verificar se a versão da biblioteca pandas está atualizada
   - `pip install pandas`

3. Atualizar a biblioteca PyArrow para evitar warnings
   - `pip install pyarrow`

4. Caso queira escrever outro programa, edite o arquivo `.txt` nomeado por `programa_entrada.txt` [localizado aqui](https://github.com/vitinhx/compiladores/blob/main/avaliacao_1/entrada/programa_entrada.txt).

5. Depois de editar o arquivo `.txt`, salve-o e execute o programa (`analisador_lexico_stm.py`) [localizado aqui](https://github.com/vitinhx/compiladores/blob/main/avaliacao_1/programa/analisador_lexico_stm.py).

## Exemplo da execução do analisador léxico:

1. Programa (Linguagem STM 0.2) exemplo escrito e salvo no arquivo .txt:

```
inicio:
    a = 30;
    b = 'teste';
    if(a > 10){
    	show(b);
    };

    c = true;
    d = false;
    if(c or d){
        show(a);
    };

    e = 'victor';
    show(e);

    f = 20;
    g = f + a;
    if(g == 50){
        goto(fim);
    };
    goto(inicio);

fim:
    end;
```

2. Executo o programa ‘analisador_lexico_stm.py’ e, no seu funcionamento, é disponibilizado um menu com várias opções, dentre elas:
```
   "1 -> Mostrar o programa"
   "2 -> Mostrar informações gerais"
   "3 -> Mostrar as siglas dos tokens"
   "4 -> Mostrar a estrutura básica da linguagem STM 0.2"
   "5 -> Mostrar os tokens por categoria"
   "6 -> Mostrar os tokens gerais"
   "7 -> Mostrar o programa original e tokenizado por linha"
   "0 -> Parar a execução"
```
3. Exemplo da tokenização feita pelo programa ao escolher a opção ‘7’ do programa:
```
Programa tokenizado:

	Linha 1:
original:
inicio:

tokenizado:
inicio         :              \n             
^              ^              ^              
|              |              |              
(0, 'id')    (1, 'sb')    (2, 'ql')    

	Linha 2:
original:
    a = 30;

tokenizado:
'    '         a              ' '            =              ' '            30             ;              \n             
^              ^              ^              ^              ^              ^              ^              ^              
|              |              |              |              |              |              |              |              
(3, 'tb')    (4, 'id')    (5, 'sp')    (6, 'sb')    (7, 'sp')    (8, 'lt')    (9, 'tr')    (10, 'ql')    

	Linha 3:
original:
    b = 'teste';

tokenizado:
'    '         b              ' '            =              ' '            'teste'        ;              \n             
^              ^              ^              ^              ^              ^              ^              ^              
|              |              |              |              |              |              |              |              
(11, 'tb')    (12, 'id')    (13, 'sp')    (14, 'sb')    (15, 'sp')    (16, 'lt')    (17, 'tr')    (18, 'ql')    

	Linha 4:
original:
    if(a > 10){

tokenizado:
'    '         if             (              a              ' '            >              ' '            10             )              {              \n             
^              ^              ^              ^              ^              ^              ^              ^              ^              ^              ^              
|              |              |              |              |              |              |              |              |              |              |              
(19, 'tb')    (20, 'kw')    (21, 'sb')    (22, 'id')    (23, 'sp')    (24, 'sb')    (25, 'sp')    (26, 'lt')    (27, 'sb')    (28, 'sb')    (29, 'ql')    

	Linha 5:
original:
    	show(b);

tokenizado:
'    '         show           (              b              )              ;              \n             
^              ^              ^              ^              ^              ^              ^              
|              |              |              |              |              |              |              
(30, 'tb')    (31, 'kw')    (32, 'sb')    (33, 'id')    (34, 'sb')    (35, 'tr')    (36, 'ql')    

	Linha 6:
original:
    };

tokenizado:
'    '         }              ;              \n             
^              ^              ^              ^              
|              |              |              |              
(37, 'tb')    (38, 'sb')    (39, 'tr')    (40, 'ql')    

	Linha 7:
original:
    c = true;

tokenizado:
'    '         c              ' '            =              ' '            true           ;              \n             
^              ^              ^              ^              ^              ^              ^              ^              
|              |              |              |              |              |              |              |              
(41, 'tb')    (42, 'id')    (43, 'sp')    (44, 'sb')    (45, 'sp')    (46, 'lt')    (47, 'tr')    (48, 'ql')    

	Linha 8:
original:
    d = false;

tokenizado:
'    '         d              ' '            =              ' '            false          ;              \n             
^              ^              ^              ^              ^              ^              ^              ^              
|              |              |              |              |              |              |              |              
(49, 'tb')    (50, 'id')    (51, 'sp')    (52, 'sb')    (53, 'sp')    (54, 'lt')    (55, 'tr')    (56, 'ql')    

	Linha 9:
original:
    if(c or d){

tokenizado:
'    '         if             (              c              ' '            or             ' '            d              )              {              \n             
^              ^              ^              ^              ^              ^              ^              ^              ^              ^              ^              
|              |              |              |              |              |              |              |              |              |              |              
(57, 'tb')    (58, 'kw')    (59, 'sb')    (60, 'id')    (61, 'sp')    (62, 'sb')    (63, 'sp')    (64, 'id')    (65, 'sb')    (66, 'sb')    (67, 'ql')    

	Linha 10:
original:
        show(a);

tokenizado:
'    '         '    '         show           (              a              )              ;              \n             
^              ^              ^              ^              ^              ^              ^              ^              
|              |              |              |              |              |              |              |              
(68, 'tb')    (69, 'tb')    (70, 'kw')    (71, 'sb')    (72, 'id')    (73, 'sb')    (74, 'tr')    (75, 'ql')    

	Linha 11:
original:
    };

tokenizado:
'    '         }              ;              \n             
^              ^              ^              ^              
|              |              |              |              
(76, 'tb')    (77, 'sb')    (78, 'tr')    (79, 'ql')    

	Linha 12:
original:
    e = 'victor';

tokenizado:
'    '         e              ' '            =              ' '            'victor'       ;              \n             
^              ^              ^              ^              ^              ^              ^              ^              
|              |              |              |              |              |              |              |              
(80, 'tb')    (81, 'id')    (82, 'sp')    (83, 'sb')    (84, 'sp')    (85, 'lt')    (86, 'tr')    (87, 'ql')    

	Linha 13:
original:
    show(e);

tokenizado:
'    '         show           (              e              )              ;              \n             
^              ^              ^              ^              ^              ^              ^              
|              |              |              |              |              |              |              
(88, 'tb')    (89, 'kw')    (90, 'sb')    (91, 'id')    (92, 'sb')    (93, 'tr')    (94, 'ql')    

	Linha 14:
original:
    f = 20;

tokenizado:
'    '         f              ' '            =              ' '            20             ;              \n             
^              ^              ^              ^              ^              ^              ^              ^              
|              |              |              |              |              |              |              |              
(95, 'tb')    (96, 'id')    (97, 'sp')    (98, 'sb')    (99, 'sp')    (100, 'lt')    (101, 'tr')    (102, 'ql')    

	Linha 15:
original:
    g = f + a;

tokenizado:
'    '         g              ' '            =              ' '            f              ' '            +              ' '            a              ;              \n             
^              ^              ^              ^              ^              ^              ^              ^              ^              ^              ^              ^              
|              |              |              |              |              |              |              |              |              |              |              |              
(103, 'tb')    (104, 'id')    (105, 'sp')    (106, 'sb')    (107, 'sp')    (108, 'id')    (109, 'sp')    (110, 'sb')    (111, 'sp')    (112, 'id')    (113, 'tr')    (114, 'ql')    

	Linha 16:
original:
    if(g == 50){

tokenizado:
'    '         if             (              g              ' '            ==             ' '            50             )              {              \n             
^              ^              ^              ^              ^              ^              ^              ^              ^              ^              ^              
|              |              |              |              |              |              |              |              |              |              |              
(115, 'tb')    (116, 'kw')    (117, 'sb')    (118, 'id')    (119, 'sp')    (120, 'sb')    (121, 'sp')    (122, 'lt')    (123, 'sb')    (124, 'sb')    (125, 'ql')    

	Linha 17:
original:
        goto(fim);

tokenizado:
'    '         '    '         goto           (              fim            )              ;              \n             
^              ^              ^              ^              ^              ^              ^              ^              
|              |              |              |              |              |              |              |              
(126, 'tb')    (127, 'tb')    (128, 'kw')    (129, 'sb')    (130, 'id')    (131, 'sb')    (132, 'tr')    (133, 'ql')    

	Linha 18:
original:
    };

tokenizado:
'    '         }              ;              \n             
^              ^              ^              ^              
|              |              |              |              
(134, 'tb')    (135, 'sb')    (136, 'tr')    (137, 'ql')    

	Linha 19:
original:
    goto(inicio);

tokenizado:
'    '         goto           (              inicio         )              ;              \n             
^              ^              ^              ^              ^              ^              ^              
|              |              |              |              |              |              |              
(138, 'tb')    (139, 'kw')    (140, 'sb')    (141, 'id')    (142, 'sb')    (143, 'tr')    (144, 'ql')    

	Linha 20:
original:
fim:

tokenizado:
fim            :              \n             
^              ^              ^              
|              |              |              
(145, 'id')    (146, 'sb')    (147, 'ql')    

	Linha 21:
original:
    end;

tokenizado:
'    '         end            ;              \n             
^              ^              ^              ^              
|              |              |              |              
(148, 'tb')    (149, 'kw')    (150, 'tr')    (151, 'ql')    


```
4. Ao finalizar a execução digitando ‘0’ como opção, o programa gera um arquivo .csv com finalidade de ser usado no programa gerador de código intermediário (Avaliação 2), código se encontra [aqui](https://github.com/vitinhx/compiladores/blob/main/avaliacao_2/analisador_sintatico_stm.py).

5. Programa conta com tal classificação de tokens:
```
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
```
