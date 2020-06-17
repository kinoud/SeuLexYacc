#include "y.tab.h"
#define OMIT -1
#define MAX_TOKEN_SIZE 500000

// int yylval; NOTE: defined in driver program (such as y.tab.c)
extern char yytext[MAX_TOKEN_SIZE];
extern int yyleng;
extern int yylval;
extern int*yyaval;
extern int yylex();
int input(); // NOTE: defined in driver program (such as y.tab.c)
void unput(int); // NOTE: defined in driver program (such as y.tab.c)
void _lexyy_init();