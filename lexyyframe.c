#include<stdio.h>
#include<string.h>
#include<assert.h>
#define ECHO printf("%s\n",yytext)
#define $$$

/******************************************************
 * gen by lex
 * user headers
 ******************************************************/

$$$

// int yylval; NOTE: defined in driver program (such as y.tab.c)
char yytext[1000000];
int yyleng;
int yylex();
char input(); // NOTE: defined in driver program (such as y.tab.c)
void unput(char); // NOTE: defined in driver program (such as y.tab.c)
/******************************************************
 * gen by lex
 * user defined functions
 ******************************************************/

$$$

/******************************************************
 * gen by lex
 * user defined actions
 ******************************************************/

$$$

/****************************************************
 * dfa things
 ****************************************************/
int _n,_start,_cur;
int _to[5000][256];
int _accept[5000];
int (*_action_of_node[5000])(); // actions are functions that return token id (int)

void _dfa_init(){
    memset(_to,-1,sizeof _to);
    memset(_accept,0,sizeof _accept);
}

void _dfa_set_edge(int i,int j,int x){
    _to[i][x]=j;
}

void _dfa_set_action(int node_id,int (*action)()){
    _accept[node_id]=1;
    _action_of_node[node_id]=action;
}

void _dfa_build(){
    _dfa_init();
    /******************************************
     * gen by lex
     ******************************************/
    // n=...
    // start=...
    // dfa_set_edge...
    // dfa_set_rule...
$$$
}

int _dfa_step(char ter){
    if(_to[_cur][ter]==-1)
        return 1;
    _cur=_to[_cur][ter];
    return 0;
}

int _dfa_acceptable(int i){
    return _accept[i]==1;
}

int _do_action(int i){
    assert(_dfa_acceptable(i));
    return _action_of_node[i]();
}

/*******************************************************
 * yy things
 *******************************************************/

int yylex(){
    // return 0 : end fo input (eos)
    // return -1 : omit
    // return -2 : <start> symbol, so that yacc knows parsing has been done
    // return -3 : error
    int last_ac=-1,last_ac_len=0;
    yyleng=0;
    yylval=-1;
    _cur=_start;
    char x;
    while(1){
        x=input();
        yytext[yyleng++]=x;
        yytext[yyleng]=0;
        if(x==0||_dfa_step(x)!=0){
            while(yyleng>last_ac_len)
                unput(yytext[--yyleng]);
            yytext[yyleng]=0;
            break;
        }
        if(_dfa_acceptable(_cur)){
            last_ac=_cur;
            last_ac_len=yyleng;
        }
    }
    if(yyleng==0){
        if(x==0){
            printf("lex work is done, now returning the last symbol 0\n");
            return 0;
        }else{
            perror("error when tokenizing\n");
            printf("last input char: %d\n",x);
            return -3;
        }
    };
    return _do_action(_cur);
}

void _lexyy_init(){
    _dfa_build();
}