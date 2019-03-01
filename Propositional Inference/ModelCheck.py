
# coding: utf-8

# In[ ]:

from pythonds.basic import Stack
from operator import *
import sys


# In[ ]:

class BinaryTree:
    def __init__(self, root_obj):
        self.key = root_obj
        self.left_child = None
        self.right_child = None
        
    def insert_left(self, new_val):
        if self.left_child == None:
            self.left_child = BinaryTree(new_val)
        else:
            t = BinaryTree(new_val)
            t.left_child = self.left_child
            self.left_child = t
            
    def insert_right(self, new_val):
        if self.right_child == None:
            self.right_child = BinaryTree(new_val)
        else:
            t = BinaryTree(new_val)
            t.right_child = self.right_child
            self.right_child = t
            
    def get_right_child(self):
        return self.right_child
    
    def get_left_child(self):
        return self.left_child
    
    def set_root_val(self, obj):
        self.key = obj
        
    def get_root_val(self):
        return self.key


# In[ ]:

class sentence:
    def __init__(self):        
        self.val=None  # parsetree of storing sentence
        self.name=None
        self.symbols=[]
        
    def creatS(self,fpexp):
        fplist = fpexp.split()
        p_stack = Stack()
        e_tree = BinaryTree('')
        p_stack.push(e_tree)
        current_tree = e_tree
        for i in fplist:
            if i == "(":
                current_tree.insert_left('')
                p_stack.push(current_tree)
                current_tree = current_tree.get_left_child()
            elif i in "'and','or'":
                current_tree.set_root_val(i)
                current_tree.insert_right('')
                p_stack.push(current_tree)
                current_tree=current_tree.get_right_child()
            elif i in "'not'":
                current_tree = p_stack.pop()
                current_tree.set_root_val(i)
                current_tree.insert_left(False)
                current_tree.insert_right('')
                p_stack.push(current_tree)
                current_tree=current_tree.get_right_child()
            elif i == ')':
                current_tree = p_stack.pop()
            else:
                current_tree.set_root_val(i)
                parent = p_stack.pop()
                current_tree = parent
                if i not in self.symbols:
                    self.symbols.append(i)
        self.val=e_tree
        
    def inorderlist(self,tree):
        leftC = tree.get_left_child()
        rightC = tree.get_right_child()
        if leftC and rightC:
            return str(self.inorderlist(leftC))+' '+str(tree.get_root_val())+' '+str(self.inorderlist(rightC))
        else:
            return tree.get_root_val()  
        
def evaluate(tree,model):
    leftC = tree.get_left_child()
    rightC = tree.get_right_child()
    if leftC and rightC:
        if tree.get_root_val()=='and':
            return evaluate(leftC,model) and evaluate(rightC,model)
        elif tree.get_root_val()=='not':
            return not evaluate(rightC,model)
        else:
            return evaluate(leftC,model) or evaluate(rightC,model)
    elif tree.get_root_val() not in model.keys():
        return None
    else:
        return model[tree.get_root_val()]


# In[ ]:

def PL_True(KB,model):
    if len(KB)==1:
        return evaluate(KB[0].val,model)
    else:
        done=False
        for i in KB:
            if evaluate(i.val,model)==False:
                return False
        return True


# In[ ]:

def TT_Entails(KB,alpha):
    symbols=[]
    for i in KB:
        for j in i.symbols:
            if j not in symbols:
                symbols.append(j)
    return TT_Check(KB,alpha,symbols,{})


# In[ ]:

def TT_Check(KB,alpha,symbols,model):
    if not symbols:
        if PL_True(KB,model):
            return PL_True(alpha,model)
        else:
            return True
    else:
        p=symbols[len(symbols)-1]
        rest=symbols[:len(symbols)-1]

        return TT_Check(KB,alpha,rest,dict(model, **{p:True})) and TT_Check(KB,alpha,rest,dict(model, **{p:False}))


# In[ ]:

