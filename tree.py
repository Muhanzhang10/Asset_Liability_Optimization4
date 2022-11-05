from openpyxl import Workbook
from openpyxl import load_workbook

class tree:
    #constructor
    def __init__(self, name_):
        self.name = name_ #The name of the asset or liability
        self.name2 = ''   #leave it for now
        self.children = [] #O(n) to get to the next layer, too slow
        self.range = []  #The range of the index of given path (a size 2 list)

    #copy constructor
    def copy(self, Tree):
        self.name = Tree.name
        if Tree.is_leaf() == True:
            return
        else:
            for i in range(len(Tree.children)):
                self.children.append(tree('temp_name'))
                self.children[i].copy(Tree.children[i])

    #go to a certain Node from the beginning
    def getTo(self, path):
        temp = self
        for p in path:
            for i in range(len(temp.children)):
                if temp.children[i].name == p:
                    temp = temp.children[i]
                    break
        if temp.name != path[-1]:
            print("Path does not exist")
            return None
        return temp

    
    #add a leaf under current tree
    def add_child(self, name):
        temp = tree(name)
        self.children.append(temp)


    #add a leaf under certain node
    #@parent: list of parent 
    def add(self, name_, parents):
        temp = self
        temp = self.getTo(parents)
        if temp != None:
            temp.add_child(name_) 
        else:
            return None
            

    #add multiple leaf under all current leaf nodes
    #@names: list of nodes' name to be added
    def add_multiples(self, names):
        if self.is_leaf() == True:
            for name in names:
                temp = tree(name)
                self.children.append(temp)
            return
        for i in range(len(self.children)):
            self.children[i].add_multiples(names)
    
    #add multiple trees under all current leaf nodes
    #@trees: list of trees' name to be added
    def connect(self, trees):
        if self.is_leaf() == True:
            for Tree in trees:
                tempTree = tree('temp_name')
                tempTree.copy(Tree)
                self.children.append(tempTree)
            return
        for i in range(len(self.children)):
            self.children[i].connect(trees)

    #determine if current node is leaf 
    def is_leaf(self):
        if len(self.children) == 0:
            return True
        else:
            return False


    #add range for leaves
    def addLeafRange(self, range_):
        if self.is_leaf() == True:
            self.range = range_.copy()
        else:
            print("Not a leaf, error")
        return


    #add range for branches
    def addbranchRange(self):
        if self.is_leaf() == False:
            self.range = [self.FindLow(), self.FindHigh()]
        else:
            print("Not a branch, error")
        return

    def FindLow(self):
        if self.is_leaf() == True:
            return self.range[0]
        return self.children[0].FindLow()

    def FindHigh(self):
        if self.is_leaf() == True:
            return self.range[-1]
        return self.children[-1].FindHigh()


    #add all the range 
    #call after all the nodes have beeen added
    def add_range(self):
        curr_index = [0]
        self.traversal1(curr_index)
        self.traversal2()
        return

    def traversal1(self, curr_index):
        if self.is_leaf() == True:
            self.addLeafRange([curr_index[-1], curr_index[-1] + 1])
            return curr_index.append(curr_index[-1] + 1)
        for i in range(len(self.children)):
            self.children[i].traversal1(curr_index)
        return

    def traversal2(self):
        if self.is_leaf() == True:
            return
        self.addbranchRange()
        for i in range(len(self.children)):
            self.children[i].traversal2()
    
    #obtain all the leave nodes
    def getLeaves(self):
        leaves = []
        self.getLeaves_helper(leaves)
        return leaves

    def getLeaves_helper(self, leaves):
        if self.is_leaf() == True:
            leaves.append(self)
            return
        for i in range(len(self.children)):
            self.children[i].getLeaves_helper(leaves)
        return

    #print the tree
    def printTree(self):
        '''
        print()
        print(self.name, ": ", end = '' )
        for i in range(len(self.children)):
            print(self.children[i].name, ', ', end = '')
        '''
        print(self.name, "   ", self.range)
        for i in range(len(self.children)):
            self.children[i].printTree()
        return
    
    #count number of nodes
    def count(self):
        if self.is_leaf() == True:
            return 1
        total = 1
        for i in range(len(self.children)):
            total += self.children[i].count()
        return total
    
    def countleaves(self):
        if self.is_leaf() == True:
            return 1
        total = 0
        for i in range(len(self.children)):
            total += self.children[i].countleaves()
        return total


    #Change structure of the tree from list to dictionary to improve runtime 
    def to_dict(self):
        temp = {}
        for i in range(len(self.children)):
            temp[self.children[i].name] = self.children[i]
            if self.is_leaf() == False:
                self.children[i].to_dict()
        self.children = temp
       
    #goint to a certain node from the beginning after turning into dictionary
    def getTod(self, path):
        temp = self
        for p in path[1::]:
            try:
                temp = temp.children[p]
            except BaseException:
                print('Path does not exist')
                return None
        return temp
