import cv2
import mediapipe as mp
import numpy as np
from PIL import Image
import matplotlib.pylab as plt



mp_drawing = mp.solutions.drawing_utils
mp_selfie_segmentation = mp.solutions.selfie_segmentation
type = 'video'
image_path = 'person.png'
video_path = 'example.mp4'


cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
# cap = cv2.VideoCapture(video_path)
fps = cap.get(cv2.CAP_PROP_FPS)
fourcc = cv2.VideoWriter_fourcc(*'DIVX')
out = cv2.VideoWriter('output.avi', fourcc, 30, (640, 480))

BG_COLOR = (0, 0, 0) # black
MASK_COLOR = (255, 255, 255) # white

with mp_selfie_segmentation.SelfieSegmentation(model_selection=1) as selfie_segmentation:
    bg_image = None
    while cap.isOpened():
      ret, image = cap.read()

      if not ret:
        print("Empty camera frame.")
        break

      image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

      image.flags.writeable = False
      results = selfie_segmentation.process(image)

      image.flags.writeable = True
      image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

      condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.5

      if bg_image is None:
        bg_image = np.zeros(image.shape, dtype=np.uint8)
        bg_image[:] = BG_COLOR
        fg_image = np.zeros(image.shape, dtype=np.uint8)
        fg_image[:] = MASK_COLOR
      output_image = np.where(condition, image, bg_image)
      mask = np.where(condition, fg_image, bg_image)

      cv2.imshow('Segmentation', output_image)
      cv2.imshow('mask', mask)

      # 투명배경
      mask = cv2.bitwise_not(mask)
      image_bg = cv2.add(image, mask)
      image_bg = Image.fromarray(cv2.cvtColor(image_bg, cv2.COLOR_BGR2RGB))
      image_bg = image_bg.convert('RGBA')
      L, H = image_bg.size
      color_0 = (255, 255, 255, 255)
      for h in range(H):
        for l in range(L):
          dot = (l, h)
          color_1 = image_bg.getpixel(dot)
          if color_1 == color_0:
            color_1 = color_1[:-1] + (0,)
            image_bg.putpixel(dot, color_1)
      numpy_image = np.array(image_bg)
      cv_image = cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR)

      # image_bg.save('output.avi')

      cv2.imshow('image_bg', cv_image)

      out.write(cv_image)

      if cv2.waitKey(1) & 0xFF == 27:
        break

    out.release()
    cap.release()
    cv2.destroyAllWindows()