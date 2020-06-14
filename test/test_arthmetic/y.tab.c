#include <stdio.h>
#include <assert.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#define $$$

/*******************************
 * gen by yacc
 * user headers
 *******************************/
//some .y headers

#define _YACC_DBG_PRT

#define _YACC_DRAW_PY_CODE "draw.py"

#define _LR_PROD_CNT 11

#define _LR_STATE_CNT 19
#define _LR_SYMBOL_CNT 259
int _name_of[10];
char _name_str[10][9]={
"NUMBER",
"'+'",
"'-'",
"'*'",
"'/'",
"lines",
"expr",
"'\n'",
"'('",
"')'"
};
#define MAX_RHS_IN_ONE_PROD 100
#define MAX_TOKEN_CNT 1000000

int **_ch_val[MAX_RHS_IN_ONE_PROD];
int _ch_num;
int _pa_val;

#include "lex.yy.h"

/*******************************
 * gen by yacc
 * user functions
 *******************************/


/*******************************
 * gen by yacc
 * user actions
 *******************************/
void _yacc_action_p0(){
(*(_ch_val[0]))=(int*)malloc(sizeof(double));
printf("ans=%lf\n",(*(double*)(*(_ch_val[2]))));
}
void _yacc_action_p1(){
(*(_ch_val[0]))=(int*)malloc(sizeof(double));
(*(double*)(*(_ch_val[0])))=(*(double*)(*(_ch_val[1])));
}
void _yacc_action_p2(){
(*(_ch_val[0]))=(int*)malloc(sizeof(double));

}
void _yacc_action_p3(){
(*(_ch_val[0]))=(int*)malloc(sizeof(double));
(*(double*)(*(_ch_val[0])))=(*(double*)(*(_ch_val[1])))+(*(double*)(*(_ch_val[3])));
}
void _yacc_action_p4(){
(*(_ch_val[0]))=(int*)malloc(sizeof(double));
(*(double*)(*(_ch_val[0])))=(*(double*)(*(_ch_val[1])))-(*(double*)(*(_ch_val[3])));
}
void _yacc_action_p5(){
(*(_ch_val[0]))=(int*)malloc(sizeof(double));
(*(double*)(*(_ch_val[0])))=(*(double*)(*(_ch_val[1])))*(*(double*)(*(_ch_val[3])));
}
void _yacc_action_p6(){
(*(_ch_val[0]))=(int*)malloc(sizeof(double));
(*(double*)(*(_ch_val[0])))=(*(double*)(*(_ch_val[1])))/(*(double*)(*(_ch_val[3])));
}
void _yacc_action_p7(){
(*(_ch_val[0]))=(int*)malloc(sizeof(double));
(*(double*)(*(_ch_val[0])))=(*(double*)(*(_ch_val[2])));
}
void _yacc_action_p8(){
(*(_ch_val[0]))=(int*)malloc(sizeof(double));
(*(double*)(*(_ch_val[0])))=-(*(double*)(*(_ch_val[2])));
}
void _yacc_action_p9(){
(*(_ch_val[0]))=(int*)malloc(sizeof(double));
(*(double*)(*(_ch_val[0])))=(*(double*)(*(_ch_val[1])));
}
void _yacc_action_p10(){
(*(_ch_val[0]))=(int*)malloc(sizeof(double));
(*(double*)(*(_ch_val[0])))=(*(double*)(*(_ch_val[1])));
}


//<500 productions
void (*_action_of_p[_LR_PROD_CNT])();

//<5000 states <500 symbols
//-1 for invalid
int _shift[_LR_STATE_CNT][_LR_SYMBOL_CNT];//shift to
int _reduce[_LR_STATE_CNT][_LR_SYMBOL_CNT];//reduce production
int _rdc_len[_LR_STATE_CNT][_LR_SYMBOL_CNT];//reduce len
int _rdc_to[_LR_STATE_CNT][_LR_SYMBOL_CNT];//reduce to

struct LALRNode{
    int syb;
    int tree_id;
};

typedef struct LALRNode LNode;

LNode _symbol_stack[MAX_TOKEN_CNT];
int _sb_top=0;
int _state_stack[MAX_TOKEN_CNT],_st_top=0;

struct TreeNode{
    int syb;
    int *val;
};

typedef struct TreeNode TNode;

