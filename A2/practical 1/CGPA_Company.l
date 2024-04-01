%{
#include <stdio.h>
#include <string.h>
int tcs = 0, infosys = 0, wipro = 0, accenture = 0, informatica = 0;
int males = 0, females = 0, cse = 0, it = 0, ec = 0;
%}

%%
[ \t]+          ; // Skip whitespace

[0-9]+\.[0-9]+  { float cgpa = atof(yytext); if (cgpa < 10) printf("CGPA: %s\n", yytext); }
[0-9]{10}       { printf("Mobile: %s\n", yytext); }
[0-9]+          { printf("Package: %s\n", yytext); }
[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,} { printf("Mail id: %s\n", yytext); }

"TCS"             { printf("Placed at: TCS\n"); tcs++; }
"Infosys"         { printf("Placed at: Infosys\n"); infosys++; }
"Wipro"           { printf("Placed at: Wipro\n"); wipro++; }
"Accenture"       { printf("Placed at: Accenture\n"); accenture++; }
"Informatica"     { printf("Placed at: Informatica\n"); informatica++; }

"Female"          { printf("Gender: Female\n"); females++; }
"Male"            { printf("Gender: Male\n"); males++; }

"CSE"             { printf("Branch: CSE\n"); cse++; }
"IT"              { printf("Branch: IT\n"); it++; }
"EC"              { printf("Branch: EC\n"); ec++; }

[a-zA-Z]+       { printf("Name of student: %s\n", yytext); }
.               ;

%%

int main(void)
{
    yyin = fopen("e3text.txt", "r");
    yylex();
    fclose(yyin);
    printf("\nNumber of students placed in each company:\n");
    printf("TCS: %d, \nInfosys: %d ,\n Wipro: %d,\n Accenture: %d,\n Informatica: %d\n",
    tcs, infosys, wipro, accenture, informatica);
    printf("Number of male students: %d\n", males);
    printf("Number of female students: %d\n", females);
    printf("Number of CSE students: %d\n", cse);
    printf("Number of IT students: %d\n", it);
    printf("Number of EC students: %d\n", ec);
    return 0;
}
int yywrap() { return 1; }