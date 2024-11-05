from node import *
import numpy as np
import pygame
import time 
import timeit
class Astar:

    def __init__(self, screen:pygame.Surface, grid, tilesize:int=20):

        self.screen = screen

        self.open = []
        self.closed = []
        self.map_grid = grid

        self.open2 = []
        self.closed2 = []

        self.tz = tilesize

        self.bi = False


    def search(self, start:Node, goal:Node):

        start2 = goal
        goal2 = start

        self.open.append(start)
        self.open2.append(start2)

        while True:

            #----------------------------------------------
            self.open.sort()
            current_node:Node = self.open.pop(0)
            self.closed.append(current_node)
            if current_node == goal:
                return self.reconstruct_path(start, self.closed[-1])
            neighbors:list[Node] = self.get_neighbors(current_node)
            for neighbor in neighbors:
                if neighbor in self.closed:
                    continue
                if neighbor not in self.open:
                    neighbor.parent = current_node
                    self.open.append(neighbor)
                if current_node.parent is None:
                    g = current_node.g + 1
                else:
                    g = abs(current_node.parent.pos[0] - current_node.pos[0]) + abs(current_node.parent.pos[1] - current_node.pos[1])
                h = self.heuristic(neighbor, goal)
                f = g + h
                self.open.sort()
                if neighbor in self.open:
                    neighbor = self.update_node(neighbor, current_node, g, h)
                    if neighbor.f > f:
                        neighbor = self.update_node(neighbor, current_node, g, h)
                else:
                    pass
            #----------------------------------------------
            if self.bi == True:
                self.open2.sort()
                current_node2:Node = self.open2.pop(0)
                self.closed2.append(current_node2)
                if current_node2 == goal2:
                    return self.reconstruct_path(start2, self.closed2[-1])
                neighbors2:list[Node] = self.get_neighbors(current_node2)
                for neighbor in neighbors2:
                    if neighbor in self.closed2:
                        continue
                    if neighbor not in self.open2:
                        neighbor.parent = current_node2
                        self.open2.append(neighbor)
                    if current_node2.parent is None:
                        g = current_node2.g + 1
                    else:
                        g = abs(current_node2.parent.pos[0] - current_node2.pos[0]) + abs(current_node2.parent.pos[1] - current_node2.pos[1])
                    h = self.heuristic(neighbor, goal2)
                    f = g + h
                    self.open2.sort()
                    if neighbor in self.open2:
                        neighbor = self.update_node(neighbor, current_node2, g, h)
                        if neighbor.f > f:
                            neighbor = self.update_node(neighbor, current_node2, g, h)
                    else:
                        pass
            #(---------------------------------------------------------------------)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                if event.type == pygame.QUIT:
                    pygame.quit()


            if self.bi == True:
                for node in self.closed:
                    if node in self.open2:
                        return self.reconstruct_path(start2, self.closed2[-1]) + self.reconstruct_path(start, self.closed[-1])

            for X in range(len(self.map_grid)):
                for Y in range(len(self.map_grid[0])):
                    if grid[X][Y] == 1:
                        pygame.draw.rect(self.screen, "yellow", (Y*self.tz, X*self.tz, self.tz, self.tz))

            for node in self.closed:
                pygame.draw.rect(self.screen, "red", (node.pos[0]*self.tz, node.pos[1]*self.tz, self.tz, self.tz))

            for node in self.closed2:
                pygame.draw.rect(self.screen, "red", (node.pos[0]*self.tz, node.pos[1]*self.tz, self.tz, self.tz))

            for node in self.open:
                pygame.draw.rect(self.screen, "green", (node.pos[0]*self.tz, node.pos[1]*self.tz, self.tz, self.tz))

            for node in self.open2:
                pygame.draw.rect(self.screen, "green", (node.pos[0]*self.tz, node.pos[1]*self.tz, self.tz, self.tz))
            
            pygame.draw.rect(self.screen, "pink", (start.pos[0]*self.tz, start.pos[1]*self.tz, self.tz, self.tz))
            pygame.draw.rect(self.screen, "blue", (goal.pos[0]*self.tz, goal.pos[1]*self.tz, self.tz, self.tz))
            
            pygame.display.flip()
        return None
        

    def reconstruct_path(self, start:Node, goal:Node):
        path = [goal]
        current = goal

        while current.parent != start:
            path.append(current.parent)
            current = current.parent

        for node in path:
            pygame.draw.rect(self.screen, "white", (node.pos[0]*self.tz, node.pos[1]*self.tz, self.tz, self.tz))

        return path[::-1]

    def heuristic(self, node:Node, goal:Node):
        return abs(node.pos[0] - goal.pos[0]) + abs(node.pos[1] - goal.pos[1])

    def update_node(self, node:Node, current:Node, g:float, h:float):
        node.g = g
        node.h = h
        node.f = g + h
        node.parent = current

        return node

    def get_neighbors(self, node:Node):
        
        dirs = [[1, 0], [0, 1], [-1, 0], [0, -1], [1, 1], [-1, 1], [1, -1], [-1, -1]]
        neighbors = []

        for dir in dirs:
            neighbor_pos = (node.pos[0] + dir[0], node.pos[1] + dir[1])

            if (0 <= neighbor_pos[0] < self.map_grid.shape[1] and
                0 <= neighbor_pos[1] < self.map_grid.shape[0]):
                
                if self.map_grid[neighbor_pos[1]][neighbor_pos[0]] != 1:
                    neighbors.append(Node(neighbor_pos))


        return neighbors



if __name__ == "__main__":

    grid_store = []

    with open("maze1.dat", "r") as maze:
        lines = maze.readlines()
    
        for line in lines:
            grid_store.append(list(map(int, line.rstrip().split()[0])))
    grid = np.array(grid_store)

    pygame.init()   


    tilesize = 4

    screen = pygame.display.set_mode((tilesize*grid.shape[1], tilesize*grid.shape[0]))

    

    start = Node((1, 1))
    goal = Node((200, 200))

    starttime = time.time()
    astar = Astar(screen, grid, tilesize)
    astar.bi = True #Comment/Uncomment to remove/add another cursor

    path = astar.search(start, goal)
    endtime = time.time()

    print(endtime - starttime)

    Done = False

    while Done == False:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    Done = True
            if event.type == pygame.QUIT:
                Done = True
        pygame.display.flip()
