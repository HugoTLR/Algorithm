import cv2 as cv
import numpy as np
import random
GET_BIN = lambda x, n: format(x, 'b').zfill(n)

def build_pattern(col):
  pattern = np.ones((PATTERN_SIZE,PATTERN_SIZE,3),dtype=np.uint8)*255


class GOL_1D:
  def __init__(self,w,n_steps,rule_id,rand=False):
    self.w = w
    self.steps = 0
    self.n_steps = n_steps
    self.states = np.array([[0]*self.w]*(self.n_steps+1))
    self.rule_id = rule_id
    self.rand_first_state = rand
    self.rules = self.get_rules(rule_id)


  def step(self,k):
    if k == 0:
      self.build_initial_state()
    else:
      curr = self.states[k-1]
      for i in range(self.w):
        code = ''.join([str(curr[(i-1)%self.w]),str(curr[i]),str(curr[(i+1)%self.w])])
        self.states[k][i] = self.rules[code]

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
      self.states[0] = [random.choice([0,1]) for _ in range(self.w)]
    else:
      self.states[0][self.w//2] = 1

  def run(self,save=False):
    # im = self.build_im()

    for k in range(len(self.states)):
      self.step(k)

      im = np.array(self.states,dtype=np.uint8)*255

      cv.imshow("im",cv.resize(im,(0,0),fx=1,fy=1,interpolation=cv.INTER_AREA))
      cv.waitKey(1)
    if save:
      cv.imwrite(f"./Images/Wolfram_ECA_Rules/rule_{self.rule_id:03d}.png",cv.resize(im,(0,0),fx=2,fy=2,interpolation=cv.INTER_AREA))
    cv.waitKey(0)
    cv.destroyAllWindows()



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
  w = 1801
  steps = 900
  # w = 401
  # steps = 200
  assert w%2 != 0, "W must be odd"

  
  gol = GOL_1D(w,steps,90,rand=False)
  gol.run(save=False)
  
  # for j in range(256):

  #   gol = GOL_1D(w,steps,j)
  #   gol.run(save=False)
  
    


 


    


