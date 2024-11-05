class Node:

    def __init__(self, pos: tuple[int, int], g_cost: float = 0, h_cost: float = 0):

        self.pos: tuple[int, int] = pos

        self.g:float = g_cost
        self.h:float = h_cost
        self.f:float = self.g+self.h

        self.parent:Node = None

    def __lt__(self, other):
        return self.f < other.f
    
    def __gt__(self, other):
        return self.f > other.f
    
    def __repr__(self):
        return str(self.pos)

    def __eq__(self, other):
        return self.pos == other.pos
    
    def __ne__(self, other):
        return self.pos != other.pos
    

if __name__ == "__main__":

    a = Node((0, 0), 0, 100)
    b = Node((0, 0), 0, 5)