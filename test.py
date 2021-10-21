import cv2
import mediapipe as mp
import numpy as np
from PIL import Image
import imutils

def backgroud_video(idx,video_width,video_height):

  mp_drawing = mp.solutions.drawing_utils
  mp_selfie_segmentation = mp.solutions.selfie_segmentation
  cap = cv2.VideoCapture(0)

  with mp_selfie_segmentation.SelfieSegmentation(model_selection=1) as selfie_segmentation:

    while cap.isOpened():
      ret, image = cap.read()
      image= cv2.resize(image, (video_width,video_height), interpolation = cv2.INTER_CUBIC)
      if not ret:
        print("Empty camera frame.")
        continue

      image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

      image.flags.writeable = False
      results = selfie_segmentation.process(image)

      image.flags.writeable = True
      image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

      condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.5

      img_array = np.fromfile('image/back_big/13_자연.png', np.uint8)
      bg_image = cv2.imdecode(img_array,cv2.IMREAD_COLOR)#np.zeros(image.shape, dtype=np.uint8)
      bg_image=cv2.resize(bg_image, (video_width,video_height), interpolation = cv2.INTER_CUBIC)
      print(bg_image.shape)
      #bg_image[:] = BG_COLOR
      output_image = np.where(condition, image, bg_image)

      cv2.imshow('Selfie Segmentation', output_image)
      if cv2.waitKey(5) & 0xFF == 27:
        break
  cap.release()

video_width=683
video_height=384
backgroud_video(1,video_width,video_height)