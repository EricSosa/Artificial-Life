import cv2
import matplotlib.pyplot as plt
import numpy as np
import random

def life(w,h,times):
    a = np.array([[random.randint(0,1) for i in range(w)] for j in range(h)])

    for t in range(times):
        #if random.random() > 0.99 :
        #    a[random.randint(0,w-1)][random.randint(0,h-1)] = random.randint(0,p)
        b = np.insert(a, 0, a[-1,:], axis=0)
        b = b[:-1,:]
        c = np.insert(a, 0, a[:,-1], axis=1)
        c = c[:,:-1]
        d = np.insert(a, -1, a[0,:], axis=0)
        d = d[1:,:]
        e = np.insert(a, -1, a[:,0], axis=1)
        e = e[:,1:]
        f = np.insert(b, -1, b[:,0], axis=1)
        f = f[:,1:]
        g = np.insert(b, 0, b[:,-1], axis=1)
        g = g[:,:-1]
        y = np.insert(d, -1, d[:,0], axis=1)
        y = y[:,1:]
        z = np.insert(d, 0, d[:,-1], axis=1)
        z = z[:,:-1]
        summ = b+c+d+e+f+g+y+z
        
        n = 0
        for j in summ:
            m = 0
            for x in j:
                if ((x < 2) | (x > 3)):
                    a[n][m] = 0
                elif (x == 3):
                    a[n][m] = 1
                m += 1
            n += 1
        image = a.astype(np.uint8)
        (thresh, image) = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY)
        cv2.imshow('window',image)
        cv2.waitKey(111)
    return 0
width = 800
height = 400
iterations = 10000
cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
life(width,height,iterations)