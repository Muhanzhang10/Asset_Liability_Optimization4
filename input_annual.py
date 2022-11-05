#Building Tree structure

from tree import tree

layers = [['all'], ['asset', 'liability'], ['balance', 'interest']]

Tree = tree('all')
for layer in layers:
    if layer == ['all']:
        continue
    Tree.add_multiples(layer)

Tree.children[0].add_multiples(['a1', 'a2', 'a3'])
Tree.children[0].add_multiples(['term1', 'term2', 'term3', 'term4', 'term5'])

l1 = tree('l1')
l2 = tree('l2')
l3 = tree('l3')
l4 = tree('l4')

l1.add_multiples(['term1', 'term2', 'term3', 'term4', 'term5', 'term6'])
l2.add_multiples(['term1', 'term2', 'term3', 'term4', 'term5', 'term6'])
l3.add_multiples(['term1'])
l4.add_multiples(['term1'])
trees = [l1, l2, l3, l4]
Tree.children[1].connect(trees)
Tree.add_range()
Tree.to_dict()

#-----------------------------------------------------------------------
#Inputting numbers 

var_balance_asset = [6600, 5500, 4400, 3300, 2200, 5500, 4675, 3850, 3025, 2200, 2750, 2200, 1650, 1100, 550]
var_balance_liability = [4000, 3750, 3500, 3250, 2750, 2500, 3750, 3500, 3250, 3000, 2750, 2500, 8000, 8500]
var_interest_asset = [0.0375, 0.04, 0.0425, 0.0450, 0.0475, 0.0370, 0.0395, 0.0420, 0.0445, 0.0470, 0.0370, 0.0400, 0.0420, 0.0445, 0.0475]
var_interest_liability = [0.01, 0.0120, 0.0140, 0.0160, 0.0180, 0.0200, 0.0105, 0.0125, 0.0150, 0.0170,0.0185, 0.0200, 0.0040, 0.0045]
var = var_balance_asset + var_interest_asset + var_balance_liability + var_interest_liability
#Store all the Variables



bound_balance_asset = [0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05]
bound_balance_liability = [0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05]
bound_interest_asset = [0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05]
bound_interest_liability = [0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05]


bound = bound_balance_asset + bound_interest_asset + bound_balance_liability + bound_interest_liability
#Corresponding bounds to the variables