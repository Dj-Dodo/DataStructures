from string import ascii_letters
import time
import numpy as np
import random

vector = []
temp = 0

class Node:
    def __init__(self, order_place):
        self.value = ''
        self.left = None
        self.right = None
        self.order_place = order_place


class BDD:
    existing_nodes = {}

    def __init__(self, var_num, nodes):
        self.vars = var_num                     #pocet premennych   
        self.nodes = nodes                      #pocet uzlov
        self.root = None    

    def BDD_create(self, function, order):
        self.root = Node(0)
        self.root.value = function
        my_order = []
        for j in range(self.vars):
            my_order.append(order[j])

        self.split_function(self.root, function, 0, my_order)

        return self.root

    def BDD_use(self, tree, input_seq):
        try:
            for j in range(len(input_seq)):
                if input_seq[j] == '0':
                    tree = tree.left

                elif input_seq[j] == '1':
                    tree = tree.right

                else:
                    return -1

            if tree.value != '1' and tree.value != '0':  # ina hodnota ako 0, 1
                return -1
            return tree.value

        except AttributeError:
            return -1
    
    def split_function(self, diagram, function, order_place, order):
        global temp
        new_left_node = None
        new_right_node = None

        function = function.replace(' ', '')
        function = function.split('+')

        fun = []
        for j in function:
            j = j.split('.')
            fun.append(j)

        new_left_node = Node(order_place + 1)
        new_right_node = Node(order_place + 1)

        for piece in fun:
            if order[diagram.order_place].upper() in piece:                                     #ak sa pismena nachadzaju v podvyraze, ide sa doprava
                if new_right_node.value != '':
                    new_right_node.value += '+'

                for character in piece:
                    if character != order[diagram.order_place].upper():
                        if new_right_node.value != '' and new_right_node.value[-1] != '+':
                            new_right_node.value += '.' + character

                        else:
                            new_right_node.value += character

                    elif len(piece) == 1:
                        new_right_node.value += '1'

            elif order[diagram.order_place].lower() in piece:                                   #ak sa negovane pismena nachadzaju v podvyraze, ide sa dolava
                if new_left_node.value != '':
                    new_left_node.value += '+'

                for character in piece:

                    if character != order[diagram.order_place].lower():

                        if new_left_node.value != '' and new_left_node.value[-1] != '+':
                            new_left_node.value += "." + character
                        else:
                            new_left_node.value += character

                    elif len(piece) == 1:
                        new_left_node.value += '1'  

            else:                                                                               #ak sa vo vyraze nenachadza pismenko, ide sa aj dolava aj doprava
                if new_right_node.value != '':
                    new_right_node.value += "+"
                if new_left_node.value != '':
                    new_left_node.value += "+"
                for character in piece:

                    if new_right_node.value != '' and new_right_node.value[-1] != '+':
                        new_right_node.value += "." + character

                    else:
                        new_right_node.value += character

                    if new_left_node.value != '' and new_left_node.value[-1] != '+':
                        new_left_node.value += "." + character

                    else:
                        new_left_node.value += character

        # REDUCE
        keys = self.existing_nodes.keys()

        # right node
        if new_right_node.value in keys:
            diagram.right = self.existing_nodes[new_right_node.value]
            
        else:
            diagram.right = new_right_node
            if diagram.right.value != '1' and diagram.right.value != '0' and diagram.right.value != '':
                self.existing_nodes[diagram.right.value] = diagram.right

        # left node
        if new_left_node.value in keys:
            diagram.left = self.existing_nodes[new_left_node.value]
            
        else:
            diagram.left = new_left_node
            if diagram.left.value != '1' and diagram.left.value != '0' and diagram.left.value != '':
                self.existing_nodes[diagram.left.value] = diagram.left

        # diagram.left = new_left_node
        # diagram.right = new_right_node
                

        # //REDUCE

        if len(order) - 2 != order_place:                                                       #rekurzivne volanie lavej strany
            self.split_function(diagram.left, diagram.left.value, order_place + 1, order)

        else:
            if diagram.left.value != '1' and diagram.left.value != '0':
                self.existing_nodes[diagram.left.value] = diagram.left

            self.create_vector(diagram, order_place)                                            #ked sme dosli na koniec, ideme robit vektor
            return

        if len(order) - 2 != order_place:                                                       #rekurzivne volanie pravej strany
            self.split_function(diagram.right, diagram.right.value, order_place + 1, order)

        else:
            if diagram.right.value != '1' and diagram.right.value != '0':
                self.existing_nodes[diagram.right.value] = diagram.right

            self.create_vector(diagram, order_place)                                            #ked sme dosli na koniec, ideme robit vektor                                               
            return

    def create_vector(self, diagram, order_place):
        global temp
        new_left_left = Node(order_place + 2)
        new_left_right = Node(order_place + 2)
        new_right_left = Node(order_place + 2)
        new_right_right = Node(order_place + 2)
        
        # vytvarame lave strany vektora
        if diagram.left.value == '1':
            new_left_left.value = '1'
            new_left_right.value = '1'
            vector.append(1)
            vector.append(1)

        elif diagram.left.value == '0':
            new_left_left.value = '0'
            new_left_right.value = '0'
            vector.append(0)
            vector.append(0)

        else:
            pom_int = 0
            pom_bool = True
            for j in range(len(diagram.left.value)):
                if diagram.left.value[j] == '1':
                    new_left_left.value = '1'
                    new_left_right.value = '1'
                    vector.append(1)
                    vector.append(1)
                    pom_bool = False
                    pom_int = 0
                    break

                if 96 < ord(diagram.left.value[j]) < 123:
                    pom_int -= 1

                elif 64 < ord(diagram.left.value[j]) < 91:
                    pom_int += 1

                else:
                    continue
            if pom_int > 0:
                new_left_left.value = '0'
                new_left_right.value = '1'
                vector.append(0)
                vector.append(1)

            elif pom_int < 0:
                new_left_left.value = '1'
                new_left_right.value = '0'
                vector.append(1)
                vector.append(0)

            elif pom_bool:
                new_left_left.value = '1'
                new_left_right.value = '1'
                vector.append(1)
                vector.append(1)
                                                                                        #vytvarame prave strany vektora
        if diagram.right.value == '1':
            new_right_left.value = '1'
            new_right_right.value = '1'
            vector.append(1)
            vector.append(1)

        elif diagram.right.value == '':
            new_right_left.value = '0'
            new_right_right.value = '0'
            vector.append(0)
            vector.append(0)

        else:
            pom_int = 0
            pom_bool = True
            for j in range(len(diagram.right.value)):
                if diagram.right.value[j] == '1':
                    new_right_left.value = '1'
                    new_right_right.value = '1'
                    vector.append(1)
                    vector.append(1)
                    pom_bool = False
                    pom_int = 0
                    break

                if 96 < ord(diagram.right.value[j]) < 123:
                    pom_int -= 1

                elif 64 < ord(diagram.right.value[j]) < 91:
                    pom_int += 1

                else:
                    continue

            if pom_int > 0:
                new_right_left.value = '0'
                new_right_right.value = '1'
                vector.append(0)
                vector.append(1)

            elif pom_int < 0:
                new_right_left.value = '1'
                new_right_right.value = '0'
                vector.append(1)
                vector.append(0)

            elif pom_bool:
                new_right_left.value = '1'
                new_right_right.value = '1'
                vector.append(1)
                vector.append(1)

        # REDUCE
        keys = self.existing_nodes.keys()

        # left-left
        if new_left_left.value in keys:
            diagram.left.left = self.existing_nodes[new_left_left.value]
            temp +=1

        else:
            diagram.left.left = new_left_left
            self.existing_nodes[diagram.left.left.value] = diagram.left.left

        # left-right
        if new_left_right.value in keys:
            diagram.left.right = self.existing_nodes[new_left_right.value]
            temp +=1

        else:
            diagram.left.right = new_left_right
            self.existing_nodes[diagram.left.right.value] = diagram.left.right

        # right-left
        if new_right_left.value in keys:
            diagram.right.left = self.existing_nodes[new_right_left.value]
            temp +=1

        else:
            diagram.right.left = new_right_left
            self.existing_nodes[diagram.right.left.value] = diagram.right.left

        # right-right
        if new_right_right.value in keys:
            diagram.right.right = self.existing_nodes[new_right_right.value]
            temp +=1

        else:
            diagram.right.right = new_right_right
            self.existing_nodes[diagram.right.right.value] = diagram.right.right

        return


