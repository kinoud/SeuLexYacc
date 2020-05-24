int yylval;

#include "lex.yy.c"

FILE *_fp;

char input(){
    return fgetc(_fp);
}
void unput(char x){
    ungetc(x,_fp);
}

int main(){
    _lexyy_init();
    _fp=fopen("in.txt","r");
    if(_fp==NULL){
        printf("open file error!\n");
        return 0;
    }
    while(1){
        int tk=yylex();
        if(tk==-1)continue;
        if(tk<-1)break;
        printf("token%4d [%s]         yylval=%d\n",tk,yytext,yylval);
    }
}