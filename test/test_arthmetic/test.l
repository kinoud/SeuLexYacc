%{
#define OMIT    -1
//user defined token id should > 256
%}

delim       [ \t]
ws          {delim}+
digit       [0-9]
number      {digit}+(\.{digit}+)?

%% 

{ws}        {return OMIT;}
{number}    { yyaval=(int*)malloc(sizeof(double));
                *((double*)yyaval)=str_to_double(yytext,yyleng);
                //printf(">>>>>>> yytext=%s yyleng=%d *yyaval=%lf\n",yytext,yyleng,*((double*)yyaval));
                return NUMBER;}
"+"           {return '+';}
"-"          {return '-';}
"*"           {return '*';}
"/"          {return '/';}
"("           {return '(';}
")"           {return ')';}
"\n"           {return '\n';}

%%

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