if __name__ == '__main__':
    
    row = random.randint(0,3)
    f = open("bool_functions.txt", "r")
    funct = ''
    for i in range(0,3):
        # riadok=f.readline()
        riadok = f.readline()
        
        if i+1==row:
            funct = riadok.replace('\n','')
            break
            

    print(funct)

    #ORDER
    chars = []

    for i in range(len(funct)-1):
        char = funct[i].upper()
        if(funct[i] == '+' or funct[i] == ' ' or funct[i] == '.'):
            continue
        elif char in chars:
            continue
        else:
            chars.append(char)

    n = len(chars)

    order = []

    bdd = BDD(n, (2 ** n) + 1)  # to-do: prerobit (2 ** n) + 1 (zistit, ci je to true)
    print("Znaky ktore sa nachadzaju vo funkcii:")

    chars.sort()
    print(chars)
    for i in range(n):
        order.append(input(f"Zadaj znak c. {i+1}: "))
    print(order)

    time1_create = time.time()
    bdd_tree = bdd.BDD_create(funct, order)
    time2_create = time.time()

    print("---------------------------------------")
    print("Vector:", end=' ')

    vector_string = ""
    for i in range(len(vector)):
        vector_string += str(vector[i]) + ' '
    print(vector_string)
    print(len(vector))
    print("BDD_Use:", end=' ')

    time1_use = time.time()

    pom=0                                                                           #testovanie BDD use
    for binary in range(0,2**n):
        pom = np.binary_repr(binary, width=n)

        result = bdd.BDD_use(bdd_tree, pom)
        
        if(int(result) != vector[binary]):
            break

    time2_use = time.time()
    #print(result)
    nodes =  (2**n)+1

    print(f"Time of BDD_Create: {time2_create - time1_create:.10f}")
    print(f"Time of BDD_Use: {time2_use - time1_use:.10f}")
    print("Number of nodes: ",nodes)
    print(f"Percentage of reduction: {(temp / nodes) * 100:.2f}%")



