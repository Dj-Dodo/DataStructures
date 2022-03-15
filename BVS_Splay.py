import time
import random

class Node:                                 #trieda Node a jej zakladna inicializacia udajov

    def __init__(self, hodnota):
        self.hodnota = hodnota
        self.left = None
        self.right = None
        self.parent = None

class SplayStrom:

    def __init__(self):             #inicializacia hlavneho rootu
        self.root = None

    def rotacia_vlavo(self, x):
        y=x.right
        x.right = y.left
        if(y.left !=None):
            y.left.parent = x
        y.parent = x.parent
        
        if(x.parent == None):
            self.root = y
        elif(x == x.parent.left):
            x.parent.left = y
        else:
            x.parent.right = y
        
        y.left = x
        x.parent = y

    def rotacia_vpravo(self, x):
        y=x.left
        x.left = y.right
        if(y.right !=None):
            y.right.parent = x
        y.parent = x.parent

        if(x.parent == None):
            self.root = y
        elif(x == x.parent.right):
            x.parent.right = y
        else:
            x.parent.left = y

        y.right = x
        x.parent = y

    def splay(self, n):
        while n.parent != None:                         #cyklus while pojde dovtedy dokym noda nebude root
            if(n.parent == self.root):                  #ked dana noda rootom, staci spravit jednu rotaciu, a ak nie je, tak dve
                if(n==n.parent.left):
                    self.rotacia_vpravo(n.parent)
                else:
                    self.rotacia_vlavo(n.parent)
            else:
                par = n.parent              #parent n-ka
                gpar = par.parent           #grandparent n-ka
                if(n.parent.left == n and par.parent.left == par):
                    self.rotacia_vpravo(gpar)
                    self.rotacia_vpravo(par)
                elif(n.parent.right == n and par.parent.right == par):
                    self.rotacia_vlavo(gpar)
                    self.rotacia_vlavo(par)
                elif(n.parent.right == n and par.parent.left == par):
                    self.rotacia_vlavo(par)
                    self.rotacia_vpravo(gpar)
                else:
                    self.rotacia_vpravo(par)
                    self.rotacia_vlavo(gpar)

    #def search(self, n, x):                 #funkcia search na vyhladavanie v strome 
        #if(x==n.hodnota):
            #self.splay(n)          
            #return n
        #elif(x<n.hodnota):                  #pokial je hladane cislo mensie ako hodnota nody, tak sa posunieme dolava
            #return self.search(n.left, x)
        #elif(x>n.hodnota):                  #pokial je hladane cislo vacsie ako hodnota nody, posunieme sa doprava
            #return self.search(n.right, x)
        #else:
            #return None

    def search(self, x, rootNode=None):
        if rootNode is None:
            rootNode = self.root

        if x == rootNode.hodnota:
            self.splay(rootNode)
            return rootNode
        elif(x<rootNode.hodnota):
            return self.search(x,rootNode.left)
        elif(x>rootNode.hodnota):
            return self.search(x, rootNode.right)
        else:
            return None

    
    def insert(self, n):                            #dokoncit jakoooo
        rootNode = self.root
        parent = None

        if(self.root is None):                      #ak nemame root, tak nám ho spraví
            self.root = n
            return
        while rootNode is not None:                 #hladame poziciu kde dame novu nodu
            parent = rootNode
            if (n.hodnota < rootNode.hodnota):      #ak je hodnota mensia ako root hodnota, tak davame dolava
                rootNode = rootNode.left
            else:                                   #inak davame doprava
                rootNode = rootNode.right
        n.parent = parent
        if(parent is None):                         #davame nodu tak dam patri, bud ako root, alebo dolava/doprava
            rootNode = n
        elif(n.hodnota < parent.hodnota):
            parent.left = n
        else:
            parent.right = n
        self.splay(n)

    def maximum(self, x):                   #funkcia, ktora bude prechadzat strom dovtedy, dokym nedojde na Nodu, ktora je uplne vpravo 
        while x.right != None:
            x = x.right
        return x

    def delete(self, n):
        self.splay(n)                                               #na zaciatok premiestnime nodu do korena pomocou funkcie splay

        lavy_substrom = SplayStrom()                                #rozdelime si strom na lavy substrom
        lavy_substrom.root = self.root.left
        if(lavy_substrom.root is not None):
            lavy_substrom.root.parent = None
        
        pravy_substrom = SplayStrom()                               #rozdelime si strom na pravy substrom
        pravy_substrom.root = self.root.right
        if(pravy_substrom.root is not None):
            pravy_substrom.root.parent = None
        
        if(lavy_substrom.root is not None):
            max = self.maximum(lavy_substrom.root)                  #zistime si maximum laveho podstromu
            lavy_substrom.splay(max)                                #najdene maximum nastavime ako root stromu
            lavy_substrom.root.right = pravy_substrom.root          #pravu cast stromu len pripojime k lavemu
            self.root = lavy_substrom.root
        else:                                                       #ak lavy strom neexistuje , tak pravy substrom spravime stromom 
            self.root = pravy_substrom.root


#---------------------------------------------------------------
#--------------------------TESTOVAC-----------------------------

velkost_prvkov = 100000
hodnoty = []

def naplnenie_hodnot(velkost):
    for i in range(velkost):
        hodnoty.append(random.randint(0,1000))
        
naplnenie_hodnot(velkost_prvkov)

strom = SplayStrom()

print("Pocet testovacich prvkov: ",velkost_prvkov)

#testovac na insert

time1 = time.time()


for i in range(velkost_prvkov):
    a = Node(hodnoty[i])
    strom.insert(a)

print("Strom uspesne insertol prvky za cas: ", time.time()-time1)

#testovac na search

time1 = time.time()
for j in range(velkost_prvkov):
    b = Node(hodnoty[j])
    strom.search(hodnoty[j])


print("Strom uspesne vyhladal prvky za cas: ", time.time() - time1)

#testovac na delete

time1 = time.time()

for k in range(velkost_prvkov):
    c = Node(hodnoty[k])
    strom.delete(c)

print("Strom uspesne deletol prvky za cas: ", time.time()-time1)
