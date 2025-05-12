#include <stdio.h>

int yyparse(void);

int main() {
    if (yyparse() == 0) {
        printf("No errors in input.\n");
    } else {
        printf("Input is invalid.\n");
    }
    return 0;
}