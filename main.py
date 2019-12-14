# -*- coding: utf-8 -*-
import sys
import os
try:
    from skimage import io
except:
    os.system('pip install scikit-image')
    from skimage import io
#import pyautogui
try:
    from PyQt5 import QtWidgets
except:
    os.system('pip install python-qt5')
    from PyQt5 import QtWidgets
try:
    import requests
except:
    os.system('pip install requests')
    import requests

import PyQt5 as Qt
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QSpinBox, QDoubleSpinBox, QHBoxLayout
from PyQt5.QtCore import  pyqtSlot, QCoreApplication
from PyQt5 import QtCore
import pdb
import json

result_path = './caption_result/'
os.makedirs(result_path, exist_ok=True)

class GridLayout(QtWidgets.QMainWindow):
#class GridLayout(QtWidgets.QWidget):
    def __init__(self):
        super(GridLayout, self).__init__()
        self.path = 'http://holer.cc:50347/data/'
        self.datalist = json.load(open('meta_data.json','r'))
        self.data_len = len(self.datalist)-1
        #pdb.set_trace()
        self.setWindowTitle("Thanks for your efforts")

        main_ground = QtWidgets.QWidget()
        self.setCentralWidget(main_ground)

        #the top part
        top_layout = QHBoxLayout()

        top_layout.addWidget(QtWidgets.QLabel(' '*50))
        top_layout.addWidget(QtWidgets.QLabel('Image ID:'))
        self.spinbox = QSpinBox(self)
        self.spinbox.setRange(0, self.data_len)                                                      # 1
        self.spinbox.setSingleStep(1)                                                       # 2
        self.spinbox.setValue(100)
        self.spinbox.valueChanged.connect(self.value_change_func)
        top_layout.addWidget(self.spinbox)
        top_layout.addWidget(QtWidgets.QLabel(' '*50))

        #======================================
        index = self.spinbox.value()
        im_name, im_data = self.datalist[index]
        r_s, r_t = im_data[0]
        l_s, l_t = im_data[1]

        #layout1, self.lft_cap, self.lft_c_label, self.lft_a_label, self.lft_im_label = self.get_gridlayout(index, l_s, l_t, 'left', 'a mountain stands on the horizon, and a beautiful beach is close to it.')
        #layout2, self.rht_cap, self.rht_c_label, self.rht_a_label, self.rht_im_label = self.get_gridlayout(index, r_s, r_t, 'right', 'there are some clouds is the blue sky, and the lake under the sky is very limpid.')
        layout1, self.lft_cap, self.lft_c_label, self.lft_a_label, self.lft_im_label = self.get_gridlayout(index, l_s, l_t, 'left', '\nbeach\nmountain\nsky\nclouds')
        layout2, self.rht_cap, self.rht_c_label, self.rht_a_label, self.rht_im_label = self.get_gridlayout(index, r_s, r_t, 'right', '\nlimpid lake\nmountain')

        h_box = QtWidgets.QVBoxLayout()

        h_box.addLayout(top_layout)
        h_box.addLayout(layout1)
        h_box.addLayout(layout2)

        v_box = QtWidgets.QVBoxLayout()

        h_box2 = QtWidgets.QHBoxLayout()
        self.next_button = QtWidgets.QPushButton('Next Sample', self)
        self.next_button.clicked.connect(self.next_click)
        
        self.prev_button = QtWidgets.QPushButton('Prev Sample', self)
        self.prev_button.clicked.connect(self.prev_click)
        h_box2.addWidget(self.prev_button)
        h_box2.addWidget(self.next_button)

        v_box.addLayout(h_box)
        v_box.addLayout(h_box2)
        
        #main_ground.setLayout(v_layout)
        main_ground.setLayout(v_box)
        self.resize(480, 400)
    
