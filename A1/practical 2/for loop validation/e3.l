%{
#include <stdio.h>
 #include "y.tab.h"
%}
alpha [A-Za-z]
digit [0-9]
%%
[\t \n]+
for return FOR;
{alpha}({alpha}|{digit})* return ID;
{digit}+ return NUM;
";" return SEMI;
"=" return EQUALS;
"+" return PLUS;
"-" return MINUS;
"++" return INCREMENT;
"--" return DECREMENT;
 "*" return TIMES;
"/" return DIVIDE;
"(" return LPAREN;
")" return RPAREN;
"{" return LBRACE;
"}" return RBRACE;
"<=" return LE;
">=" return GE;
"==" return EQ;
"!=" return NE;
"," return COMMA;
. return yytext[0];
%%
