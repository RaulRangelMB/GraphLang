%{
#include <stdio.h>
#include <stdlib.h>

extern int yylineno;
extern char* yytext;

void yyerror(const char *s);
int yylex(void);

%}

%union {
    int intval;
    char* strval;
}

%token <intval> NUMBER
%token <strval> IDENTIFIER STRING

%token VAR INT_TYPE BOOL_TYPE STRING_TYPE VERTICE EDGE
%token CONNECT WITH LEFT RIGHT BOTH
%token IF ELSE WHILE PATH PRINTLN SCAN
%token TRUE FALSE
%token EQ ASSIGN GT LT AND OR PLUS MINUS TIMES DIVIDE NOT
%token LPAREN RPAREN LBRACE RBRACE NEWLINE COMMA

%%

program:
    block
    ;

block:
    LBRACE NEWLINE statement_list RBRACE
    ;

statement_list:
    | NEWLINE statement_list
    | statement NEWLINE statement_list
    ;

statement:
    assignment
    | print
    | vardec
    | connect
    | if
    | while
    | path
    ;

assignment:
    IDENTIFIER ASSIGN bexpression
    ;

print:
    PRINTLN LPAREN bexpression RPAREN
    | PRINTLN LPAREN path RPAREN
    ;

vardec:
    VAR IDENTIFIER type
    | VAR IDENTIFIER type ASSIGN bexpression
    ;

type:
    INT_TYPE 
    | BOOL_TYPE 
    | STRING_TYPE 
    | VERTICE 
    | EDGE
    ;

connect:
    CONNECT IDENTIFIER IDENTIFIER WITH IDENTIFIER direction
    ;

direction:
    LEFT
    | RIGHT
    | BOTH
    ;

if:
    IF bexpression block
    | IF bexpression block ELSE block
    ;

while:
    WHILE bexpression block
    ;

path:
    PATH LPAREN IDENTIFIER COMMA IDENTIFIER RPAREN
    ;

bexpression:
    bterm
    | bterm OR bterm
    ;

bterm:
    relexpression
    | relexpression AND relexpression
    ;

relexpression:
    expression
    | expression EQ expression
    | expression GT expression
    | expression LT expression
    ;

expression:
    expression PLUS term
    | expression MINUS term
    | term
    ;

term:
    term TIMES factor
    | term DIVIDE factor
    | factor
    ;

factor:
    PLUS factor
    | MINUS factor
    | NOT factor
    | NUMBER
    | STRING
    | TRUE
    | FALSE
    | LPAREN bexpression RPAREN
    | IDENTIFIER
    | SCAN
    ;

%%

void yyerror(const char *s) {
    fprintf(stderr, "Erro '%s': %s\n", 
            yytext, s);
}