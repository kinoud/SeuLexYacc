%{
#include<stdlib.h>
#define NUMBER  260
#define ID      261
#define OMIT    -1
//user defined token id should > 256
%}

delim       [ \t]
ws          {delim}+
letter      [A-Za-z]
digit       [0-9]
id          {letter}({letter}|{digit})*
number      {digit}+(\.{digit}+)?((E|e)[+-]?{digit}+)?

%% 

{ws}        {return OMIT;}
{id}        {return ID;}
{number}    {yylval=atoi(yytext);return NUMBER;}
\+           {return '+';}
-           {return '-';}
\*           {return '*';}
/           {return '/';}
\(           {return '(';}
\)           {return ')';}
\n           {return '\n';}

%%

int installID() {
    /* to do */
}

int installNum(){
    /* to do */
}
