#include "lex.yy.c"


FILE *_fp;

char input(){
    int x=fgetc(_fp);
    return x==-1?0:x;
}
void unput(char x){
    ungetc(x,_fp);
}

int main(){
    _lexyy_init();
    _fp=fopen("in.c","r");
    if(_fp==NULL){
        printf("open file error!\n");
        return 0;
    }
    while(1){
        int tk=yylex();
        if(tk==-1)continue;
        if(tk<-1)break;
        printf("token%4d [%s]         yylval=%d\n",tk,yytext,yylval);
        if(tk==0)break;
    }
}