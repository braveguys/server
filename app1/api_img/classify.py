import cv2
import time
import numpy as np

SCALE = 8
MARK = False


def classify(imagepath):
    data = cv2.imread(imagepath)
    data = data[:, :, ::-1]  # BGR -> RGB
    data = cv2.resize(data, (data.shape[1] // SCALE, data.shape[0] // SCALE))
    data = data.astype(np.float32)
    # assert data.shape == (180, 320, 3)

    clean_cnt = 0
    dirty_cnt = 0
    dirty_list = []

    max_rgb = np.max(data, 2)
    isBlue = (data[:, :, 2] == max_rgb)
    mean_rgb = np.expand_dims(np.mean(data, 2), 2)
    isGray = np.max(np.abs(data - mean_rgb), 2) < 20

    for x in range(data.shape[0]):
        for y in range(data.shape[1]):
            if isGray[x][y]:
                if MARK:
                    data[x][y] = (0, 177, 64)
                clean_cnt += 1
            else:
                if isBlue[x][y]:
                    if MARK:
                        data[x][y] = (0, 0, 255)
                else:
                    dirty_cnt += 1
                    dirty_list.append(data[x][y])

    ratio = dirty_cnt / clean_cnt * 100.0
    print(time.time(), clean_cnt, dirty_cnt, '%.1f' % ratio)
    return ratio