TNode _tree_node[MAX_TOKEN_CNT];
int _node_cnt,_tree_root;
int _edge_cnt;
int _edge_head[MAX_TOKEN_CNT];
int _edge_next[MAX_TOKEN_CNT];
int _edge_to[MAX_TOKEN_CNT];

void _add_shift(int i,int j,int x){
    _shift[i][x]=j;
}
void _add_reduce(int i,int x,int p,int len,int to){
    _reduce[i][x]=p;
    _rdc_len[i][x]=len;
    _rdc_to[i][x]=to;
}

int _ytab_init(){
    memset(_shift,-1,sizeof _shift);
    memset(_reduce,-1,sizeof _reduce);
    memset(_edge_head,-1,sizeof _edge_head);
    _sb_top=-1;
    _st_top=0;
    _state_stack[0]=0;
    _node_cnt=0;
    _edge_cnt=0;
    /*******************************
     * gen by yacc
     *******************************/
    //sth like:
    //add_shift(x,x,x);
    //add_reduce(x,x,x,x,x);
    //action_of_p[x]=xxxxxxx;
_action_of_p[0]=_yacc_action_p0;
_action_of_p[1]=_yacc_action_p1;
_action_of_p[2]=_yacc_action_p2;
_action_of_p[3]=_yacc_action_p3;
_action_of_p[4]=_yacc_action_p4;
_action_of_p[5]=_yacc_action_p5;
_action_of_p[6]=_yacc_action_p6;
_action_of_p[7]=_yacc_action_p7;
_action_of_p[8]=_yacc_action_p8;
_action_of_p[9]=_yacc_action_p9;
_action_of_p[10]=_yacc_action_p10;
_add_reduce(0,'\n',2,0,257); _add_shift(0,1,257); _add_reduce(0,NUMBER,2,0,257); 
_add_reduce(0,'-',2,0,257); _add_reduce(0,'(',2,0,257); _add_reduce(0,0,2,0,257); 
_add_shift(1,2,'\n'); _add_shift(1,3,NUMBER); _add_shift(1,4,'-'); 
_add_shift(1,17,258); _add_shift(1,14,'('); _add_reduce(1,0,10,1,-2); 
_add_reduce(2,'\n',1,2,257); _add_reduce(2,NUMBER,1,2,257); _add_reduce(2,'-',1,2,257); 
_add_reduce(2,'(',1,2,257); _add_reduce(2,0,1,2,257); _add_reduce(3,'\n',9,1,258); 
_add_reduce(3,')',9,1,258); _add_reduce(3,'*',9,1,258); _add_reduce(3,'+',9,1,258); 
_add_reduce(3,'-',9,1,258); _add_reduce(3,'/',9,1,258); _add_shift(4,3,NUMBER); 
_add_shift(4,4,'-'); _add_shift(4,5,258); _add_shift(4,14,'('); 
_add_reduce(5,'\n',8,2,258); _add_reduce(5,')',8,2,258); _add_reduce(5,'*',8,2,258); 
_add_reduce(5,'+',8,2,258); _add_reduce(5,'-',8,2,258); _add_reduce(5,'/',8,2,258); 
_add_shift(6,3,NUMBER); _add_shift(6,4,'-'); _add_shift(6,7,258); 
_add_shift(6,14,'('); _add_reduce(7,'\n',5,3,258); _add_reduce(7,')',5,3,258); 
_add_reduce(7,'*',5,3,258); _add_reduce(7,'+',5,3,258); _add_reduce(7,'-',5,3,258); 
_add_reduce(7,'/',5,3,258); _add_shift(8,3,NUMBER); _add_shift(8,4,'-'); 
_add_shift(8,9,258); _add_shift(8,14,'('); _add_reduce(9,'\n',3,3,258); 
_add_reduce(9,')',3,3,258); _add_shift(9,6,'*'); _add_reduce(9,'+',3,3,258); 
_add_reduce(9,'-',3,3,258); _add_shift(9,12,'/'); _add_shift(10,3,NUMBER); 
_add_shift(10,4,'-'); _add_shift(10,11,258); _add_shift(10,14,'('); 
_add_reduce(11,'\n',4,3,258); _add_reduce(11,')',4,3,258); _add_shift(11,6,'*'); 
_add_reduce(11,'+',4,3,258); _add_reduce(11,'-',4,3,258); _add_shift(11,12,'/'); 
_add_shift(12,3,NUMBER); _add_shift(12,4,'-'); _add_shift(12,13,258); 
_add_shift(12,14,'('); _add_reduce(13,'\n',6,3,258); _add_reduce(13,')',6,3,258); 
_add_reduce(13,'*',6,3,258); _add_reduce(13,'+',6,3,258); _add_reduce(13,'-',6,3,258); 
_add_reduce(13,'/',6,3,258); _add_shift(14,3,NUMBER); _add_shift(14,4,'-'); 
_add_shift(14,15,258); _add_shift(14,14,'('); _add_shift(15,16,')'); 
_add_shift(15,6,'*'); _add_shift(15,8,'+'); _add_shift(15,10,'-'); 
_add_shift(15,12,'/'); _add_reduce(16,'\n',7,3,258); _add_reduce(16,')',7,3,258); 
_add_reduce(16,'*',7,3,258); _add_reduce(16,'+',7,3,258); _add_reduce(16,'-',7,3,258); 
_add_reduce(16,'/',7,3,258); _add_shift(17,18,'\n'); _add_shift(17,6,'*'); 
_add_shift(17,8,'+'); _add_shift(17,10,'-'); _add_shift(17,12,'/'); 
_add_reduce(18,'\n',0,3,257); _add_reduce(18,NUMBER,0,3,257); _add_reduce(18,'-',0,3,257); 
_add_reduce(18,'(',0,3,257); _add_reduce(18,0,0,3,257); 
_name_of[NUMBER]=0;_name_of['+']=1;_name_of['-']=2;_name_of['*']=3;
_name_of['/']=4;_name_of[257]=5;_name_of[258]=6;_name_of['\n']=7;
_name_of['(']=8;_name_of[')']=9;
}

