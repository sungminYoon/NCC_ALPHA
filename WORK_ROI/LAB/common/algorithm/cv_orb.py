"""
Created by SungMin Yoon on 2020-06-17..
Copyright (c) 2020 year SungMin Yoon. All rights reserved.
"""
import cv2


def features_orb(image_01, image_02):
    # ORB 알고리즘의 속성
    orb = cv2.ORB_create(
        nfeatures=10,
        scaleFactor=1.2,
        nlevels=8,
        edgeThreshold=31,
        firstLevel=0,
        WTA_K=2,
        scoreType=cv2.ORB_HARRIS_SCORE,
        patchSize=31,
        fastThreshold=20,
    )
    # ORB 알고리즘의 현재 이미지
    kp1, des1 = orb.detectAndCompute(image_01, None)

    # ORB 알고리즘의 비교 대상 이미지
    kp2, des2 = orb.detectAndCompute(image_02, None)

    # 비교
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)
    matches = sorted(matches, key=lambda x: x.distance)

    k: int = 0

    # 거리 총합의 값이 적을 수록 비슷한 이미지
    distance_sum: float = 0.0

    # 특징이 몇게인지
    distance_count = 0

    for number in matches[:100]:
        obj: cv2.DMatch = number
        distance_sum = distance_sum + obj.distance
        distance_count = distance_count + k
        k = k + 1

    bundle = (distance_sum, distance_count)
    return bundle


