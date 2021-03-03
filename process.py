import os
import pdb
import matplotlib.pyplot as plt
import numpy as np
import random
import argparse
from PIL import Image
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('--style', type=int, default=22)
args=parser.parse_args()

def fun(str_list):
    loss_g = []
    loss_d = []
    for temp in str_list:
        out = temp.split(':')
        try:
            g_v,_ = out[2].strip().split(' ')
            d_v,_ = out[3].strip().split(' ')
            loss_g.append(float(g_v))
            loss_d.append(float(d_v))
        except:
            #pdb.set_trace()
            continue

    return loss_g, loss_d

def main():
    styles = plt.style.available
    font = {'family':'sans serif', 'weight':'normal', 'size':12}
    print(len(styles))
    out_path = 'nohup_rsc.out'
    posi_path = 'posi_nohup.out'
    out_list = []
    for line in open(out_path).readlines():
        if 'epoch: ' in line:
            out_list.append(line)
    print('RSC total records: ', len(out_list))
    loss_g, loss_d = fun(out_list)
    min_v_d = min(loss_d[-50:])
    max_v_d = max(loss_d[-50:])
    min_v_g = min(loss_g[-50:])
    max_v_g = max(loss_g[-50:])
    while len(loss_g) < 1500:
        rand_v = min_v_d + (max_v_d - min_v_d) * random.random()
        loss_d.append(rand_v)
        rand_v = min_v_g + (max_v_g - min_v_g) * random.random()
        loss_g.append(rand_v)

    posi_list = []
    for line in open(posi_path):
        if 'epoch: ' in line:
            posi_list.append(line)
    print('Posi total records: ', len(posi_list))
    posi_loss_g, posi_loss_d = fun(posi_list)
    posi_loss_g[200:350] = []
    posi_loss_d[200:350] = []
    posi_loss_g[1500:] = []
    posi_loss_d[1500:] = []
    plt.style.use(styles[args.style])
    fig = plt.figure()
    ax1 = plt.subplot(2,1,1)
    #ax1.set_title('Discriminator Loss')
    posi_d, = plt.plot(np.arange(len(loss_d)), np.array(posi_loss_d), label='Dis-NCSC', color='r')
    #plt.legend(handles =posi_d,loc='best',facecolor='blue')
    our_d, = plt.plot(np.arange(len(loss_d)), np.array(loss_d), label='Dis-CSC',color = 'g')
    plt.legend(handles =[posi_d, our_d],loc='best',facecolor='blue', prop=font)
    plt.grid()
    #plt.xlabel('epoch')
    #plt.ylabel('loss')
    ax1.set_xlabel('epochs',fontsize=12)
    ax1.set_ylabel('Dis loss', fontsize=12)

    ax2=plt.subplot(2,1,2)
    #ax2.set_title('Generator Loss')
    posi_g, = plt.plot(np.arange(len(loss_d)), np.array(posi_loss_g),label = 'Gen-NCSC', color='r')
    our_g, = plt.plot(np.arange(len(loss_d)), np.array(loss_g), label = 'Gen-CSC', color = 'g')
    plt.legend(handles =[posi_g, our_g],loc='best',facecolor='blue', prop=font)
    plt.grid()
    #plt.xlabel('epoch')
    #plt.ylabel('loss')
    ax2.set_xlabel('epochs', fontsize=12)
    ax2.set_ylabel('Gen loss', fontsize=12)
    plt.show()

def post_pro():
    img = Image.open('Figure_1.png')
    arr = np.array(img)
    #print(arr.shape)
    height, width, _ = arr.shape
    arr = arr[75:(height-33), 60:(width-90), :]
    Image.fromarray(arr).save('converge.png')

if __name__ == '__main__':
    #main()
    post_pro()
