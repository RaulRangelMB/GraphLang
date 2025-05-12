%{

#include "parser.tab.h"
#include <string.h>
#include <stdlib.h>

%}

DIGIT [0-9]
LETTER [a-zA-Z]
IDENTIFIER {LETTER}({LETTER}|{DIGIT}|_)*
NUMBER {DIGIT}+

%%

"var"           { return VAR; }
"int"           { return INT_TYPE; }
"bool"          { return BOOL_TYPE; }
"string"        { return STRING_TYPE; }
"vertice"       { return VERTICE; }
"edge"          { return EDGE; }

"connect"       { return CONNECT; }
"with"          { return WITH; }
"left"          { return LEFT; }
"right"         { return RIGHT; }
"both"          { return BOTH; }

"if"            { return IF; }
"else"          { return ELSE; }
"while"         { return WHILE; }

"path"          { return PATH; }
"Println"       { return PRINTLN; }
"Scan()"        { return SCAN; }

"true"          { return TRUE; }
"false"         { return FALSE; }

"=="            { return EQ; }
"="             { return ASSIGN; }
">"             { return GT; }
"<"             { return LT; }

"&&"            { return AND; }
"||"            { return OR; }
"+"             { return PLUS; }
"-"             { return MINUS; }
"*"             { return TIMES; }
"/"             { return DIVIDE; }
"!"             { return NOT; }

"("             { return LPAREN; }
")"             { return RPAREN; }
"{"             { return LBRACE; }
"}"             { return RBRACE; }
","             { return COMMA; }
"\n"            { return NEWLINE; }

{IDENTIFIER}            { yylval.strval = strdup(yytext); return IDENTIFIER; }
{DIGIT}+                { yylval.intval = atoi(yytext); return NUMBER; }

\"[^\"]*\"      {
                  // Remove quotes and store string
                  yylval.strval = strdup(yytext + 1);
                  yylval.strval[strlen(yylval.strval) - 1] = 0;
                  return STRING;
               }

[ \t\r]+        ; // Skip whitespace
.               { printf("Unknown character: %s\n", yytext); return -1; }

%%

int yywrap() {
    return 1;
}