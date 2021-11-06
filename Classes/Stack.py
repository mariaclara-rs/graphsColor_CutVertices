from StackNode import StackNode

class Stack:
    def __init__(self):
        self.head = None
     
    def is_empty(self):
        return self.head == None
     
    def push(self,head):
        if self.head == None:
            self.head = StackNode(head,None)
        else:
            newnode = StackNode(head,self.head)
            self.head = newnode
     
    def pop(self):
        if self.is_empty():
            return None
        else:
            aux = self.head
            self.head = self.head.next
            aux.next = None
            return aux
     
    def top(self):
        if self.is_empty():
            return None
        else:
            return self.head