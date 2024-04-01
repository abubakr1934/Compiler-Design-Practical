%{
#include <stdio.h>
#include <stdlib.h>
%}

%token A B C
%token ERROR

%%

start: s C { printf("String accepted\n"); }
     | ERROR { printf("String rejected\n"); }
     ;

s: A s B
   | A B
   ;

%%

int yyerror(char *msg) {
    printf("Syntax Error\n");
    return 0;
}

int main() {
    printf("Enter the string: ");
    yyparse();
    return 0;
}


