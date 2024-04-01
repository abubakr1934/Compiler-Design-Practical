%{
#include <stdio.h>
int wordCount = 0,
    lineCount = 0,
    smallCount = 0,
    capitalCount = 0,
    digitCount = 0,
    specialCount = 0,
    question_count = 0;
%}
%%
(0[1-9]|[12][0-9]|3[01])\/(0[1-9]|1[0-2])\/\d{4} { printf("Date of examination: %s\n", yytext); }
"Sem:"[[:space:]]*[IiI|IiIiI|IiIiIiIiI|IiIiIiIiIiIi]+ { printf("Semester: %s\n", yytext); }
Question[0-9]+ { wordCount += yyleng; question_count++; }
[a-z] { smallCount++; }
[A-Z] { capitalCount++; }
[0-9] { digitCount++; }
[^a-zA-Z0-9\n] { specialCount++; }
\n { lineCount++; }
%%
int main() {
    FILE *file = fopen("e2text.txt", "r");
    yyin = file;
    yylex();
    fclose(file);
    printf("Number of questions: %d\n", question_count);
    printf("Number of words: %d\n", wordCount);
    printf("Number of lines: %d\n", lineCount);
    printf("Number of small letters: %d\n", smallCount);
    printf("Number of capital letters: %d\n", capitalCount);
    printf("Number of digits: %d\n", digitCount);
    printf("Number of special characters: %d\n", specialCount);
    return 0;
}
int yywrap() {
    return 1;
}
