# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/Users/Christian/Desktop/newChat/untitled.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from _thread import start_new_thread
import socket
from PyQt5 import QtCore, QtGui, QtWidgets
from time import time
from PyQt5.QtWidgets import QInputDialog
import pyDes

host = 'localhost'
puerto = 8000
usuario = "Cliente"

llave = "DESCRYPT"
k = pyDes.des(llave, pyDes.CBC,b'\0\0\0\0\0\0\0\0', pad=None, padmode=pyDes.PAD_PKCS5)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(402, 285)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.txtConversacion = QtWidgets.QTextEdit(self.centralwidget)
        self.txtConversacion.setGeometry(QtCore.QRect(0, 0, 401, 221))
        self.txtConversacion.setObjectName("txtConversacion")
        self.btnEnviar = QtWidgets.QPushButton(self.centralwidget)
        self.btnEnviar.setGeometry(QtCore.QRect(330, 220, 75, 23))
        self.btnEnviar.setObjectName("btnEnviar")
        self.txtMensaje = QtWidgets.QLineEdit(self.centralwidget)
        self.txtMensaje.setGeometry(QtCore.QRect(0, 220, 331, 20))
        self.txtMensaje.setObjectName("txtMensaje")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 402, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Chat Python"))
        self.btnEnviar.setText(_translate("MainWindow", "Enviar"))



    def ValidarTexto(self):
        contenido = self.txtMensaje.text()
        if contenido == "":
            self.btnEnviar.setEnabled(False)
        else:
            self.btnEnviar.setEnabled(True)

    def mensaje(self):
        data = self.txtMensaje.text()
        d = k.encrypt(data.encode("UTF-8"))
        self.txtConversacion.append(" Yo > "+data)
        self.txtMensaje.setText("")
        clientsocket.send(bytes(data,"UTF-8"))
        #print("Mensaje: ",data," Encriptado: ",str(d)," Desencriptado: ",str(k.decrypt(d)))
        #clientsocket.send(bytes(str(d),"UTF-8"))

    def run(self,clientsocket):
        while True:
            try:
                #169.254.118.82
                t = time()
                newdata = clientsocket.recv(2048)
                mensaje = newdata.decode('utf-8')
                self.txtConversacion.append("Servidor < "+mensaje)




            except:
                self.txtConversacion.append("Servidor desconectado")
                time.sleep(5)

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    '''items = ( str(socket.gethostbyname(socket.gethostname())),"" )
    item, ok = QInputDialog.getItem(None, "IP",
         "Selecciona una IP:", items, 0, False)
    if ok and item:
        host = item'''
    newIP,ok = QInputDialog.getText(None, 'IP ', 'Ingresa la ip:\nActual: '+socket.gethostbyname(socket.gethostname()))
    if ok:
        host = newIP
    #host = '169.254.118.82'
    #host = socket.gethostbyname(socket.gethostname())
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect((host,puerto))

    ui.txtConversacion.setText("Host: "+str(host)+" Puerto: "+str(puerto)+"\n"+usuario)
    ui.txtConversacion.setReadOnly(True)
    ui.btnEnviar.setEnabled(False)
    ui.txtMensaje.textChanged.connect(ui.ValidarTexto)
    ui.btnEnviar.clicked.connect(ui.mensaje)


    MainWindow.setWindowTitle("Cliente")
    MainWindow.setFixedSize(402, 260)

    MainWindow.show()
    start_new_thread(ui.run,(clientsocket,))
    # sys.exit(app.exec_())
    app.exec_()