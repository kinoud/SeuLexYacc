#include<stdio.h>
#include<string.h>
#include<assert.h>
#include "lex.yy.h"
#define ECHO printf("%s\n",yytext)
#define $$$

/******************************************************
 * gen by lex
 * user headers
 ******************************************************/

#define OMIT    -1
//user defined token id should > 256

#define _DFA_NODE_CNT 12

// int yylval; NOTE: defined in driver program (such as y.tab.c)
char yytext[MAX_TOKEN_SIZE];
int yyleng;
int yylval;
int*yyaval;
int yylex();
/******************************************************
 * gen by lex
 * user defined functions
 ******************************************************/


double str_to_double(char* s,int n){
	double ans=0;
	int tail=0;
	for(int i=0;i<n;i++){
		if(s[i]=='.')
			tail=n-1-i;
		else{
			ans=ans*10+s[i]-'0';
		}
	}
	for(int i=0;i<tail;i++)
		ans/=10;
	return ans;
}

/******************************************************
 * gen by lex
 * user defined actions
 ******************************************************/

int _lex_action_0(){
return OMIT;
}
int _lex_action_1(){
 yyaval=(int*)malloc(sizeof(double));
                *((double*)yyaval)=str_to_double(yytext,yyleng);
                //printf(">>>>>>> yytext=%s yyleng=%d *yyaval=%lf\n",yytext,yyleng,*((double*)yyaval));
                return NUMBER;
}
int _lex_action_2(){
return '+';
}
int _lex_action_3(){
return '-';
}
int _lex_action_4(){
return '*';
}
int _lex_action_5(){
return '/';
}
int _lex_action_6(){
return '(';
}
int _lex_action_7(){
return ')';
}
int _lex_action_8(){
return '\n';
}

/****************************************************
 * dfa things
 ****************************************************/
int _n,_start_node,_cur;
int _to[_DFA_NODE_CNT][256];
int _accept[_DFA_NODE_CNT];
int (*_action_of_node[_DFA_NODE_CNT])(); // actions are functions that return token id (int)

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
_n=12;_start_node=7;
_dfa_set_edge(3,3,54); _dfa_set_edge(3,3,56); _dfa_set_edge(3,8,46); 
_dfa_set_edge(3,3,55); _dfa_set_edge(3,3,49); _dfa_set_edge(3,3,57); 
_dfa_set_edge(3,3,48); _dfa_set_edge(3,3,51); _dfa_set_edge(3,3,50); 
_dfa_set_edge(3,3,52); _dfa_set_edge(3,3,53); _dfa_set_edge(5,5,9); 
_dfa_set_edge(5,5,32); _dfa_set_edge(6,6,54); _dfa_set_edge(6,6,56); 
_dfa_set_edge(6,6,55); _dfa_set_edge(6,6,49); _dfa_set_edge(6,6,57); 
_dfa_set_edge(6,6,48); _dfa_set_edge(6,6,51); _dfa_set_edge(6,6,50); 
_dfa_set_edge(6,6,52); _dfa_set_edge(6,6,53); _dfa_set_edge(7,3,54); 
_dfa_set_edge(7,3,56); _dfa_set_edge(7,4,43); _dfa_set_edge(7,3,55); 
_dfa_set_edge(7,9,42); _dfa_set_edge(7,2,40); _dfa_set_edge(7,5,9); 
_dfa_set_edge(7,11,47); _dfa_set_edge(7,0,10); _dfa_set_edge(7,3,49); 
_dfa_set_edge(7,3,57); _dfa_set_edge(7,10,41); _dfa_set_edge(7,3,48); 
_dfa_set_edge(7,3,51); _dfa_set_edge(7,3,50); _dfa_set_edge(7,1,45); 
_dfa_set_edge(7,5,32); _dfa_set_edge(7,3,52); _dfa_set_edge(7,3,53); 
_dfa_set_edge(8,6,54); _dfa_set_edge(8,6,56); _dfa_set_edge(8,6,55); 
_dfa_set_edge(8,6,49); _dfa_set_edge(8,6,57); _dfa_set_edge(8,6,48); 
_dfa_set_edge(8,6,51); _dfa_set_edge(8,6,50); _dfa_set_edge(8,6,52); 
_dfa_set_edge(8,6,53); _dfa_set_action(0,_lex_action_8); _dfa_set_action(1,_lex_action_3); _dfa_set_action(2,_lex_action_6); 
_dfa_set_action(3,_lex_action_1); _dfa_set_action(4,_lex_action_2); _dfa_set_action(5,_lex_action_0); 
_dfa_set_action(6,_lex_action_1); _dfa_set_action(9,_lex_action_4); _dfa_set_action(10,_lex_action_7); 
_dfa_set_action(11,_lex_action_5); }

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
    yyaval=NULL;
    _cur=_start_node;
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
#ifdef _LEX_DBG_PRT
            printf("lex work is done, now returning the last symbol 0\n");
#endif
            return 0;
        }else{
#ifdef _LEX_DBG_PRT
            perror("error when tokenizing\n");
            printf("last input char: %d\n",x);
#endif
            return -3;
        }
    };
    return _do_action(_cur);
}

void _lexyy_init(){
    _dfa_build();
}