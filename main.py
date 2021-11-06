from Head import Head
from Vertex import Vertex
from List import List
from tkinter import Entry, Button, Label, Tk
import networkx as nx
from pyvis.network import Network
import webbrowser
import os

count = 0
NodesTree = []
vet_grau = []
window = Tk()


def clear_console():
    command = "clear"
    if os.name in ("nt", "dos"):  # If Machine is running on Windows, use cls
        command = "cls"
    os.system(command)


def connection_exists(c, connections):
    for i in range(0, len(connections)):
        if c[0] in connections[i] and c[1] in connections[i]:
            return True
    return False


label = Label()


def show_label(Li):
    i = 4
    L = Li._list
    while L != None:
        l = L.vertex
        global label
        label = Label(window, text="{} -> ".format(L.name))
        label.grid(column=2, row=i)
        c = 3
        while l != None:
            label = Label(window, text="{} -> ".format(l.name))
            label.grid(column=c, row=i)
            c += 1
            l = l.next
        i += 1
        L = L.next


def add_connection(c, connections, L):
    clear_console()
    if len(c.get()) == 2:
        connections = []
        connections.append([c.get()[0].upper(), c.get()[1].upper()])
        connections.append([c.get()[1].upper(), c.get()[0].upper()])
        init_graph(L, connections)
        show_label(L)
        # show(L._list)
        c.delete(0, "end")
    else:
        print("conexao inválida!")


def menu():
    window.title("Grafos - Vertices Input")
    header_title = Label(
        window, text="Insira as ligações. ex: ae", font=("calibre", 14, "bold")
    )
    c_entry = Entry(window)

    connections = []
    L = List()
    btn_add = Button(
        window,
        text="Adicionar conexão",
        command=lambda: add_connection(c_entry, connections, L),
    )

    btn_start = Button(
        window,
        text="Iniciar",
        command=lambda: init_graph(L, connections),
    )

    btn_dfs = Button(
        window,
        text="Corte dos Vertices",
        command=lambda: algorithm_cut(L),
    )

    btn_color = Button(
        window,
        text="Coloração",
        command=lambda: (algorithm_coloring(L), depth(L._list)),
    )

    """ btn_reset = Button(
        window,
        text="Resetar",
        command=lambda: reset(L),
    ) """

    header_title.grid(column=0, row=0)
    c_entry.grid(column=0, row=1)
    btn_add.grid(column=0, row=2)
    btn_start.grid(column=1, row=2)
    btn_dfs.grid(column=0, row=3)
    # btn_reset.grid(column=0, row=4)
    btn_color.grid(column=1, row=3)

    window.mainloop()


""" def reset(L):
    L = List()
    global count
    count = 0
    global NodesTree
    NodesTree = []
    global vet_grau
    vet_grau = []
    global label
    label.destroy() """


def init_graph(li, connections):  # li é do tipo lista
    for r in connections:
        head_li = li.find_head(r[0])
        if head_li == None:
            head_li = Head(r[0])
            li.insert(head_li)
        head_li.insert_vertex(Vertex(r[1]))
    li.connections()
    show(li._list)
    show_graph(li._list, "")


def show(L):
    while L != None:

        print("Nome: {} Vetor: {} Min: {}".format(L.name, L.vet,L.min))
        # print("Nome: {} Vetor: {} Pai: {}".format(L.name, L.vet[0], L.father.name))
        l = L.vertex
        while l != None:
            print("-> " + l.name)
            l = l.next
        L = L.next


def show_color(L):
    while L != None:
        print("Nome: {} Color: {}".format(L.name, L.color))
        # print("Nome: {} Vetor: {} Pai: {}".format(L.name, L.vet[0], L.father.name))
        l = L.vertex
        while l != None:
            print("-> " + l.name)
            l = l.next
        L = L.next


def depth(L):
    global count
    count = 0
    Laux = L
    Laux.father = Laux
    while Laux != None:
        if Laux.color == 0:  # para todo vértice que ainda não foi visitado (cor==0)
            # L = Cabeca dos head #Laux = Head de uma linha
            dfs(L, Laux)
        Laux = Laux.next


