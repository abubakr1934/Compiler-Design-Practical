%{
#include "y.tab.h"
%}

%%

"a"        { return A; }
"b"        { return B; }
"c"        { return C; }
.          { return ERROR; }
\n         { return 0; } /* Return 0 for newline to terminate input */
%%

int yywrap() {
    return 1;
}
