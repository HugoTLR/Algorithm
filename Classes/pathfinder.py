import math
from copy import deepcopy as dc
from collections import defaultdict
from heapq import heappush,heappop
from sys import maxsize
class Pathfinder:
  SYMBOLS = {"START":'S',\
              "TARGET":'T',\
              "WALL":'#',\
              "EMPTY":'.'}


  DIR = [(-1,0),(0,1),(1,0),(0,-1)]
  def __init__(self):
    pass

  def __str__(self):
    res = f"{self.start=}\t{self.target=}\n"
    for row in self.grid:
      res = res + ''.join(row) + '\n'
    return res
  def build_status(self):
    raise NotImplementedError("Must override build_status")
  def solve(self):
    raise NotImplementedError("Must override solve")
  def compute_graph(self):
    raise NotImplementedError("Must override compute_graph")

  def find_valid_neighbours(self,pos):
    neighbours = []
    for d in Pathfinder.DIR:
        n_pos = ( (pos[0]+d[0]), (pos[1]+d[1]))
        print(f"{self.h=} {self.w=} {n_pos=}")
        if n_pos[1] >= 0 and n_pos[1] < self.h and n_pos[0] >= 0 and n_pos[0] < self.w and self.grid[n_pos[1]][n_pos[0]] != '#':
            neighbours.append(n_pos)
    return neighbours

  def find_start_pos(self):
    for k in self.graph.keys():
      if self.graph[k]["symbol"] == Pathfinder.SYMBOLS['START']:
        self.start = k
        break

  def find_target_pos(self):
    for k in self.graph.keys():
        if self.graph[k]["symbol"] == Pathfinder.SYMBOLS['TARGET']:
          self.target = k
          break

  def instanciate_graph(self,grid):
    self.graph = {}
    self.graph = defaultdict(lambda: [],self.graph)
    for j,row in enumerate(grid):
      for i,col in enumerate(row):
        if col != '#': # remove wall
          self.graph[(i,j)] = {"symbol":col,\
                                "neighbours":self.find_valid_neighbours((i,j)),\
                                "dist":defaultdict(lambda:maxsize,{}),\
                                "pred":defaultdict(lambda:None,{})}
    self.find_start_pos()
    self.find_target_pos()
    #print(self)

  def reconstruct_closest_path(self,t=None):

    g = self.target
    if t != None:
      g = t
    #print(self.graph[self.start])

    path = [g]
    while not g.__eq__(self.start):
      g = self.graph[self.start]["pred"][g]

      path.append(g)
    return path[::-1]



class Dijkstra(Pathfinder):
  def __init__(self):
    pass
  def __str__(self): 
    return super().__str__()

  def solve(self,grid):
    self.grid = grid
    self.w = len(grid[0])
    self.h = len(grid)


    self.instanciate_graph(grid)
    self.compute_graph()

    # for k,v in self.graph.items():
    
      # print(f"{k}\t{v['neighbours']}\t{v['dist']}")

    # path = self.reconstruct_closest_path()
    # print(f"{path=}")

  def build_status_map(self,VISITED,c=None,EXPLORING=[],path=[]):
    base_grid = dc(self.grid)
    for V in VISITED:
      base_grid[V[1]][V[0]] = 'V'
    for E in EXPLORING:
      base_grid[E[1]][E[0]] = 'E'
    if c is not None:
      base_grid[c[1]][c[0]] = 'C'
    for P in path:
      if P != self.start and P != self.target:
        base_grid[P[1]][P[0]] = 'P'

    base_grid[self.start[1]][self.start[0]] = 'S'
    base_grid[self.target[1]][self.target[0]] = 'T'
    return base_grid



  def compute_graph(self):
    # for key in self.graph.keys():
    self.dijkstra(self.start)
    
  def dijkstra(self,source):
    status = self.build_status_map([])
    self.init_step = status
    self.steps = []
    VISITED = []
    Q = []
    self.graph[source]["dist"][source] = 0
    for k in self.graph.keys(): heappush(Q,(self.graph[source]["dist"][k],k))

    changed = False
    while Q:
      (d,u) = heappop(Q)



      nbs = self.graph[u]["neighbours"]


      status = self.build_status_map(VISITED,c=u,EXPLORING=nbs)
      
      VISITED.append(u)
      for nb in nbs:
        alt = self.graph[source]["dist"][u] + 1
        if alt < self.graph[source]["dist"][nb]:
          self.graph[source]["dist"][nb] = alt
          self.graph[source]["pred"][nb] = u
          heappush(Q,(alt,nb))
          VISITED.append(nb)
          changed = True
      if changed:
        self.steps.append(status)
      changed = False

    path = self.reconstruct_closest_path()
    self.final_step = self.build_status_map(VISITED,path=path)
    