# 1º valor do vetor
# L = lista    h = vertice
def dfs(L, h):
    global count
    count += 1
    global NodesTree
    NodesTree.append(h.name)
    print(h.name)
    h.vet[0] = count
    h.color = 2  # nó visitado
    print("Vertice: {} - Ordem de visitação: {}".format(h.name, h.vet[0]))
    vt = h.vertex
    while vt != None:
        if vt.head.color == 0:
            vt.head.father = h
            dfs(L, vt.head)
            print("BACKTRACKING - Vertice: {}".format(h.name))
        vt = vt.next
    h.color = 3  # não existe mais nós adajacentes não visitados


def show_graph(L, id):
    G = nx.Graph()
    L2 = L
    while L != None:
        G.add_node(L.name, title=L.vet, group=L.color)
        L = L.next

    while L2 != None:
        l = L2.vertex
        while l != None:
            G.add_edge(L2.name, l.name, group=l.head.color)
            l = l.next
        L2 = L2.next

    net = Network(notebook=True)
    net.from_nx(G)
    net.show(id + "-graph.html")
    filename = "file:///" + os.getcwd() + "/" + id + "-graph.html"
    webbrowser.open_new_tab(filename)


def tree(L):
    LTree = List()
    for i in range(len(NodesTree)):
        node = L.find_head(NodesTree[i])
        nn = Head(node.name)
        nn.color = node.color
        nn.vet = node.vet
        # encontrar pai de nn
        LTree.insert(nn)
        father_nn = LTree.find_head(node.father.name)
        nn.father = father_nn
        if nn != father_nn:
            vertexnew = Vertex(father_nn.name)
            nn.insert_vertex(vertexnew)
            vertexnew = Vertex(nn.name)
            father_nn.insert_vertex(vertexnew)
            # print("{} - {}".format(nn.name, father_nn.name))

    return LTree


# 2º valor do vetor
def dotted(L, LTree):
    Li = L
    Lt = LTree
    lost_child = ""
    #compara as duas listas para verificar as ligacoes perdidas
    while Li != None:
        li = Li.vertex
        min = 0
        while li != None:
            lt = Lt.vertex
            while lt != None and li.name > lt.name:
                lt = lt.next
            if lt == None or li.name != lt.name:
                if min == 0 or li.head.vet[0] < min:
                    min = li.head.vet[0]
                    lost_child = li.head.name
                # print("no head: "+Li.name+" tenho no original: "+li.name+" mas não tenho na ltree")
            li = li.next
        if min > 0:
            print(
                "Vertice {}\n Conexão perdida com o vértice {} (ordem de visitação {}) ".format(
                    Li.name, lost_child, min
                )
            )
        Li.vet[1] = min
        Li = Li.next
        Lt = Lt.next


# 3º valor do vetor
def step3(Ltree):
    print("Step 3")
    show(Ltree._list)
    i = len(NodesTree) - 1

    aux = []
    while i >= 0:
        node = Ltree.find_head(NodesTree[i])  # node é do tipo head
        if node!=None:
            if node.number_vetices()>1 or i==0:
                l = node.vertex
                while l!=None:
                    if node.father.name != l.name:
                        aux.append(l.head.min)
                    l = l.next
                node.vet[2] = min(aux)
                aux = []
                for k in range(len(node.vet)):
                    if node.vet[k]!=0:
                        aux.append(node.vet[k])
                node.min = min(aux)
                aux = []
                
            else:
                aux = []
                node.vet[2] = 0
                for k in range(len(node.vet)):
                    if node.vet[k]!=0:
                        aux.append(node.vet[k])

                node.min = min(aux)

        i -= 1
"""     
def step3(Ltree):
    i = len(NodesTree) - 1
    while i >= 0:
        node = Ltree.find_head(NodesTree[i])  # node é do tipo head
        if node.vet[2] == 0:
            if node.vet[1] > 0:
                node.vet[2] = min(node.vet[0], node.vet[1])
            else:
                node.vet[2] = node.vet[0]
        if node.father.vet[2] == 0 or node.vet[2] < node.father.vet[2]:
            node.father.vet[2] = node.vet[2]
        i -= 1
 """
