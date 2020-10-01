#3rd Party
import cv2  as cv
from numpy import array,uint8
#System
from random import choice
#Local
from .utils import GET_BIN

class ECA:
  def __init__(self,w,n_steps,rule_id,rand):
    assert w%2 != 0, "W must be odd"
    assert rule_id >= 0 and rule_id <= 255, "There is only 256 rules [0-255]"
    self.w = w
    self.steps = 0
    self.n_steps = n_steps+1
    self.states = array([[0]*self.w]*(self.n_steps))
    self.rule_id = rule_id
    self.rand_first_state = rand
    self.rules = self.get_rules(rule_id)

  def get_rules(self,rule_id):
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

  def build_initial_state(self):
    if self.rand_first_state:
      self.states[0] = [choice([0,1]) for _ in range(self.w)]
    else:
      self.states[0][self.w//2] = 1

  def step(self,k):
    if k == 0:
      self.build_initial_state()
    else:
      curr = self.states[k-1]
      for i in range(self.w):
        code = ''.join([str(curr[(i-1)%self.w]),str(curr[i]),str(curr[(i+1)%self.w])])
        self.states[k][i] = self.rules[code]