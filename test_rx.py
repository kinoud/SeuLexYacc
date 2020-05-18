import regexparser as rx

rx.build()
rx.clear()
rx.pushseq(list('((a|bc[^d])*|e)f'))
rx.pusheos()
rx.parse()