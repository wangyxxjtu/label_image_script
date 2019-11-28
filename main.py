# -*- coding: utf-8 -*-
import sys
import os
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
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QSpinBox, QDoubleSpinBox, QHBoxLayout
from PyQt5.QtCore import  pyqtSlot, QCoreApplication
from PyQt5 import QtCore
import pdb
try:
    import json
except:
    os.system('pip install json')
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
        c_label = QtWidgets.QLabel(', '.join(s))
        grid.addWidget(c_label, 1, 1)
        
        grid.addWidget(QtWidgets.QLabel("Attribution:"), 2, 0)        
        a_label = QtWidgets.QLabel(', '.join(t))
        grid.addWidget(a_label, 2, 1)

        grid.addWidget(QtWidgets.QLabel("Your Caption:"), 3, 0)
        cap = QtWidgets.QTextEdit()
        cap.setPlaceholderText('For example: {}'.format(example_cap))
        grid.addWidget(cap, 3, 1, 5, 1)

        #path = 'http://172.19.123.28:9000/data/test_0.jpg'
        path = self.path + str(index) + '_%s.jpg'%flag 
        img_data = requests.get(path)
        Png=QtGui.QPixmap()
        Png.loadFromData(img_data.content)
        im_label = QtWidgets.QLabel()
        im_label.setPixmap(Png)
        
        H_box = QtWidgets.QHBoxLayout()
        H_box.addWidget(im_label) 
        H_box.addLayout(grid)

        return H_box, cap, c_label, a_label, im_label 

    @pyqtSlot()
    def value_change_func(self):
        index = self.spinbox.value()
        im_name, im_data = self.datalist[index]#[min(index, self.data_len)]
        r_s, r_t = im_data[0]
        l_s, l_t = im_data[1]
        path = self.path + str(index) + '_left.jpg' 
        img_data = requests.get(path)
        Png=QtGui.QPixmap()
        Png.loadFromData(img_data.content)
        #im_label = QtWidgets.QLabel()
        self.lft_im_label.setPixmap(Png)

        path = self.path + str(index) + '_right.jpg' 
        img_data = requests.get(path)
        Png=QtGui.QPixmap()
        Png.loadFromData(img_data.content)
 
        self.rht_im_label.setPixmap(Png)
        
        self.lft_c_label.setText(', '.join(l_s))
        self.lft_a_label.setText(', '.join(l_t))
        self.rht_c_label.setText(', '.join(r_s))
        self.rht_a_label.setText(', '.join(r_t))

        self.lft_im_label.repaint()
        self.rht_im_label.repaint()
        self.lft_c_label.setText(', '.join(l_s))
        self.lft_a_label.setText(', '.join(l_t))
        self.rht_c_label.setText(', '.join(r_s))
        self.rht_a_label.setText(', '.join(r_t))

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

        #self.lft_cap.setPlainText("")
        #self.rht_cap.setPlainText("")
        
        #print('done')

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
                
        #self.rht_cap.setPlainText(rht_cap)
        #self.lft_cap.setPlainText(lft_cap)
        self.spinbox.setValue(fench_index)

app = QtWidgets.QApplication(sys.argv)
grid_layout = GridLayout()
grid_layout.show()
sys.exit(app.exec_())
