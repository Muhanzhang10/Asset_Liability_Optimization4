from tree import tree
from input import Tree  
from input import var
from input import bound
from scipy.optimize import minimize
import numpy as np
from saveFile import save
#var = []

def run(path = '/Users/zhangmuhan/Desktop/result.xlsx', var = var):
    def year_total(after, isAsset):
        if isAsset == True:
            path = 'asset'
        else:
            path = 'liability'
        total = 0
        for i in range(Tree.getTo(['all', path, 'balance']).range[0], Tree.getTo(['all', path, 'balance']).range[1]):
            total += var[i]
        return total

    def year_average(after, isAsset):
        if isAsset == True:
            path = 'asset'
        else:
            path = 'liability'
        total = 0
        total_month = len(Tree.getTo(['all', path, 'balance']).children)
        for month_name in Tree.getTo(['all', path, 'balance']).children:
            month_total = 0
            r = Tree.getTo(['all', path, 'balance', month_name.name]).range
            for i in range (r[0], r[1]):
                month_total += after[i]
            month_total = month_total * (total_month - int(month_name.name[-1]) + 0.5)
            total += month_total

        total *= 2
        total /= total_month
        return total

    def asset_bound(after):
        sum = year_average(after, True)
        return 51000 - sum

    def liability_bound(after):
        sum = year_average(after, False)
        return sum - 55000

        
    def find_bound():
        boundary = []
        for i in range(len(var)):
            boundary.append(((1 - bound[i]) * var[i], (1 + bound[i]) * var[i]))
        return boundary

    def ratio(after):
        interval_a = Tree.getTo(['all', 'asset','balance']).range
        interval_l = Tree.getTo(['all', 'liability', 'balance']).range
        sum_a = 0
        sum_l = 0
        for i in range(interval_a[0], interval_a[1]):
            sum_a += after[i]
        for i in range(interval_l[0], interval_l[1]):
            sum_l += after[i]
        ratio = sum_a / sum_l
        return ratio

    
    def ratio_up(after):
        return 0.85 * 1.05 - ratio(after)
    
    def ratio_down(after):
        return ratio(after) - 0.85 * 0.95 

    def NII(after):
        sum_t = 0
        month = 1
        total_month = len(Tree.getTo(['all', 'asset', 'balance']).children)
        for month_name in Tree.getTo(['all', 'asset', 'balance']).children:
            sum = 0
            month_name = month_name.name
            interval_a_balance = Tree.getTo(['all', 'asset', 'balance', month_name]).range
            interval_a_interest = Tree.getTo(['all', 'asset', 'interest', month_name]).range
            interval_l_balance = Tree.getTo(['all', 'liability', 'balance', month_name]).range
            interval_l_interest = Tree.getTo(['all', 'liability', 'interest', month_name]).range
            balance_a = after[interval_a_balance[0]: interval_a_balance[1]]
            interest_a = after[interval_a_interest[0]: interval_a_interest[1]]
            balance_l = after[interval_l_balance[0]: interval_l_balance[1]]
            interest_l = after[interval_l_interest[0]: interval_l_interest[1]]
            for i in range(len(balance_a)):
                sum += balance_a[i] * interest_a[i]
            for i in range(len(balance_l)):
                sum -= balance_l[i] * interest_l[i]
            sum = sum * ((total_month - month) * 2 + 1)
            sum_t += sum
            print(month_name, sum)
            month += 1
            
        return -sum_t
    
    boundary = find_bound()


    '''
    print("NII Before optimization: ", NII(var) * -1)
    print("ratio: ", ratio(var))
    '''

    cons = []
    cons.append({'type': 'ineq', 'fun': asset_bound})
    cons.append({'type': 'ineq', 'fun': liability_bound})
    cons.append({'type': 'ineq', 'fun': ratio_down})
    cons.append({'type': 'ineq', 'fun': ratio_up})
    res = minimize(NII, var, method = 'trust-constr', bounds = boundary, constraints = cons, options = {"maxiter": 2000})
    print("Success: ", res.success)
    print("Ratio: ", ratio(res.x))
    print('Asset_bound: ', 51000 - asset_bound(res.x))
    print('Liability_bound: ', 55000 + liability_bound(res.x))
    print("NII Before optimization: ", NII(var) * -1)
    print("NII After optimization: ", NII(res.x) * -1)
    print("Asset balance: ", res.x[Tree.getTo(['all', 'asset', 'balance']).range[0]:Tree.getTo(['all', 'asset', 'balance']).range[1]:])
    print("Liability balance: ", res.x[Tree.getTo(['all', 'liability', 'balance']).range[0]:Tree.getTo(['all', 'liability', 'balance']).range[1]:])
    print("Asset interest: ", res.x[Tree.getTo(['all', 'asset', 'interest']).range[0]:Tree.getTo(['all', 'asset', 'interest']).range[1]:])
    print("Liability interest: ", res.x[Tree.getTo(['all', 'liability', 'interest']).range[0]:Tree.getTo(['all', 'liability', 'interest']).range[1]:])
    print()
    info = {'Liability total': 2400 + liability_bound(res.x), 'Asset total': 20500 - asset_bound(res.x), 'Before optimization':  NII(var) * -1, 'After optimization': NII(res.x) * -1}
    
    return res.x, NII(res.x) * -1



run(path = '/Users/zhangmuhan/Desktop/result.xlsx', var = var)




