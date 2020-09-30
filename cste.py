from numpy import uint8, zeros
from cv2 import rectangle

##IMAGE
WIDTH = 960
HEIGHT = 720
PATTERN_SIZE = 13

#GLOBAL COLORS
STATUS = {
  0: "GRAY",
  1: "WHITE",
  2: "BLUE",
  3: "GREEN",
  4: "RED",
  5: "BLACK",
  6: "ORANGE",
  7: "PURPLE",
  8: "PINK"
}

COLORS = {
  "WHITE":(255,255,255),
  "GRAY":(75,75,75),
  "BLUE":(0,0,255),
  "GREEN":(0,255,0),
  "RED": (255,0,0),
  "BLACK": (0,0,0),
  "ORANGE":(255,125,0),
  "PURPLE":(200,0,255),
  "PINK":(255,0,200)
}


def build_pattern(s):
  pattern = zeros((PATTERN_SIZE,PATTERN_SIZE,3),dtype=uint8)
  color = COLORS[STATUS[s]]
  rectangle(pattern,(1,1),(PATTERN_SIZE-2,PATTERN_SIZE-2),color,-1)
  return pattern

PATTERNS = {}
for s in STATUS: PATTERNS[s] = build_pattern(s)


##PATHFINDER
SYMBOLS = {
  "EMPTY"   : '.',
  "VISITED" : 'V',
  "PATH"    : 'P',
  "TARGET"  : 'T',
  "START"   : 'S',
  "WALL"    : '#',
  "CURRENT" : 'C',
  "EXPLORE" : 'E',
  "OPEN"    : 'O'
}

SYM_TO_STAT = {
  '.': 0,
  'V': 1,
  'P': 2,
  'T': 3,
  'S': 4,
  '#': 5,
  'C': 6,
  'E': 7,
  'O': 8

}

DIR = [(-1,0),(0,1),(1,0),(0,-1)]