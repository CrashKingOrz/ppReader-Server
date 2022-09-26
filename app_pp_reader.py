import time
import cv2
import numpy as np

from kernel.process.mode_processor import ModeProcessor

process = ModeProcessor(device="GPU")


# button2content: {0: 'character', 1: 'word', 2: 'sentence', 3: 'object', 4: 'general'}


def test(button, image, finger_coord1=np.array([-1, -1]), finger_coord2=np.array([-1, -1])):
    text_results = process.mode_execute(button, image, finger_coord1, finger_coord2)
    print(text_results)


if __name__ == '__main__':
    img = cv2.imread("./sample/ocr.png")
    button = 2
    pt1 = (10, 10)
    pt2 = (5090, 4000)

    finger_coord1 = np.array(pt1)
    finger_coord2 = np.array(pt2)

    if button in [0, 1, 2]:
        point_size = 1
        point_color = (0, 0, 255)  # BGR
        thickness = 10
        img = cv2.circle(img, pt2, 10, point_color, thickness)
        test(button, img, finger_coord2)
    else:
        img = cv2.rectangle(img, pt1, pt2, (255, 0, 0), 5)
        test(button, img, finger_coord1, finger_coord2)

    cv2.namedWindow("img", cv2.WINDOW_FREERATIO)
    cv2.imshow("img", img)
    cv2.waitKey(0)
