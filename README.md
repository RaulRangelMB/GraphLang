# GraphLang

GraphLang é uma linguagem de programação feita para a criação, manipulação e visualização de grafos. Vértices e arestas são tratados como tipos de variáveis (como int, bool, str, etc.) e tem seus próprios identificadores e valores.

## Flex e Bison

As ferramentas Flex e Bison foram usadas para verificar se uma entrada é válida. A análise léxica é feita no arquivo `lexer.l`, que age como Tokenizer, e a análise sintática é feita no arquivo `parser.y`, que age como Parser.

Para compilar e executar, use os comandos abaixo:

```
bison -d parser.y
flex lexer.l
gcc -o graphlang main.c parser.tab.c lex.yy.c -lfl
./graphlang < teste.txt
```

Isso permite validar se uma entrada está conforme as regras da linguagem.