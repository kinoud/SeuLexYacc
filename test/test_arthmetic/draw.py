from nltk.tree import Tree
from nltk.draw.tree import draw_trees

tree_node_1="lines"
tree_node_0="NUMBER"
tree_node_3=Tree("expr",[tree_node_0])
tree_node_2="'+'"
tree_node_4="NUMBER"
tree_node_6=Tree("expr",[tree_node_4])
tree_node_7=Tree("expr",[tree_node_3,tree_node_2,tree_node_6])
tree_node_5="'+'"
tree_node_8="NUMBER"
tree_node_10=Tree("expr",[tree_node_8])
tree_node_11=Tree("expr",[tree_node_7,tree_node_5,tree_node_10])
tree_node_9="'+'"
tree_node_12="NUMBER"
tree_node_14=Tree("expr",[tree_node_12])
tree_node_15=Tree("expr",[tree_node_11,tree_node_9,tree_node_14])
tree_node_13="'
'"
tree_node_17=Tree("lines",[tree_node_1,tree_node_15,tree_node_13])
tree_node_16="'-'"
tree_node_18="NUMBER"
tree_node_20=Tree("expr",[tree_node_18])
tree_node_21=Tree("expr",[tree_node_16,tree_node_20])
tree_node_19="'-'"
tree_node_22="NUMBER"
tree_node_24=Tree("expr",[tree_node_22])
tree_node_25=Tree("expr",[tree_node_21,tree_node_19,tree_node_24])
tree_node_23="'-'"
tree_node_26="NUMBER"
tree_node_28=Tree("expr",[tree_node_26])
tree_node_29=Tree("expr",[tree_node_25,tree_node_23,tree_node_28])
tree_node_27="'-'"
tree_node_30="NUMBER"
tree_node_32=Tree("expr",[tree_node_30])
tree_node_33=Tree("expr",[tree_node_29,tree_node_27,tree_node_32])
tree_node_31="'
'"
tree_node_35=Tree("lines",[tree_node_17,tree_node_33,tree_node_31])
tree_node_34="NUMBER"
tree_node_37=Tree("expr",[tree_node_34])
tree_node_36="'*'"
tree_node_38="NUMBER"
tree_node_40=Tree("expr",[tree_node_38])
tree_node_41=Tree("expr",[tree_node_37,tree_node_36,tree_node_40])
tree_node_39="'/'"
tree_node_42="NUMBER"
tree_node_44=Tree("expr",[tree_node_42])
tree_node_45=Tree("expr",[tree_node_41,tree_node_39,tree_node_44])
tree_node_43="'/'"
tree_node_46="NUMBER"
tree_node_48=Tree("expr",[tree_node_46])
tree_node_49=Tree("expr",[tree_node_45,tree_node_43,tree_node_48])
tree_node_47="'
'"
tree_node_51=Tree("lines",[tree_node_35,tree_node_49,tree_node_47])
tree_node_50="NUMBER"
tree_node_53=Tree("expr",[tree_node_50])
tree_node_52="'+'"
tree_node_54="NUMBER"
tree_node_56=Tree("expr",[tree_node_54])
tree_node_55="'*'"
tree_node_57="NUMBER"
tree_node_59=Tree("expr",[tree_node_57])
tree_node_60=Tree("expr",[tree_node_56,tree_node_55,tree_node_59])
tree_node_61=Tree("expr",[tree_node_53,tree_node_52,tree_node_60])
tree_node_58="'+'"
tree_node_62="NUMBER"
tree_node_64=Tree("expr",[tree_node_62])
tree_node_65=Tree("expr",[tree_node_61,tree_node_58,tree_node_64])
tree_node_63="'
'"
tree_node_67=Tree("lines",[tree_node_51,tree_node_65,tree_node_63])
tree_node_68=Tree("<start>",[tree_node_67])
draw_trees(tree_node_68)
