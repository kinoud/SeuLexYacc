%{
#include <stdlib.h>
#include "test.h"
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
{digit}`@{digit} {
yyaval=(int*)malloc(sizeof(Magic));
((Magic*)yyaval)->x=0x30^yytext[0];
((Magic*)yyaval)->y=0x30^yytext[3];
return MAGIC;
}
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
