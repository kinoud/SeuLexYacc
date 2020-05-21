%{
//#include <stdio.h>
//#include "y.tab.h"

//void count(void);
%}

D			[0-9]
L			[a-zA-Z_]
H			[a-fA-F0-9]
E			([Ee][+-]?{D}+)
P                       ([Pp][+-]?{D}+)
FS			(f|F|l|L)
IS                      ((u|U)|(u|U)?(l|L|ll|LL)|(l|L|ll|LL)(u|U))

%%

//[^\n]*              { /* consume //-comment */ }
auto			{ print("AUTO"); }
_Bool			{ print("BOOL"); }
break			{ print("BREAK"); }
case			{ print("CASE"); }
char			{ print("CHAR"); }
_Complex		{ print("COMPLEX"); }
const			{ print("CONST"); }
continue		{ print("CONTINUE"); }
default		{ print("DEFAULT"); }
do			{ print("DO"); }
double		{ print("DOUBLE"); }
else			{ print("ELSE"); }
enum			{ print("ENUM"); }
extern		{ print("EXTERN"); }
float			{ print("FLOAT"); }
for			{ print("FOR"); }
goto			{ print("GOTO"); }
if			{ print("IF"); }
_Imaginary		{ print("IMAGINARY"); }
inline		{ print("INLINE"); }
int			{ print("INT"); }
long			{ print("LONG"); }
register		{ print("REGISTER"); }
restrict		{ print("RESTRICT"); }
return		{ print("RETURN"); }
short			{ print("SHORT"); }
signed		{ print("SIGNED"); }
sizeof		{ print("SIZEOF"); }
static		{ print("STATIC"); }
struct		{ print("STRUCT"); }
switch		{ print("SWITCH"); }
typedef		{ print("TYPEDEF"); }
union			{ print("UNION"); }
unsigned		{ print("UNSIGNED"); }
void			{ print("VOID"); }
volatile		{ print("VOLATILE"); }
while			{ print("WHILE"); }

{L}({L}|{D})*		{ print("ID"); }

0[xX]{H}+{IS}?		{ print("CONSTANT"); }
0[0-7]*{IS}?		{ print("CONSTANT"); }
[1-9]{D}*{IS}?		{ print("CONSTANT"); }
L?'(\\.|[^\\'\n])+'	{ print("CONSTANT"); }

{D}+{E}{FS}?		{ print("CONSTANT"); }
{D}*\.{D}+{E}?{FS}?	{ print("CONSTANT"); }
{D}+\.{D}*{E}?{FS}?	{ print("CONSTANT"); }
0[xX]{H}+{P}{FS}?	{ print("CONSTANT"); }
0[xX]{H}*\.{H}+{P}?{FS}?     { print("CONSTANT"); }
0[xX]{H}+\.{H}*{P}?{FS}?     { print("CONSTANT"); }


L?\"(\\.|[^\\"\n])*\"	{ print("STRING_LITERAL"); }

\.\.\.			{ print("ELLIPSIS"); }
>>=			{ print("RIGHT_ASSIGN"); }
<<=			{ print("LEFT_ASSIGN"); }
\+=			{ print("ADD_ASSIGN"); }
-=			{ print("SUB_ASSIGN"); }
\*=			{ print("MUL_ASSIGN"); }
/=			{ print("DIV_ASSIGN"); }
%=			{ print("MOD_ASSIGN"); }
&=			{ print("AND_ASSIGN"); }
\^=			{ print("XOR_ASSIGN"); }
\|=			{ print("OR_ASSIGN"); }
>>			{ print("RIGHT_OP"); }
<<			{ print("LEFT_OP"); }
\+\+			{ print("INC_OP"); }
--			{ print("DEC_OP"); }
->			{ print("PTR_OP"); }
&&			{ print("AND_OP"); }
\|\|			{ print("OR_OP"); }
<=			{ print("LE_OP"); }
>=			{ print("GE_OP"); }
==			{ print("EQ_OP"); }
!=			{ print("NE_OP"); }
;			{ print("';'"); }
(\{|<%)		{ print("left curve brace"); }
(\}|%>)		{ print("right curve brace"); }
,			{ print("','"); }
:			{ print("':'"); }
=			{ print("'='"); }
\(			{ print("'('"); }
\)			{ print("')'"); }
(\[|<:)		{ print("'['"); }
(\]|:>)		{ print("']'"); }
\.			{ print("'.'"); }
&			{ print("'&'"); }
!			{ print("'!'"); }
~			{ print("'~'"); }
-			{ print("'-'"); }
\+			{ print("'+'"); }
\*			{ print("'*'"); }
/			{ print("'/'"); }
%			{ print("'%'"); }
<			{ print("'<'"); }
>			{ print("'>'"); }
\^			{ print("'^'"); }
\|			{ print("'|'"); }
\?			{ print("'?'"); }

[ \t\n]		{ }
.			{ /* Add code to complain about unmatched characters */ }

%%


void print(const char* t){
	printf("<%s> %s\n",t,yytext);
}

int yywrap(void)
{
	return 1;
}


// void comment(void)
// {
// 	char c, prev = 0;
  
// 	while ((c = input()) != 0)      /* (EOF maps to 0) */
// 	{
// 		if (c == '/' && prev == '*')
// 			return;
// 		prev = c;
// 	}
// 	error("unterminated comment");
// }


int column = 0;

void count(void)
{
	int i;

	for (i = 0; yytext[i] != '\0'; i++)
		if (yytext[i] == '\n')
			column = 0;
		else if (yytext[i] == '\t')
			column += 8 - (column % 8);
		else
			column++;

	//ECHO;
}


int check_type(void)
{
/*
* pseudo code --- this is what it should check
*
*	if (yytext == type_name)
*		return TYPE_NAME;
*
*	return IDENTIFIER;
*/

/*
*	it actually will only return IDENTIFIER
*/

	//return IDENTIFIER;
}