from symbolpool import *
import LALR as lr

lr.init()

# lr.adp('`<start>',  ['`S'])
# lr.adp('`S',        ['`C','`C'])
# lr.adp('`C',        ['c','`C'])
# lr.adp('`C',        ['d'])
# lr.adp_done('`<start>')

lr.adp('`<start>',  ['`S'])
lr.adp('`S',        ['`L','=','`R'])
lr.adp('`S',        ['`R'])
lr.adp('`L',        ['*','`R'])
lr.adp('`L',        ['id'])
lr.adp('`R',        ['`L'])
lr.adp_done('`<start>')



lr.build()

# for i,sp in lr.state_wrappers.items():
#     print(sp)


for U in lr.ID2state.values():
    print(U)

for I,i,J,j in lr.la._prop:
    print('I%d (%s) ====> I%d (%s)'%(I.id,str(i),J.id,str(j)))