const int _inq_size=MAX_TOKEN_CNT;
LNode _inq[MAX_TOKEN_CNT+5];
int _inq_f,_inq_r;//[f,r) front rear

void _inq_clear(){
    _inq_f=0;
    _inq_r=0;
}

int _inq_len(){
    return (_inq_r-_inq_f+_inq_size)%_inq_size;
}

void _inq_append(LNode x){
    int _=_inq_r;
    _inq_r=(_inq_r+1)%_inq_size;
    assert(_inq_r!=_inq_f);//ensure not full
    _inq[_]=x;
}

void _inq_appendleft(LNode x){
    _inq_f--;
    if(_inq_f<0)_inq_f+=_inq_size;
    assert(_inq_f!=_inq_r);
    _inq[_inq_f]=x;
}

LNode _inq_pop(){
    assert(_inq_r!=_inq_f);
    _inq_r--;
    if(_inq_r<0)_inq_r+=_inq_size;
    return _inq[_inq_r];
}

LNode _inq_popleft(){
    assert(_inq_r!=_inq_f);
    int _=_inq_f;
    _inq_f=(_inq_f+1)%_inq_size;
    return _inq[_];
}

void _inq_print(){
    int x=_inq_f;
    while(x!=_inq_r){
        int d=_inq[x].syb;
        if(d>0&&isgraph(d))
            printf("%c",d);
        else
            printf("%d ",d);
        x=(x+1)%_inq_size;
    }
}

void _print(){
    printf("[ ");
    for(int i=0;i<=_sb_top;i++){
        int x=_symbol_stack[i].syb;
        if(isgraph(x))printf("%c ",x);
        else printf("%d ",x);
    }
    printf("] <=== [ ");
    _inq_print();
    printf("] <=== yylex()\n");
    printf("[ ");
    for(int i=0;i<=_st_top;i++){
        printf("%d ",_state_stack[i]);
    }
    printf(" ]\n");
}

int _new_tree(TNode u){
    //return tree_id
    //printf("new node %d\n\n",_node_cnt);
    _tree_node[_node_cnt++]=u;
    return _node_cnt-1;
}

void _dfs_clean(int u){
    TNode tu=_tree_node[u];
    int h=_edge_head[u];
	while(h!=-1){
        _dfs_clean(_edge_to[h]);
        h=_edge_next[h];
    }
    free(tu.val);
}

FILE* DrawHandle;

