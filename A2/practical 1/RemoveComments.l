%{
%}

start \/\* 
end \*\/ 

%%

\/\/[^\n]* { printf("Single-line comment: %s\n", yytext); }

{start}[^]{end} { printf("Multiline comment: %s\n", yytext); }

.|\n { fprintf(yyout, "%s", yytext); }

%%

int main() 
{ 
    yyin = fopen("ep4read.txt", "r"); 
    yyout = fopen("ep4write.txt", "w"); 

    yylex(); 

    fclose(yyin);
    fclose(yyout);

    return 0; 
}

int yywrap() {
    return 1;
}