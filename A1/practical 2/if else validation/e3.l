%{
#include <stdio.h>
#include "y.tab.h"
%}

%%
[\t\n]               /* ignore whitespace and newlines */
if                   { return IF; }
else                 { return ELSE; }
[a-zA-Z]+            { return IDs; }
[0-9]+               { return NUM; }
">="                 { return GE; }
"=="                 { return EQ; }
"!="                 { return NE; }
"||"                 { return OR; }
"&&"                 { return AND; }
.                    { return yytext[0]; }
%%

int yywrap() {
    return 1;
}