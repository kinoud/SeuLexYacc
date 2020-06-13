#include<stdio.h>
#include<string.h>
#include<assert.h>
#include "lex.yy.h"


FILE *_fp;

char input(){
    int x=fgetc(_fp);
    return x==-1?0:x;
}
void unput(char x){
    ungetc(x,_fp);
}

int main(int argc,char** argv){
    _lexyy_init();
    assert(argc>=2);
    _fp=fopen(argv[1],"r");
    if(_fp==NULL){
        puts("open file error");
        return 0;
    }
    while(1){
        int tk=yylex();
        if(tk==OMIT)continue;
        if(tk<-1)break;
        printf("token%4d [%s]         yylval=%d\n",tk,yytext,yylval);
        if(tk==0)break;
    }
}