from tree import tree
from input_annual import Tree  
from input_annual import var
from input_annual import bound
from scipy.optimize import minimize
import numpy as np
from saveFile import save

'''
@para
path: path of the result to be stored; to be built later
var: initial values of the variables; comes in as a list
'''
def run(path = 'result.xlsx', var = var):
    #Asset total should not exceed 51000
    def asset_bound(after):
        sum = 0 
        interval = Tree.getTod(['all', 'asset', 'balance']).range
        for i in range(interval[0], interval[1]):
            sum += after[i]
        return 51000 - sum

    #Liability total should not fall below 55000
    def liability_bound(after):
        sum = 0
        interval = Tree.getTod(['all', 'liability', 'balance']).range
        for i in range(interval[0], interval[1]):
            sum += after[i]
        return sum - 55000

    #Calcualate boundary for each variable
    def find_bound():
        boundary = []
        for i in range(len(var)):
            boundary.append(((1 - bound[i]) * var[i], (1 + bound[i]) * var[i]))
        return boundary

    #Helper function for ratio_up and ratio_down
    #Calculates ratio of asset and liability times a certain coefficient 
    def ratio(after):
        interval_a = Tree.getTod(['all', 'asset','balance']).range
        interval_l = Tree.getTod(['all', 'liability', 'balance']).range
        sum_a = 0
        sum_l = 0
        for i in range(interval_a[0], interval_a[1]):
            sum_a += after[i]
            
        for i in range(interval_l[0], interval_l[1]):
            sum_l += after[i]

        ratio = sum_a / sum_l / 0.55 * 0.5
        return ratio

    #ratio should not exceed 0.85 * 1.05
    def ratio_up(after):
        return 0.85 * 1.05 - ratio(after)
    
    #ratio should not fall below 0.85 * 0.95
    def ratio_down(after):
        return ratio(after) - 0.85 * 0.95 

    #function to be optimized
    def NII(after):
        sum = 0
        interval_a_balance = Tree.getTod(['all', 'asset', 'balance']).range
        interval_a_interest = Tree.getTod(['all', 'asset', 'interest']).range
        interval_l_balance = Tree.getTod(['all', 'liability', 'balance']).range
        interval_l_interest = Tree.getTod(['all', 'liability', 'interest']).range
        balance_a = after[interval_a_balance[0]: interval_a_balance[1]]
        interest_a = after[interval_a_interest[0]: interval_a_interest[1]]
        balance_l = after[interval_l_balance[0]: interval_l_balance[1]]
        interest_l = after[interval_l_interest[0]: interval_l_interest[1]]
        for i in range(len(balance_a)):
            sum += balance_a[i] * interest_a[i]
        for i in range(len(balance_l)):
            sum -= balance_l[i] * interest_l[i]
        
        return -sum
    
    boundary = find_bound()
    '''
    print("NII Before optimization: ", NII(var) * -1)
    print("ratio: ", ratio(var))
    print('asset_bound: ', 51000 - asset_bound(var))
    print('liability_bound: ', 55000 + liability_bound(var))
    '''


    #optimization process
    cons = []
    cons.append({'type': 'ineq', 'fun': asset_bound})
    cons.append({'type': 'ineq', 'fun': liability_bound})
    cons.append({'type': 'ineq', 'fun': ratio_down})
    cons.append({'type': 'ineq', 'fun': ratio_up})
    res = minimize(NII, var, method = 'trust-constr', bounds = boundary, constraints = cons, options = {"maxiter": 2000})
    #print results
    print("Success: ", res.success)
    print("Ratio: ", ratio(res.x))
    print('asset_bound: ', 51000 - asset_bound(res.x))
    print('liability_bound: ', 55000 + liability_bound(res.x))
    print("NII Before optimization: ", NII(var) * -1)
    print("NII After optimization: ", NII(res.x) * -1)
    print(res.x)
    print()
    info = {'Liability total': 2400 + liability_bound(res.x), 'Asset total': 20500 - asset_bound(res.x), 'Before optimization':  NII(var) * -1, 'After optimization': NII(res.x) * -1}
    
    return res.x, NII(res.x) * -1
    

run(path = 'result.xlsx', var = var)




