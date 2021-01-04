import matplotlib.pyplot as plt
import numpy as np
import random
random.seed(11)
def ca2d(p,w,h,times,Neumann,noise):
    a = np.zeros([w,h])
    #initialize first cell
    a[0][0] = 1
    # calculate for each time step
    for t in range(times):
        if Neumann == 0:
            for j in range(h):
                for i in range(w):
                    #if noise = 1 multiply with random between 0 and 1
                    if (noise*random.random()) > 0.99999 :
                        a[j][i] = 0
                    else:
                        a[j][i] = (a[j][i]+a[j][i-1]+a[j-1][i]) % p
        if Neumann == 1:
            for j in range(h):
                for i in range(w):
                    #if noise = 1 multiply with random between 0 and 1
                    if (noise*random.random()) > 0.99999 :
                        a[j][i] = 0
                    elif (i < w-1) & (j < h-1) :
                        a[j][i] = (a[j][i]+a[j][i-1]+a[j-1][i]+a[j][i+1]+a[j+1][i]) % p
                    #for the rightmost & downmost to circle around
                    elif (i == w-1) & (j < h-1) :
                        a[j][i] = (a[j][i]+a[j][i-1]+a[j-1][i]+a[j][0]+a[j+1][i]) % p
                    elif (j == h-1) & (i < w-1) :
                        a[j][i] = (a[j][i]+a[j][i-1]+a[j-1][i]+a[j][i+1]+a[0][i]) % p
                    elif (j == h-1) & (i == w-1) :
                        a[j][i] = (a[j][i]+a[j][i-1]+a[j-1][i]+a[j][0]+a[0][i]) % p
        ax.cla()
        ax.imshow(a, cmap='jet')
        ax.set_title("Iteration {}".format(t))
        plt.pause(0.1)
    return 0
# Settings
p = 5
#I wouldnt go over 500*500
width = 100
height = 100
iterations = 50
#0 = off, 1 = on
neumann = 1
noise = 0

fig, ax = plt.subplots(figsize=(5,5))
ca2d(p,width,height,iterations,neumann,noise)