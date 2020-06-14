%{
#include <stdlib.h>
#include "test.h"
%}

delim       [ \t]
ws          {delim}+
letter      [\101-\132a-z]
digit       [\x30-\x39]
id          {letter}({letter}|{digit})*
number      {digit}+(\.{digit}+)?((\x65|"\105")[+-]?{digit}+)?

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
