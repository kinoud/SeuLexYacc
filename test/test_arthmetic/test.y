%{
//some .y headers
%}

%type double

%token NUMBER

%left '+' '-'
%left '*' '/'
%right UMINUS
%start lines

%%
lines   : lines expr '\n'   {printf("ans=%lf\n",$2);}
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
        ;
%%
