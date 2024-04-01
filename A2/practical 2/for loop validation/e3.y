%{
#include <stdio.h>
#include <stdlib.h>
%}
%token FOR ID NUM SEMI EQUALS PLUS MINUS INCREMENT DECREMENT
TIMES DIVIDE LPAREN RPAREN LBRACE RBRACE LE GE EQ NE COMMA
%right EQUALS
%left PLUS MINUS
%left TIMES DIVIDE
%left INCREMENT DECREMENT
%left LE GE EQ NE
%left LPAREN RPAREN
%nonassoc LBRACE RBRACE
%%
Program : Statement { printf("Valid for statement\n"); exit(0); }
;
Statement : ForLoop
;
ForLoop : FOR LPAREN ForInit SEMI ForCond SEMI ForIncr RPAREN LBRACE
LoopBody RBRACE
;
ForInit : ID EQUALS exp
|
;
ForCond : exp
|
;
ForIncr : exp
|
;
LoopBody : Statement
| LoopBody Statement
|
;
exp : exp PLUS exp
| exp MINUS exp
| exp TIMES exp
| exp DIVIDE exp
| exp LE exp
| exp GE exp
| exp EQ exp
| exp NE exp
| ID
| NUM
| ID INCREMENT
| ID DECREMENT
;
%%
int main() {
printf("Enter the for loop statement to check :\n");
yyparse();
return 0;
}
int yywrap(void) {;
return 1;
}
int yyerror(char *s) {
printf("Invalid for statement\n");
return 0;
}