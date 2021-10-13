import cv2
import mediapipe as mp
import numpy as np
from PIL import Image


mp_drawing = mp.solutions.drawing_utils
mp_selfie_segmentation = mp.solutions.selfie_segmentation
type = 'video'
image_path = 'person.png'
video_path = 'C:/Users/mjw27/Desktop/Anyractive/hand.avi'

if type == 'image':
  image = cv2.imread(image_path)
  height, width, _ = image.shape

  BG_COLOR = (0, 0, 0) # black
  MASK_COLOR = (255, 255, 255) # white

  with mp_selfie_segmentation.SelfieSegmentation(model_selection=0) as model:
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = model.process(img)
    condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.5

    fg_image = np.zeros(img.shape, dtype=np.uint8)
    fg_image[:] = MASK_COLOR
    bg_image = np.zeros(img.shape, dtype=np.uint8)
    bg_image[:] = BG_COLOR
    mask = np.where(condition, fg_image, bg_image)

  result = np.where(condition, image, bg_image)

  cv2.imshow('seg', result)
  cv2.imshow('img', image)

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

  image_bg.save('output.png')

  cv2.waitKey()
  cv2.destroyAllWindows()

# video
else:
  BG_COLOR = (192, 192, 192) # gray
  # cap = cv2.VideoCapture(2, cv2.CAP_DSHOW)
  cap = cv2.VideoCapture(video_path)

  with mp_selfie_segmentation.SelfieSegmentation(model_selection=1) as selfie_segmentation:
    bg_image = None
    while cap.isOpened():
      ret, image = cap.read()

      if not ret:
        print("Empty camera frame.")
        continue

      image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

      image.flags.writeable = False
      results = selfie_segmentation.process(image)

      image.flags.writeable = True
      image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

      condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.5

      if bg_image is None:
        bg_image = np.zeros(image.shape, dtype=np.uint8)
        bg_image[:] = BG_COLOR
      output_image = np.where(condition, image, bg_image)

      cv2.imshow('Selfie Segmentation', output_image)
      if cv2.waitKey(5) & 0xFF == 27:
        break
  cap.release()