def converter(exp):
    exp=exp.split()
    if len(exp)==1:
        return exp[0]
    temp=[]
    if '==>' in exp:
        index=exp.index('==>')
        exp[index]=')'
        exp.insert(index+1,'or')
        exp.insert(0,'~')
        exp.insert(0,'(')        
    elif '<==>' in exp:
        index=exp.index('<==>')
        head=exp[:]
        tail=exp[:]
        #head
        head[index]=')'
        head.insert(index+1,'or')
        head.insert(0,'~')
        head.insert(0,'(') 
        #tail
        tail[index]='or'
        tail.insert(index+1,'not')
        tail.insert(index+1,'(')
        tail.insert(len(tail),')')
        exp=['(']+head+[')']+['and']+['(']+tail+[')']
    
    for i in exp:
        if i=='&':
            temp.append('and')
        elif i=='|':
            temp.append('or')
        elif i=='~':
            temp.append('not')
        else:
            temp.append(i)
    temp.insert(0,'(')
    temp.insert(len(temp),')')
    rep=' '.join(temp)           
        
    return rep


# In[ ]:

def connection(KB,alpha):
    # create KB
    KB1=[]
    for s in KB:
        temp=converter(s)
        rule=sentence()
        rule.creatS(temp)
        KB1.append(rule)
    #create alpha
    temp=converter(alpha)
    alpha1=sentence()
    alpha1.creatS(temp)

    
    result1=TT_Entails(KB1,[alpha1])
    if result1==True:
        return result1
    else:
        temp='( not '+temp+' )'
        
        alpha2=sentence()
        alpha2.creatS(temp)
        result2=TT_Entails(KB1,[alpha2])        
        if result2==True:
            return False
        else:
            return "Cannot tell"

    


# In[ ]:

# This is the main 
over=False
while not over:
    sys.stdout.write('Start Model Checking? Y or N \n')
    while True:
        end=input()
        if end!='Y' and end!='N':
            sys.stderr.write('Input erro: please input Y or N\n')
        else:
            break
    if end=='N':
        over=True
        break
        
    #build KB
    sys.stdout.write('Please start to create new knowledge base\n')
    sen=''
    KB=[]
    while sen!='end':
        sen=input()
        if sen!='end':
            KB.append(sen)
            
     #check sentence       
    sys.stdout.write('Please input sentence that you want to check\n')
    alpha=''
    while alpha!='end':
        alpha=input()
        if alpha!='end':
            result=connection(KB,alpha)
            sys.stdout.write('%s\n'%(result))


# S1=sentence()
# S2=sentence()
# S3=sentence()
# S1.creatS("P")
# S2.creatS("( ( not P ) or Q )")
# S3.creatS("( not Q )")
# KB=[S1,S2]
# alpha=[S3]
# TT_Entails(KB,alpha)

# R1=sentence()
# R2=sentence()
# R3=sentence()
# R4=sentence()
# R5=sentence()

# R1.creatS("( not P11 )")
# R2.creatS("( ( ( not B11 ) or ( P12 or P21 ) ) and ( B11 or ( not ( P12 or P21 ) ) ) )")
# R3.creatS("( ( ( not B21 ) or P11 or P22 or P31 ) and ( ( ( not P11 ) and ( not P22 ) and ( not P31 ) ) or B21 ) )")
# R4.creatS("( not B11 )")
# R5.creatS("B21")
# KB=[R1,R2,R3,R4,R5]
# R6=sentence()
# R6.creatS("P12")
# alpha=[R6]
# 
# TT_Entails(KB,alpha)

# L1=sentence()
# L2=sentence()
# L3=sentence()
# L4=sentence()
# L5=sentence()
# L6=sentence()

# L1.creatS("( ( ( not A ) or ( C and A ) ) and ( A or ( not ( C and A ) ) ) )")
# L2.creatS("( ( not B ) or ( not C ) and ( C or B ) )")
# L3.creatS("( ( ( not C ) or ( B or ( not A ) ) ) and (   ( not ( B or ( not A ) ) ) or C ) )")
# L4.creatS("L")
# L5.creatS("B")
# L6.creatS("C")

# KB=[L1,L2,L3]
# alpha=[L4]
# TT_Entails(KB,alpha)
