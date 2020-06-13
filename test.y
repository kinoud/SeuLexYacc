%{
//some .y headers
#include "test.h"
%}
%token NUMBER ID
%type Magic
%token MAGIC

%left '+' '-'
%left '*' '/'
%right UMINUS
%start lines

%%
%type int
lines   : lines expr '\n'   {printf("ans=%d\n",$2);}
        | lines '\n' 
        |                
        ;
expr    : expr '+' expr     {$$=$1+$3;}
        | expr '-' expr     {$$=$1-$3;}
        | expr '*' expr     {$$=$1*$3;}  
        | expr '/' expr     {$$=$1/$3;}
        | '(' expr ')'      {$$=$2;}
        | '-' expr %prec UMINUS {$$=-$2;}
        | NUMBER   
        | MAGIC      {$$=$1.x;printf("Magic:%d\n",$1.y);}
        ;
%%
