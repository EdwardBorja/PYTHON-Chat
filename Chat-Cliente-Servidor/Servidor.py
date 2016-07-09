# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/Users/Christian/Desktop/newChat/untitled.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
from _thread import start_new_thread
import socket
from PyQt5 import QtCore, QtGui, QtWidgets
import time
from PyQt5.QtWidgets import QInputDialog
import pyDes

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
puerto = 8000
llave = "DESCRYPT"
k = pyDes.des(llave, pyDes.CBC,b'\0\0\0\0\0\0\0\0', pad=None, padmode=pyDes.PAD_PKCS5)

'''
serversocket.bind((host, puerto))
serversocket.listen(5)
clientsocket, clientaddress = serversocket.accept()
'''
usuario = "Servidor"
print()

bandera = False;
lista_de_clientes = ["2","1"]
Cliente = ""

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


########################################################################################################################

    def mensaje(self):
        data = self.txtMensaje.text()
        d = k.encrypt(data.encode("UTF-8"))
        self.txtConversacion.append(" Yo > "+data)
        self.txtMensaje.setText("")
        #mensaje sin encriptar
        clientsocket.send(bytes(data,"UTF-8"))
        #print("Mensaje: ",data," Encriptado: ",str(d)," Desencriptado: ",str(k.decrypt(d)))
        #clientsocket.send(bytes(str(d),"UTF-8"))

    def run(self,clientsocket):
        while True:
            try:
                newdata = clientsocket.recv(2048)
                mensaje = newdata.decode("UTF-8")
                self.txtConversacion.append(clientaddress[0] + " : " + str(clientaddress[1])+' dice < '+mensaje)

            except:
                self.txtConversacion.append("No puede recibir respuesta\nIntentanto en 5 seg")
                time.sleep(5)
########################################################################################################################
if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()

    host = socket.gethostbyname(socket.gethostname())

    serversocket.bind((host, puerto))
    serversocket.listen(5)
    clientsocket, clientaddress = serversocket.accept()

    ui.setupUi(MainWindow)
    ui.txtConversacion.setText("Host: "+str(host)+" Puerto: "+str(puerto)+"\n"+usuario)

    ui.txtConversacion.setReadOnly(True)
    ui.btnEnviar.setEnabled(False)
    ui.btnEnviar.clicked.connect(ui.mensaje)
    ui.txtMensaje.textChanged.connect(ui.ValidarTexto)
    #start_new_thread(ui.run,(clientsocket,))

    MainWindow.setFixedSize(402, 260)
    MainWindow.setWindowTitle("Servidor")
    MainWindow.show()
    start_new_thread(ui.run,(clientsocket,))
    # sys.exit(app.exec_())
    app.exec_()
