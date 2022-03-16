from copy import deepcopy
import random
import time

class Node:
    def __init__(self, hodnota):                #inicializacia nody
        self.hodnota = hodnota
        self.left = None
        self.right = None
        self.height = 1
        self.parent = None

class AVL:

    def __init__(self):                         #inicializacia root-u
        self.root = None

    def height(self, Node):                     #pomocna funkcia na vysku             
        if not Node:
            return 0
        else:
            return Node.height
    
    def balance(self, Node):                    #funckia na vyvazenie stromu
        if not Node:
            return 0
        else:
            return self.height(Node.left) - self.height(Node.right)
    
    def maximum(self, a, b):
        if(a > b):
            return a
        else:
            return b
    
    def minihodnota(self, n):
        if(n is None or n.left is None):
            return n
        else:
            return self.minihodnota(n.left)

    def rotacia_vlavo(self, x):
        y = x.right
        x.right = y.left
        if(y.left is not None):         #ak ma y lavy substrom, nastavime x hodnotu ako parenta laveho y substromu
            y.left.parent = x
        
        if(x.parent is None):           #ak parent x je NULL, y bude root stromu
            self.root = y
        elif(x is x.left.parent):
            x.left.parent = y
        else:
            x.right.parent = y
        x = y.left
        y = x.parent

        x.height = 1 + self.maximum(self.height(x.left), self.height(x.right))          #nastavime vysky x a y
        y.height = 1 + self.maximum(self.height(y.left), self.height(y.right))

    def rotacia_vpravo(self, x):
        y = x.left
        x.left = y.right
        if(y.right is not None):            #ak ma y pravy substrom, nastavime x hodnotu ako parenta praveho y substromu
            y.right.parent = x
        if(x.parent is None):               #ak parent x je NULL, y bude root stromu
            self.root = y
        elif(x is x.right.parent):
            x.right.parent = y
        else:
            x.left.parent = x
        x = y.right
        y = x.parent

        x.height = 1 + self.maximum(self.height(x.left), self.height(x.right))          #nastavime vysky x a y 
        y.height = 1 + self.maximum(self.height(y.left), self.height(y.right))

    def search(self, x, rootNode=None):                         #funkcia na vyhladavanie hodnoty v avl strome
        
        if rootNode is None:
            rootNode = self.root
        
        if x == rootNode.hodnota:                           
            return rootNode
        elif(x<rootNode.hodnota):
            return self.search(x, rootNode.left)
        elif(x>rootNode.hodnota):
            return self.search(x, rootNode.right)
        else:
            return None

    def insert(self, n, rootNode):
        newNode = Node(n)
    
        if rootNode is None:
            rootNode = newNode
            return rootNode
        elif(n < rootNode.hodnota):
            rootNode.left = self.insert(n, rootNode.left)
            return rootNode
        elif(n > rootNode.hodnota):
            rootNode.right = self.insert(n, rootNode.right)
            return rootNode

        newNode.height += self.maximum(self.height(newNode.left), self.height(newNode.right))

        balanceFaktor = self.balance(self.root)             #updatneme balance faktor
                                                             #ak su nody nevybalancovane , tak ich vybalancujeme  
        if(balanceFaktor > 1):                              #ak je BF vacsi ako 1, znamena to ze vyska laveho substromu je vacsia ako praveho substromu 
            if(newNode<newNode.left.hodnota):                           #ak je nova noda mensia ako hodnota laveho childu, pouzijeme rotaciu vpravo
                return self.rotacia_vpravo(newNode)
            else:
                newNode.left = self.rotacia_vlavo(newNode.left)         #inak pouzijeme left-right rotaciu
                return self.rotacia_vpravo(newNode)
        elif(balanceFaktor < -1):                           #ak je BF mensi ako -1 , tak vyska praveho substromu je vacsia ako laveho substromu
            if(newNode>newNode.right.hodnota):                          #ak je nova noda vacsia ako hodnota praveho childu, pouzijeme rotaciu vlavo
                return self.rotacia_vlavo(newNode)
            else:                                           #inak pouzijeme right-left rotaciu
                newNode.right = self.rotacia_vpravo(newNode.right)
                return self.rotacia_vlavo(newNode)
        return newNode

    def delete(self, n, value):
        if(n is None):
            return n
        elif(value < n.hodnota):
            n.left = self.delete(n.left, value)
        elif(value > n.hodnota):
            n.right = self.delete(n.right, value)
        else:
            if(n.left is None):
                pom = n.right
                n = None
                return pom
            elif(n.right is None):
                pom = n.left
                n = None
                return pom
            pom = self.minihodnota(n.right)
            n.hodnota = pom.hodnota
            n.right = self.delete(n.right, pom.hodnota)
        if(n is None):
            return n

        balanceFaktor = self.balance(n)
        if(balanceFaktor > 1):
            if(self.balance(n.left)>=0):
                return self.rotacia_vpravo(n)
            else:
                n.left = self.rotacia_vlavo(n.left)
                return self.rotacia_vpravo(n)
        if(balanceFaktor < -1):
            if(self.balance(n.right) <=0 ):
                return self.rotacia_vlavo(n)
            else:
                n.right = self.rotacia_vpravo(n.right)
                return self.rotacia_vlavo(n)
        return n

    def preorder(self, root):
        if root is None:
            return 
        print(root.hodnota)
        self.preorder(root.left)
        self.preorder(root.right)

#Tree = AVL()
#rt = None
#rt = Tree.insert(3, rt)
#rt = Tree.insert(5, rt)
#rt = Tree.insert(7, rt)
#print("PREORDER")
#Tree.preorder(rt)
#rt = Tree.insert(1, rt)
#rt = Tree.insert(2, rt)
#print("PREORDER")
#Tree.preorder(rt)
#rt = Tree.insert(4, rt)
#rt = Tree.insert(6, rt)
#rt = Tree.delete(rt, 7)
#rt = Tree.insert(8, rt)
#rt = Tree.insert(9, rt)
#print("PREORDER")
#Tree.preorder(rt)
#rt = Tree.delete(rt, 3)
#print("PREORDER")
#Tree.preorder(rt)
#-------------------------------------------------------------
#---------------------TESTOVAC--------------------------------
#treba napriklad vlozit 100 000 a potom z toho napriklad 50k vymazat atd atd

velkost_prvkov = 1000000
hodnoty = []

def naplnenie_hodnot(velkost):
    for _ in range(velkost):
        hodnoty.append(random.randint(0,1000))

naplnenie_hodnot(velkost_prvkov)

Tree = AVL()

print("Pocet testovacich prvkov: ",velkost_prvkov)

#testovac na insert

time1 = time.time()

a=None
for i in range(velkost_prvkov):
    Node(hodnoty[i])
    a = Tree.insert(hodnoty[i], a)

time2 = time.time()
print("Strom uspesne insertoval prvky za cas: ", time2-time1)

#testovac na search

#time1 = time.time()

#b=None
#for j in range(velkost_prvkov):
    #Node(hodnoty[j])
    #b = Tree.search(hodnoty[j], b)

#time2=time.time()
print("Strom uspesne vyhladal prvky v case: ",time2-time1)

#testovac na delete

time1 = time.time()

c=None
for k in range(velkost_prvkov):
    Node(hodnoty[k])
    c = Tree.delete(c, hodnoty[k])

time2 = time.time()
print("Strom uspesne deletol prvky za cas: ", time2-time1)
