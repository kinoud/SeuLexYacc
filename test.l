%{
    /*
    this is a test
    */
%}

delim       [ \t\n]
ws          {delim}+
letter      [A-Za-z]
digit       [0-9]
id          {letter}({letter}|{digit})*
number      [+-]?{digit}+(\.{digit}+)?((E|e)[+-]?{digit}+)?

%% 

{ws}        {/* no action and no return */}
if          {printf("<if>\n");}
then        {printf("<then>\n");}
else        {printf("<else>\n");}
{id}        {printf("<id> %s\n",yytext);}
{number}    {printf("<number> %s\n",yytext);}
<           {printf("<LT>\n");}
<=          {printf("<LE>\n");}
=           {printf("<EQ>\n");}
<>          {printf("<NE>\n");}
>           {printf("<GT>\n");}
>=          {printf("<GE>\n");}

%%

int installID() {
    /* to do */
}

int installNum(){
    /* to do */
}