# encontrar vértices de corte
def cut_vertices(LTree):
    Lt = LTree._list
    vc = []
    while Lt != None:
        if Lt.number_vetices() > 1: #nao entra se for raiz com 1 filho ou folha
            lv = Lt.vertex
            while lv != None:
                aux = []
                # print(lv.head.father.name+" - "+Lt.name)
                if lv.head.father.name == Lt.name: #verifica se o elemento é pai

                    """ for k in range(len(lv.head.vet)):
                        if lv.head.vet[k]!=0:
                            aux.append(lv.head.vet[k]) """
                    if lv.head.min >= Lt.vet[0]:
                        vc.append(Lt.name)
                    """if lv.head.vet[1] != 0:
                        if (
                            min(min(lv.head.vet[0], lv.head.vet[1]), lv.head.vet[2])
                            >= Lt.vet[0]
                        ):
                            vc.append(Lt.name)
                    elif min(lv.head.vet[0], lv.head.vet[2]) >= Lt.vet[0]:
                        vc.append(Lt.name)"""


                lv = lv.next
        Lt = Lt.next
    return vc


def algorithm_cut(L):
    clear_console()
    print("\n- Busca em profundidade: \n")
    # definir ordem de visitação e definir quem é pai de quem
    depth(L._list)
    print("\n- Lista de adjacencia que representa o grafo: \n")
    show(L._list)
    # contruir novo" graf o - arvore de visitação
    print("\n- Lista de adjacencia que representa a árvore de visita: \n")
    LTree = tree(L)
    LTree.connections()
    show_graph(LTree._list, "cut")
    show(LTree._list)
    # preencher segundo campo do vetor - definir quais da conexões perdidas tem menor ordem de visitação
    dotted(L._list, LTree._list)
    # preencher terceiro campo do vetor
    step3(LTree)
    print("\n- Lista de adjacencia finalizada: \n")
    show(LTree._list)
    # determinar vértices de corte
    vc = cut_vertices(LTree)
    # print("------")
    # show(L._list)
    print("\nVértices de corte: {}\n".format(len(vc)))
    for i in range(len(vc)):
        print(vc[i])


# maior primeiro
def algorithm_coloring(L):
    clear_console()
    # criando lista com vertices ordenados (decrescente) pelo grau
    print("\n- Coloração do Grafo: \n")
    print("\n- Lista de adjacencia: \n")
    show(L._list)
    global vet_grau 
    Lt = L._list
    while Lt != None:
        Lt.grau = Lt.number_vetices()
        Lt.color = 0
        vet_grau.append([Lt.grau, Lt.name])  # [grau,vertice]
        print("\nVertice: {} Grau: {}".format(Lt.name, Lt.grau))
        Lt = Lt.next
    vet_grau.sort(reverse=True)
    print("\n- Lista dos vértices do grafo organizados em ordem decrescente de grau")
    print(vet_grau)
    color = 1
    # percorrer lista vet_grau
    for i in range(len(vet_grau)):
        print("\nVértice {} em análise".format(vet_grau[i]))
        vname = vet_grau[i][1]
        h = L.find_head(vname)
        if h.color == 0:
            h.color = color
            print("\nVértice: {} Cor: {}".format(h.name, h.color))
            # busca na lista vertices não adjacentes a h para colorir com a mesma cor
            k = i + 1

            v_adj = []
            v_adj.append(h)
            while k < len(vet_grau):
                #vet_grau[k][1] é  adjacente a algumem de v_adj
                find = False
                for item in v_adj:
                    if item.search_vertex(vet_grau[k][1])!=None:
                        find=True
                if not(find) and L.find_head(vet_grau[k][1]).color == 0:
                    L.find_head(vet_grau[k][1]).color = color
                    print("\nVértice {} recebe mesma cor do Vértice {} (pois não são adjacentes)".format(vet_grau[k][1], h.name))
                    v_adj.append(L.find_head(vet_grau[k][1]))
                k += 1

            color += 1
        else:
            print("\nVértice {} já colorido!".format(vet_grau[i]))
    print("\n-Resultado:")
    show_color(L._list)
    show_graph(L._list, "color")


def main():
    L = List()
    # init_graph(L)
    # L.connections()
    # depth(L._list)
    # algorithm_cut(L)
    # algorithm_coloring(L)
    # show(L._list)
    menu()


main()