void _dfs(int u){
    TNode tu=_tree_node[u];
    int h=_edge_head[u];
	int first_node=1;
    if(h==-1){
		fprintf(DrawHandle,"tree_node_%d=\"%s\"\n",u,tu.syb!=-2?_name_str[_name_of[tu.syb]]:"<start>");
        return;
    }
    while(1){
        _dfs(_edge_to[h]);
        h=_edge_next[h];
        if(h==-1)break;
    }
	fprintf(DrawHandle,"tree_node_%d=Tree(\"%s\",[",u,tu.syb!=-2?_name_str[_name_of[tu.syb]]:"<start>");
	h=_edge_head[u];
	while(1){
		if(first_node)first_node=0;else fprintf(DrawHandle,",");
		fprintf(DrawHandle,"tree_node_%d",_edge_to[h]);
        h=_edge_next[h];
        if(h==-1)break;
    }
	fputs("])\n",DrawHandle);
}


int _step(){
    //return 1 : step success
    //return 0 : step failure

    int cur=_state_stack[_st_top];
    if(_inq_len()==0){
        int syb=yylex();
        int*valptr;
        if(yyaval==NULL){
            valptr=(int*)malloc(sizeof(int));
            *valptr=yylval;
        }else{
            valptr=yyaval;
        }
        _inq_append((LNode){syb,_new_tree((TNode){syb,valptr})});
        //printf("call yylex() get: %d val=%d\n",syb,val);
    }
    LNode nxt=_inq[_inq_f];
    int syb=nxt.syb;
    if(syb==-1){
        _inq_popleft();
        return 1; //omit
    }
    if(syb==-2){
#ifdef _YACC_DBG_PRT
        puts("yacc work is done");
        puts("\nfinal stacks:");
        _print();
#endif
        _tree_root=nxt.tree_id;
        //printf("root = %d\n",nxt.tree_id);
#ifdef _YACC_DRAW_PY_CODE
        DrawHandle=fopen(_YACC_DRAW_PY_CODE, "w");
		fputs("from nltk.tree import Tree\nfrom nltk.draw.tree import draw_trees\n\n",DrawHandle);
        _dfs(_tree_root);
		fprintf(DrawHandle,"draw_trees(tree_node_%d)\n",_tree_root);
        fclose(DrawHandle);
#ifdef _YACC_DBG_PRT
        puts("grammer tree draw code generated!");
#endif
#endif
        return 0;
    }

    int s=_shift[cur][syb];
    int r=_reduce[cur][syb];
    if(s==-1&&r==-1){
#ifdef _YACC_DBG_PRT
        puts("error: cannot shift nor reduce");
#endif
        return 0;
    }

    if(s!=-1){
        _symbol_stack[++_sb_top]=_inq_popleft();
        _state_stack[++_st_top]=s;
    }else{
        int len=_rdc_len[cur][syb],
            to=_rdc_to[cur][syb];

        int u=_new_tree((TNode){to,NULL});

        _ch_val[0]=&(_tree_node[u].val);
        assert(_ch_val[0]!=0);
        assert(_ch_val[0]!=NULL);
        // add edges in grammer tree
        for(int i=0;i<len;i++){
            LNode x=_symbol_stack[_sb_top--];
            _ch_val[len-i]=&(_tree_node[x.tree_id].val);// for action
            assert(_ch_val[len-i]!=0);
            assert(_ch_val[len-i]!=NULL);
            int e=_edge_cnt++;
            _edge_to[e]=x.tree_id;
            _edge_next[e]=_edge_head[u];
            _edge_head[u]=e;
            //printf("new edge %d -> %d\n\n",u,x.tree_id);
        }

        _st_top-=len;
        
        _inq_appendleft((LNode){to,u});

        _action_of_p[r]();
        
    }
    //_print();
    return 1;
}


FILE *_fp;

char input(){
    int x=fgetc(_fp);
    return x==-1?0:x;
}

void unput(char x){
    ungetc(x,_fp);
}

int main(int argc,char** argv){
    assert(argc>=2);
    _fp=fopen(argv[1],"r");
    if(_fp==NULL){
        puts("open file error");
        return 0;
    }
    _lexyy_init();
    _ytab_init();
    while(_step());
    _dfs_clean(_tree_root);
#ifdef _YACC_DBG_PRT
    puts("\nparsing done, please check the results");
#endif
}