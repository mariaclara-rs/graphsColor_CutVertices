class Head:
    def __init__(self, name):
        self.name = name
        self.color = 0
        self.vertex = None
        self.next = None
        self.vet = [0, 0, 0]
        self.father = None
        self.grau = 0
        self.min = 0

    def number_vetices(self):
        v = self.vertex
        n = 0
        while v != None:
            n += 1
            v = v.next
        return n

    def insert_vertex(self, nodev):
        if self.vertex == None:
            self.vertex = nodev
        elif nodev.name < self.vertex.name:
            nodev.next = self.vertex
            self.vertex = nodev
        else:
            Laux = self.vertex
            while Laux.next != None and Laux.next.name < nodev.name:
                Laux = Laux.next
            nodev.next = Laux.next
            Laux.next = nodev

    def search_vertex(self, namevertex):
        aux = self.vertex
        while aux != None and namevertex > aux.name:
            aux = aux.next
        if aux != None and namevertex != aux.name:
            aux = None
        return aux
