from symbolpool import *
import LALR as lr

lr.init()

lr.adp('`<start>',  ['`S'])
lr.adp('`S',        ['`C','`C'])
lr.adp('`C',        ['c','`C'])
lr.adp('`C',        ['d'])
lr.adp_done('`<start>')

lr.build()

for i,sp in lr.state_wrappers.items():
    print(sp)