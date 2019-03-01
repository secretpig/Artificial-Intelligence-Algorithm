
# coding: utf-8

# In[278]:

from pythonds.basic import Stack
from operator import *
import sys


# In[279]:

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


# In[280]:

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
        
    def updatesymbols(self,tree):
        ref=['and','not','or',False]
        if tree:
            if (tree.get_root_val() not in ref) and (tree.get_root_val() not in self.symbols):
                self.symbols.append(tree.get_root_val())
            self.updatesymbols(tree.get_left_child())
            self.updatesymbols(tree.get_right_child())         
   
        
    def inorderlist(self,tree):
        leftC = tree.get_left_child()
        rightC = tree.get_right_child()
        if leftC and rightC:
            return str(self.inorderlist(leftC))+' '+str(tree.get_root_val())+' '+str(self.inorderlist(rightC))
        else:
            return tree.get_root_val() 
        
    def show(self,tree):
        if tree:
            print(tree.get_root_val())
            self.show(tree.get_left_child())
            self.show(tree.get_right_child())         
    


# In[281]:

def CNF(sen):    
    tree=sen.val
    movein(tree)
    distribute(tree)
    listC=cut(tree)
    clauses=[]
    for i in listC:
        temp=sentence()
        temp.val=i
        temp.updatesymbols(temp.val)
        clauses.append(temp)
    return clauses    
    
def movein(tree):
    dic={'and':'or','or':'and'}
    if tree:
        if tree.get_root_val()=='not' and tree.get_right_child().get_root_val() in dic.keys():
            tree.insert_left('not')
            tree.set_root_val(dic[tree.get_right_child().get_root_val()])            
            rightC=tree.get_right_child()
            RleftC=rightC.get_left_child()
            leftC=tree.get_left_child()            
            leftC.right_child=RleftC          
            rightC.set_root_val('not')
            rightC.left_child=None
            rightC.insert_left(False)
        elif tree.get_root_val()=='not' and tree.get_right_child().get_root_val()=='not':
            rightC=tree.get_right_child()
            RrightC=rightC.get_right_child()
            tree.set_root_val(RrightC.get_root_val())
            tree.left_child=RrightC.left_child
            tree.right_child=RrightC.right_child
            
        movein(tree.get_left_child())
        movein(tree.get_right_child())
    
def distribute(tree):
    if tree:
        if tree.get_root_val()=='or' and tree.get_right_child().get_root_val()=='and':
            tree.set_root_val('and')
            tree.insert_left('or')
            tree.get_right_child().set_root_val('or')
            tree.get_left_child().right_child=tree.get_right_child().get_left_child()
            tree.get_right_child().left_child=tree.get_left_child().get_left_child()
        elif tree.get_root_val()=='or' and tree.get_left_child().get_root_val()=='and':
            tree.set_root_val('and')
            tree.insert_right('or')
            tree.get_left_child().set_root_val('or')
            tree.get_right_child().left_child=tree.get_left_child().get_right_child()
            tree.get_left_child().right_child=tree.get_right_child().get_right_child()
        distribute(tree.get_left_child())
        distribute(tree.get_right_child())
            
def cut(tree):
    if tree:
        if tree.get_root_val()=='and':
            return cut(tree.get_left_child())+cut(tree.get_right_child())
        else:
            return [tree]


# In[282]:

def evaluate(tree,model):
    leftC = tree.get_left_child()
    rightC = tree.get_right_child()
    if leftC and rightC:        
        if tree.get_root_val()=='and':
            return evaluate(leftC,model) and evaluate(rightC,model)
        elif tree.get_root_val()=='not':
            return (None if evaluate(rightC,model)==None else not evaluate(rightC,model))
        else:
            return evaluate(leftC,model) or evaluate(rightC,model)
    elif tree.get_root_val() not in model.keys():
        return None
    else:
        return model[tree.get_root_val()]


# In[283]:

def DPLL_S(s):
    clauses=s
    symbols=[]
    for i in s:
        for j in i.symbols:
            if j not in symbols:
                symbols.append(j)
    return DPLL(clauses,symbols,{})


# In[284]:

def DPLL(clauses,symbols,model):
    unknown=[]
    for i in clauses:
        result=evaluate(i.val,model)
        if result is False:
            return False
        if result is not True:
            unknown.append(i)
    if not unknown:
        return model
    p,value=find_pure_symbol(symbols,unknown)
    if p:
        symbols.remove(p)
        return DPLL(clauses, symbols,dict(model, **{p:value}))
    
    p,value=find_unit_clause(clauses,model)
    if p:
        symbols.remove(p)
        return DPLL(clauses,symbols,dict(model, **{p:value}))
    if not symbols:
        raise TypeError("Argument should be of the type Expr.")
        
    p=symbols[0]
    rest=symbols[1:]
    
    return DPLL(clauses,rest,dict(model, **{p:True})) or DPLL(clauses,rest,dict(model, **{p:False}))


# In[285]:

def find_pure_symbol(symbols,clauses):
    if not symbols:
        return None,None
    for i in symbols:
        pos=False
        neg=False
        for c in clauses:
            exp=c.inorderlist(c.val).split()            
            for j in range(len(exp)):                
                if exp[j]==i:
                    if j==0 or exp[j-1]!='not':
                        pos=True
                    else:
                        neg=True
        if pos!=neg:
            return i, pos
    return None,None


# In[286]:

def find_unit_clause(clauses,model):
    p=None
    value=None
    for clause in clauses:
        p,value=unit_clause_assign(clause,model)
        if p:
            return p, value            
    return None,None

def unit_clause_assign(clause,model):
    exp=clause.inorderlist(clause.val).split()
    
    p,value=None,None
    i=0
    while i <len(exp):
        if exp[i]!='and' and exp[i]!='or' and exp[i]!='False':
            if exp[i]=='not':
                sym=exp[i+1]
                pos=False
                i+=1
            else:
                sym=exp[i]
                pos=True
            if sym in model.keys():
                if model[sym]==pos:
                    return None,None
            elif p:
                return None,None
            else:
                p,value=sym,pos
            i+=1
        else:
            i+=1
    return p,value


# In[287]:

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


# In[288]:

def connection(KB,alpha):
    # create KB
    KB1=[]
    for s in KB:
        temp=converter(s)
        rule=sentence()
        rule.creatS(temp)
        clauses=CNF(rule)
        KB1+=clauses
    #create alpha
    temp=converter(alpha)
    alpha1=sentence()
    alpha1.creatS(temp)       
    
    s1=KB1+[alpha1]
    result1=DPLL_S(s1)
    if result1==False:
        return False
    else:
        temp=converter(alpha)
        temp='( not '+temp+' )'
        alpha2=sentence()
        alpha2.creatS(temp)
        s2=KB1+[alpha2]
        result2= DPLL_S(s2)       
        if result2==False:
            return True
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

