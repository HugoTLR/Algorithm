#3rd Party
from cv2 import  resize,INTER_CUBIC
from PyQt5.QtGui import QImage
#System
#Local
from cste import IMAGE_SCALE

def display_image(image):
  h,w = image.shape[:2]
  disp_size = w//IMAGE_SCALE, h//IMAGE_SCALE
  disp_bpl = disp_size[0] * 3
  if IMAGE_SCALE > 1:
      image = resize(image, disp_size, 
                       interpolation=INTER_CUBIC)
  qim = QImage(image.data, disp_size[0], disp_size[1],disp_bpl,QImage.Format_RGB888)
  return qim