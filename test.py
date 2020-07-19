import cv2 as cv
import numpy as np
import random

GET_BIN = lambda x, n: format(x, 'b').zfill(n)

def build_pattern(col):
  pattern = np.ones((PATTERN_SIZE,PATTERN_SIZE,3),dtype=np.uint8)*255

  #color = COLORS
  pattern[:1,:] = COLORS["GRAY"]
  pattern[-1:,:] = COLORS["GRAY"]
  pattern[:,:1] = COLORS["GRAY"]
  pattern[:,-1:] = COLORS["GRAY"]
  if col == 1:
    cv.rectangle(pattern,(1,1),(PATTERN_SIZE-2,PATTERN_SIZE-2),COLORS["BLACK"],-1)
  return pattern



class GOL_1D:
  def __init__(self,w,n_steps,rule_id,rand=False):
    self.w = w
    self.states = []
    self.steps = 0
    self.n_steps = n_steps
    self.rule_id = rule_id
    self.rand_first_state = rand
    self.rules = self.get_rules(rule_id)

    self.patterns = {0:build_pattern(0),1:build_pattern(1)}
  def step(self):
    if not self.states:
      return self.build_initial_state()

    curr = self.states[-1]

    state = curr.copy()
    for i in range(self.w):
      code = ''.join([str(curr[(i-1)%self.w]),str(curr[i]),str(curr[(i+1)%self.w])])
      state[i] = self.rules[code]
    return state
  def build_im(self):
    im = np.zeros(((self.n_steps+1)*PATTERN_SIZE,w*PATTERN_SIZE,3),dtype=np.uint8)

    pattern = self.patterns[0]
    for j in range(self.n_steps+1):
      for i in range(self.w):
        im[j*PATTERN_SIZE:j*PATTERN_SIZE+PATTERN_SIZE,i*PATTERN_SIZE:i*PATTERN_SIZE+PATTERN_SIZE] = pattern

    #im = cv.resize(im,(0,0),fx=.25,fy=.25,interpolation=cv.INTER_AREA)
    return im
  def update_im(self,im,k):
    for i in range(self.w):
      pattern = self.patterns[self.states[k][i]]
      im[k*PATTERN_SIZE:k*PATTERN_SIZE+PATTERN_SIZE,i*PATTERN_SIZE:i*PATTERN_SIZE+PATTERN_SIZE] = pattern
    return im
  def build_initial_state(self):
    if self.rand_first_state:
      initial = [random.choice([0,1]) for _ in range(self.w)]
    else:
      initial = [0]*self.w
      initial[self.w//2] = 1
    return initial

  def run(self,save=False):
    im = self.build_im()
    for k in range(self.n_steps+1):
      self.states.append(self.step())
      im = self.update_im(im,k)
      cv.imshow("im",cv.resize(im,(0,0),fx=.1,fy=.1,interpolation=cv.INTER_AREA))
      cv.waitKey(1)
    if save:
      cv.imwrite(f"./Images/Wolfram_ECA_Rules/rule_{self.rule_id:03d}.png",self.build_im())
    cv.waitKey(0)
    cv.destroyAllWindows()
    """
    while self.steps < self.n_steps:
      #print(''.join([str(s) for s in self.state]))
      self.state = self.step()
      self.steps += 1
    """


  def get_rules(self,rule_id):
    assert rule_id >= 0 and rule_id <= 255, "There is only 256 rules [0-255]"
    rule_to_bin = GET_BIN(rule_id,8)
    rules = { "111":0,\
              "110":0,\
              "101":0,\
              "100":0,\
              "011":0,\
              "010":0,\
              "001":0,\
              "000":0 }
    assert len(rules) == len(rule_to_bin), "binary not of size 8"
    cpt = 0
    for k,v in rules.items():
      rules[k] = int(rule_to_bin[cpt])
      cpt += 1
    return rules



if __name__ == "__main__":

  COLORS = {"WHITE":(255,255,255),\
              "GRAY":(175,175,175),\
              "BLUE":(0,0,255),\
              "GREEN":(0,255,0),\
              "RED": (255,0,0),\
              "BLACK": (0,0,0),\
              "ORANGE":(255,125,0),\
              "PURPLE":(200,0,255),\
              "PINK":(255,0,200)}

  PATTERN_SIZE = 9
  w = 801
  assert w%2 != 0, "W must be odd"

  
  steps = 400
  gol = GOL_1D(w,steps,30,rand=True)
  gol.run()
""""
  for j in range(256):

    gol = GOL_1D(w,steps,j)
    gol.run(save=True)
    """


 


    


