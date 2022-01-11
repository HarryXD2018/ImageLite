import cv2
from mtcnn.mtcnn import MTCNN
from ctypes import *


def face_detection(img):
    detector = MTCNN()
    face = detector.detect_faces(img)
    face = face[0]
    # »­¿ò
    box = face["box"]

    cv2.rectangle(img, (box[0], box[1]), (box[0] + box[2], box[1] + box[3]), (255, 0, 0), 2)

    # »­¹Ø¼üµã
    left_eye = face["keypoints"]["left_eye"]
    right_eye = face["keypoints"]["right_eye"]
    nose = face["keypoints"]["nose"]
    mouth_left = face["keypoints"]["mouth_left"]
    mouth_right = face["keypoints"]["mouth_right"]

    points_list = [(left_eye[0], left_eye[1]),
                   (right_eye[0], right_eye[1]),
                   (nose[0], nose[1]),
                   (mouth_left[0], mouth_left[1]),
                   (mouth_right[0], mouth_right[1])]
    for point in points_list:
        cv2.circle(img, point, 1, (255, 0, 0), 4)