#include<stdio.h>
#include<assert.h>
#include<string.h>
#define $$$

/*******************************
 * gen by yacc
 * user headers
 *******************************/
$$$


int yylval;
int *_ch_val[100];
int _ch_num;
int _pa_val;

#include "lex.yy.c"

/*******************************
 * gen by yacc
 * user functions
 *******************************/
$$$


/*******************************
 * gen by yacc
 * user actions
 *******************************/
$$$


//<500 productions
void (*_action_of_p[500])();

//<5000 states <500 symbols
//-1 for invalid
int _shift[5000][1000];//shift to
int _reduce[5000][1000];//reduce production
int _rdc_len[5000][1000];//reduce len
int _rdc_to[5000][1000];//reduce to

struct LALRNode{
    int syb;
    int tree_id;
};

typedef struct LALRNode LNode;

LNode _symbol_stack[1000000];
int _sb_top=0;
int _state_stack[1000000],_st_top=0;

struct TreeNode{
    int syb;
    int val;
};

typedef struct TreeNode TNode;

TNode _tree_node[1000000];
int _node_cnt,_tree_root;
int _tree_edge[1000000],_edge_cnt;
int _edge_head[1000000];
int _edge_next[1000000];
int _edge_to[1000000];

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
$$$

}

const int _inq_size=1000000;
LNode _inq[1000000+5];
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


void _dfs(int u){
    TNode tu=_tree_node[u];
    printf("Tree((%d,%d)",tu.syb,tu.val);
    int h=_edge_head[u];
    if(h==-1){
        printf(",[])");
        return;
    }
    printf(",[");
    while(1){
        _dfs(_edge_to[h]);
        h=_edge_next[h];
        if(h==-1)break;
        printf(",");
    }
    printf("])");
}


int _step(){
    //return 1 : step success
    //return 0 : step failure

    int cur=_state_stack[_st_top];
    if(_inq_len()==0){
        int syb=yylex();
        int val=yylval;
        _inq_append((LNode){syb,_new_tree((TNode){syb,val})});
        //printf("call yylex() get: %d val=%d\n",syb,val);
    }
    LNode nxt=_inq[_inq_f];
    int syb=nxt.syb;
    if(syb==-1)return 1; //omit
    if(syb==-2){
        puts("yacc work is done");
        puts("\nfinal stacks:");
        _print();
        _tree_root=nxt.tree_id;
        //printf("root = %d\n",nxt.tree_id);
        puts("\ngrammer tree:");
        _dfs(_tree_root);
        puts("");
        return 0;
    }

    int s=_shift[cur][syb];
    int r=_reduce[cur][syb];
    if(s==-1&&r==-1){
        puts("error: cannot shift nor reduce");
        return 0;
    }

    if(s!=-1){
        _symbol_stack[++_sb_top]=_inq_popleft();
        _state_stack[++_st_top]=s;
    }else{
        int len=_rdc_len[cur][syb],
            to=_rdc_to[cur][syb];

        int u=_new_tree((TNode){to,-1});
        
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
    return fgetc(_fp);
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
    puts("\nparsing done, please check the results");
}