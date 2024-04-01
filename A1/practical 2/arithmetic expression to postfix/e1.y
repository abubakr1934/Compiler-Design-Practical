%{
#include<stdio.h>
#include<stdlib.h>
int answer=0;
%}
%token NUMBER ID NL
%left '+' '-'
%left '*' '/'
%right NEGATIVE
%%
stmt : exp NL {
printf("Valid expression & Answer: %d \n",$1);
exit(0);
}
|
exp1 NL {
printf("Valid Expression \nBut, Calculation Can Be Performed On Numbers\n");
exit(0);
}
;

exp : exp '+' exp {$$=$1+$3; printf("+");}
| exp '-' exp {$$=$1-$3; printf("-");}
| exp '' exp {$$=$1$3; printf("*");}
| exp '/' exp {$$=$1/$3; printf("/");}
| '(' exp ')' {$$=$2;}
| NUMBER {$$=$1; printf("%d", $1);}
;
exp1 : exp1 '+' exp1 {printf("+");}
| exp1 '-' exp1 {printf("-");}
| exp1 '' exp1 {printf("");}
| exp1 '/' exp1 {printf("/");}
| '(' exp1 ')'
| ID { printf("%s",$1);}
;

%%
int yyerror(char *msg)
{
printf("Invalid Expression \n");
exit(0);
}
int main()
{
printf("Enter the expression : \n");
yyparse();
}
Lex file :
%{
#include "y.tab.h"
%}
%%
[ \t]+
[0-9]+ { yylval.num = atoi(yytext); return NUMBER; }
[a-zA-Z]+ { yylval.str = strdup(yytext); return ID; }
\n { return NL; }
. { return yytext[0]; }
%%