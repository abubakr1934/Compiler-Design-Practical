%{
#include <stdio.h>
#include <stdlib.h>
%}
%token ID NUM IF ELSE LE GE EQ NE OR AND
%right "="
%left OR AND
%left '>' '<' LE GE EQ NE
%left '+' '-'
%left '*' '/'
%right UMINUS
%left '!'
%%
S : ST {printf("Valid if statement\n"); exit(0);}
ST : IF '(' E ')' DEF ELSE DEF
;
DEF : '{' BODY '}'

| E';'
| ST
|
;
BODY : BODY BODY
| E ';'
| ST
|
;
E : ID '=' E
| E '+' E
| E '-' E
| E '*' E
| E '/' E
| E '<' E
| E '>' E
| E LE E
| E GE E
| E EQ E
| E NE E
| E OR E
| E AND E
| E '+' '+'
| E '-' '-'
| ID
| NUM
;

E2 : E'<'E
| E'>'E
| E LE E
| E GE E
| E EQ E
| E NE E
| E OR E
| E AND E
;
%%
main() {
printf("Enter the if else statement to check :");
yyparse();
}
int yywrap(void)
{
return 1;
}

int yyerror(char *mes) {
printf("Invalid if else statement\n");
return 0;
}