#    def init_img_data(self):
        #img_dict = json.load(open('all_img_clss_attrs.json','r'))
        #self.datalist = [item for item in img_dict.items()]
        #json.dump(self.datalist, open('all_img_clss_attrs_ls.json', 'w'))
        #self.datalist = json.load(open('all_img_clss_attrs_ls.json','r'))

    def get_gridlayout(self, index, s, t, flag, example_cap):

        grid = QtWidgets.QGridLayout()
        #grid.addWidget(label, 2, 1, 5,1)
        grid.addWidget(QtWidgets.QLabel("Category:"), 1, 0)
        #c_label = QtWidgets.QLabel(', '.join(s))
        c_label = QtWidgets.QHBoxLayout()
        c_items = s
        for i in range(5):
            temp = QtWidgets.QCheckBox(c_items[i])
            setattr(self,flag+'_c_it' +str(i), temp)
            c_label.addWidget(getattr(self, flag+'_c_it'+str(i)))

        grid.addLayout(c_label, 1, 1)
        
        grid.addWidget(QtWidgets.QLabel("Attribution:"), 2, 0)        
        a_label = QtWidgets.QHBoxLayout()
        for j in range(9):
            temp = QtWidgets.QCheckBox(t[j])
            setattr(self, flag+'_a_it'+str(j), temp)
            a_label.addWidget(getattr(self,flag+"_a_it"+str(j)))
 
        grid.addLayout(a_label, 2, 1)

        grid.addWidget(QtWidgets.QLabel("Your Caption:"), 3, 0)
        cap = QtWidgets.QTextEdit()
        cap.setPlaceholderText('For example: {}'.format(example_cap))
        grid.addWidget(cap, 3, 1, 5, 1)

        #path = 'http://172.19.123.28:9000/data/test_0.jpg'
        '''path = self.path + str(index) + '_%s.jpg'%flag 
        img_data = requests.get(path)
        Png=QtGui.QPixmap()
        Png.loadFromData(img_data.content)'''
        path = self.path + str(index) + '.jpg'
        #if not os.path.exists('./left.jpg'):
            #urllib.urlretrieve(img, './temp.jpg')
        img = io.imread(path)
        left = img[:,:128, :]
        right = img[:,128:, :]
        left = left[:,::-1, :]
        io.imsave('left.jpg', left)
        io.imsave('right.jpg', right)
        
        #img_data = requests.get(path)
        Png=QtGui.QPixmap('./{}.jpg'.format(flag))
        Png = Png.scaled(196, 196)#, Qt.KeepAspectRatio, Qt.FastTransformation)
        im_label = QtWidgets.QLabel()
        im_label.setPixmap(Png)
        
        H_box = QtWidgets.QHBoxLayout()
        H_box.addWidget(im_label) 
        H_box.addLayout(grid)
        '''if flag == 'left':
            for k in range(5):
                attr = getattr(self, 'left_c_it'+str(k))
                attr.stateChanged.connect(lambda: self.checkBox_change_left(attr))'''
            #self.left_c_it0.stateChanged.connect(lambda: self.checkBox_change_left(self.left_c_it0))
        if flag == 'left':
            self.connect_to(self.left_c_it0)
            self.connect_to(self.left_c_it1)
            self.connect_to(self.left_c_it2)
            self.connect_to(self.left_c_it3)
            self.connect_to(self.left_c_it4)
            self.connect_to(self.left_a_it0)
            self.connect_to(self.left_a_it1)
            self.connect_to(self.left_a_it2)
            self.connect_to(self.left_a_it3)
            self.connect_to(self.left_a_it4)
            self.connect_to(self.left_a_it5)
            self.connect_to(self.left_a_it6)
            self.connect_to(self.left_a_it7)
            self.connect_to(self.left_a_it8)
        else:
            self.connect_to(self.right_c_it0, False)
            self.connect_to(self.right_c_it1, False)
            self.connect_to(self.right_c_it2, False)
            self.connect_to(self.right_c_it3, False)
            self.connect_to(self.right_c_it4, False)
            self.connect_to(self.right_a_it0, False)
            self.connect_to(self.right_a_it1, False)
            self.connect_to(self.right_a_it2, False)
            self.connect_to(self.right_a_it3, False)
            self.connect_to(self.right_a_it4, False)
            self.connect_to(self.right_a_it5, False)
            self.connect_to(self.right_a_it6, False)
            self.connect_to(self.right_a_it7, False)
            self.connect_to(self.right_a_it8, False)

        return H_box, cap, c_label, a_label, im_label 

    def connect_to(self, box, left=True):
        if left:
            box.stateChanged.connect(lambda: self.checkBox_change(box))
        else:
            box.stateChanged.connect(lambda: self.checkBox_change(box, left))

    def checkBox_change(self,ck_box, left=True):
        if not ck_box.isChecked():
            return
        if left:
            cap_text =  self.lft_cap.toPlainText()
            box_text = ck_box.text()
            #ck_box.setChecked(True)
            cap_text = cap_text + box_text + '\n'
            self.lft_cap.setPlainText(cap_text)
        else:
            cap_text =  self.rht_cap.toPlainText()
            box_text = ck_box.text()
            #ck_box.setChecked(True)
            cap_text = cap_text + box_text + '\n'
            self.rht_cap.setPlainText(cap_text)

    @pyqtSlot()
    def value_change_func(self):
        index = self.spinbox.value()
        im_name, im_data = self.datalist[index]#[min(index, self.data_len)]
        r_s, r_t = im_data[0]
        l_s, l_t = im_data[1]
        path = self.path + str(index) + '.jpg'
        #if not os.path.exists('./left.jpg'):
            #urllib.urlretrieve(img, './temp.jpg')
        img = io.imread(path)
        left = img[:,:128, :]
        right = img[:,128:, :]
        left = left[:,::-1, :]
        io.imsave('left.jpg', left)
        io.imsave('right.jpg', right)
        
        Png=QtGui.QPixmap('./left.jpg')
        Png = Png.scaled(196, 196)#, Qt.KeepAspectRatio, Qt.FastTransformation)
        #im_label = QtWidgets.QLabel()
        self.lft_im_label.setPixmap(Png)
 
        Png=QtGui.QPixmap('./right.jpg')
        Png = Png.scaled(196, 196)#, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.rht_im_label.setPixmap(Png)
        
        for i in range(5):
            temp = getattr(self, 'left_c_it'+str(i))
            temp.setText(l_s[i])
            temp.setChecked(False)
            temp1 = getattr(self, 'right_c_it'+str(i))
            temp1.setText(r_s[i])
            temp1.setChecked(False)
        
        for i in range(9):
            temp = getattr(self, 'left_a_it'+str(i))
            temp.setText(l_t[i])
            temp.setChecked(False)
            temp1 = getattr(self, 'right_a_it'+str(i))
            temp1.setText(r_t[i])
            temp1.setChecked(False)

        #for i in range(5):
        #    temp = getattr(self, 'left_c_it'+str(i))
        #    temp.setChecked(False)
        #self.left_c_it0.setChecked(False)
 
        self.lft_im_label.repaint()
        self.rht_im_label.repaint()

        #self.left_c_it1.setChecked(False)

        QtWidgets.qApp.processEvents()
        QCoreApplication.processEvents()
        #print(index,'done')

    @pyqtSlot()
    def next_click(self):
        index = self.spinbox.value()
        #print(index)
        fench_index = min(index+1, self.data_len)

        lft_cap = self.lft_cap.toPlainText()
        rht_cap = self.rht_cap.toPlainText()
        with open(result_path + str(index) + '_left.txt', 'w+') as f:
            f.write(lft_cap + '\n')
        with open(result_path + str(index) + '_right.txt', 'w+') as f:
            f.write(rht_cap + '\n')
        #print(lft_cap, rht_cap)

        
        self.spinbox.setValue(fench_index)
        rht_cap = ''
        lft_cap = ''
        if os.path.exists(result_path + str(fench_index) +'_left.txt'):
            lines = open(result_path + str(fench_index) + '_left.txt').readlines()
            lines =list(filter(lambda x:x.strip()!='', lines))
            if len(lines) > 0:
                lft_cap = ''.join(lines)#[-1]

        if os.path.exists(result_path + str(fench_index) +'_right.txt'):
            lines = open(result_path + str(fench_index) + '_right.txt').readlines()
            lines =list(filter(lambda x:x.strip()!='', lines))
            if len(lines) > 0:
                rht_cap = ''.join(lines)#[-1]

        if len(rht_cap.strip())!= '':
            self.rht_cap.setPlainText(rht_cap)
        if len(lft_cap.strip())!= '':
            self.lft_cap.setPlainText(lft_cap)


    @pyqtSlot()
    def prev_click(self):
        index = self.spinbox.value()
        #print(index)
        fench_index = max(0, index-1)

        rht_cap = ''
        lft_cap = ''
        if os.path.exists(result_path + str(fench_index) +'_left.txt'):
            lines = open(result_path + str(fench_index) + '_left.txt').readlines()
            lines =list(filter(lambda x:x.strip()!='', lines))
            if len(lines) > 0:
                lft_cap = ''.join(lines)

        if os.path.exists(result_path + str(fench_index) +'_right.txt'):
            lines = open(result_path + str(fench_index) + '_right.txt').readlines()
            lines =list(filter(lambda x:x.strip()!='', lines))
            if len(lines) > 0:
                rht_cap = ''.join(lines)#[-1]

        if len(rht_cap.strip())!= '':
            self.rht_cap.setPlainText(rht_cap)
        if len(lft_cap.strip())!= '':
            self.lft_cap.setPlainText(lft_cap)
                
        self.spinbox.setValue(fench_index)

app = QtWidgets.QApplication(sys.argv)
grid_layout = GridLayout()
grid_layout.show()
sys.exit(app.exec_())
