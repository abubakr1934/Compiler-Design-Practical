%{
#include "y.tab.h"
%}

%%
[ \t]+         
[0-9]+         { yylval.num = atoi(yytext); return NUMBER; }
[a-zA-Z]+      { yylval.str = strdup(yytext); return ID; }
\n             { return NL; }
.              { return yytext[0]; }
%%