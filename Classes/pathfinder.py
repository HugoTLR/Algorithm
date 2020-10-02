#System
from collections import defaultdict
from copy import deepcopy as dc
from heapq import heappush,heappop
from sys import maxsize
#Local
from cste import SYMBOLS, DIR

class Pathfinder:
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
    for d in DIR:
        n_pos = ( (pos[0]+d[0]), (pos[1]+d[1]))
        if n_pos[1] >= 0 and n_pos[1] < self.h and n_pos[0] >= 0 and n_pos[0] < self.w and self.grid[n_pos[1]][n_pos[0]] != SYMBOLS['WALL']:
            neighbours.append(n_pos)
    return neighbours

  def find_start_pos(self):
    for k in self.graph.keys():
      if self.graph[k]["symbol"] == SYMBOLS['START']:
        self.start = k
        break

  def find_target_pos(self):
    for k in self.graph.keys():
        if self.graph[k]["symbol"] == SYMBOLS['TARGET']:
          self.target = k
          break

  def instanciate_graph(self,grid):
    self.graph = {}
    self.graph = defaultdict(lambda: [],self.graph)
    for j,row in enumerate(grid):
      for i,col in enumerate(row):
        if col != '#': # avoid wall
          self.graph[(i,j)] = {"symbol":col,\
                                "neighbours":self.find_valid_neighbours((i,j)),\
                                "dist":defaultdict(lambda:maxsize,{}),\
                                "pred":defaultdict(lambda:None,{})}
    self.find_start_pos()
    self.find_target_pos()

  def build_status_map(self,VISITED,c=None,EXPLORING=[],path=[],open_set=[]):
    base_grid = dc(self.grid)
    for V in VISITED:
      base_grid[V[1]][V[0]] = SYMBOLS['VISITED']
    for E in EXPLORING:
      base_grid[E[1]][E[0]] = SYMBOLS['EXPLORE']
    for O in open_set:
      base_grid[O[1]][O[0]] = SYMBOLS['OPEN']
    if c is not None:
      base_grid[c[1]][c[0]] = SYMBOLS['CURRENT']

    for P in path:
      if P != self.start and P != self.target:
        base_grid[P[1]][P[0]] = SYMBOLS['PATH']


    base_grid[self.start[1]][self.start[0]] = SYMBOLS['START']
    base_grid[self.target[1]][self.target[0]] = SYMBOLS['TARGET']
    return base_grid

  def reconstruct_closest_path(self,t=None):

    g = self.target
    #Debugging purpose
    if t != None:
      g = t

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


  def compute_graph(self):
    #Used to compute dijkstra for every cell to the target
    # for key in self.graph.keys():
    self.dijkstra(self.start)
    
  def dijkstra(self,source):
    status = self.build_status_map([])
    self.steps = [status]
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
          changed = True
      if changed:
        self.steps.append(status)
      changed = False

    path = self.reconstruct_closest_path()
    self.steps.append(self.build_status_map(VISITED,path=path))


class AStar(Pathfinder):
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

  def compute_graph(self):
    path = self.aStar()
    # print(f"FINAL PATH : {path}")



  def dist(self,p1,p2):
    return abs(p2[0]-p1[0])+abs(p2[1]-p1[1])
  def heuristic(self,pos):
    return 2*self.dist(pos,self.target)

  def find_best_node(self,open_set,f_scores):
    best = maxsize
    best_n = None
    for o in open_set:
      if f_scores[o] < best:
        best = f_scores[o]
        best_n = o
    return best_n 
  def reconstruct_path(self,came_from,current):

    total_path = [current]
    while current in came_from.keys():
      current = came_from[current]
      total_path.append(current)

    total_path = total_path[::-1]
    total_path.pop(0)
    return total_path
  def aStar(self):
    status = self.build_status_map([])
    self.steps = [status]
    VISITED = []



    open_set = [self.start]

    came_from = {}
    g_scores = {}
    f_scores = {}
    came_from = defaultdict(lambda:None,came_from)
    g_scores = defaultdict(lambda:maxsize,g_scores)
    f_scores = defaultdict(lambda:maxsize,f_scores)

    g_scores[self.start] = 0
    # f_scores[self.start] = heuristic(graph,start)
    f_scores[self.start] = 0
    path = None
    while open_set:
      current = self.find_best_node(open_set,f_scores)
      status = self.build_status_map(VISITED,c=current,EXPLORING=self.graph[current]["neighbours"],open_set=open_set)
      VISITED.append(current)

      if current == self.target:
        # print(f"Found ! Score of last cell : {g_scores[current]=}  {f_scores[current]=}")
        path = self.reconstruct_path(came_from,current)
        break

      open_set.pop(open_set.index(current))
      neighbours = self.graph[current]["neighbours"]
      changes = False
      for nb in neighbours:
        t_g_score = g_scores[current] + 1
        if t_g_score < g_scores[nb]:
          came_from[nb] = current
          g_scores[nb] = t_g_score
          f_scores[nb] = g_scores[nb] + self.heuristic(nb)
          # board[nb[0]][nb[1]] = '0'
          if nb not in open_set:
            open_set.append(nb)
            changes = True
      if changes:
        self.steps.append(status)
        changes = False


    status = self.build_status_map(VISITED,path=path)
    self.steps.append(status)
    return path
