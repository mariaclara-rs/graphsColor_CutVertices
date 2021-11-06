class List:
    def __init__(self):
        self._list = None  # raiz da lista

    def find_head(self, nodename):
        node = None
        if self._list != None:
            node = self._list
            while node != None and nodename > node.name:
                node = node.next
            if node != None and nodename != node.name:
                node = None
        return node

    def find_father(self, node):
        Laux = self._list
        while Laux != None and node.name > Laux.name:
            Laux = Laux.next
        if node.name != Laux.name:
            Laux = None
        # print("pai de " + node.name + " e " + Laux.name)
        return Laux

    def connections(self):
        auxH = self._list
        while auxH != None:
            auxV = auxH.vertex
            while auxV != None:
                auxV.head = self.find_head(auxV.name)
                auxV = auxV.next
            auxH = auxH.next

    def insert(self, node):
        if self._list == None:
            self._list = node
        else:
            if node.name < self._list.name:
                node.next = self._list
                self._list = node
            else:
                Laux = self._list
                while Laux.next != None and Laux.next.name < node.name:
                    Laux = Laux.next
                node.next = Laux.next
                Laux.next = node
