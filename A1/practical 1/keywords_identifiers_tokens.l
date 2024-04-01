%{
#include<stdio.h>
#include<stdlib.h>

int keyword=0;
int identifier=0;
int integer=0;
int float_number=0;  
int operator_count=0;  
%}

%%
"while"|"if"|"else"|"return"|"int"|"char"|"float" { keyword++; printf("Keyword : %s\n", yytext); }
[a-zA-Z_][a-zA-Z0-9_]* { identifier++; printf("Identifier : %s\n", yytext); }
[0-9]+ { integer++; printf("Integer : %s\n", yytext); }
[0-9]*"."[0-9]+ { float_number++; printf("\t float : %s\n", yytext); }
"<="|"=="|"="|"++"|"-"|"*"|"+" { operator_count++; printf("\t operator : %s\n", yytext); }
.;

%%

int main()
{
    yyin = fopen("C:\\Users\\ANUJ BELGAONKAR\\Desktop\\Practical1\\e1text.txt", "r");
    yylex();
    return 0;
}

int yywrap()
{
    return 1;
}