from PyQt5 import QtWidgets, uic
import socket
import threading
import sys

class Client:
    def __init__(self):
        host, port = 127.0.0.0, 55555 
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))


    def run_client(self, name):
        self.nickname = '<b><font color = "red">'+name+'</font></b>'
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

        # write_thread = threading.Thread(target=self.write())
        # write_thread.start()

    def receive(self):
        while True:
            try:
                message = self.client.recv(1024).decode('ascii')
                if message == 'NICK':
                    self.client.send(self.nickname.encode('ascii'))
                else:
                    self.print_receive(message)
            except:
                self.print_receive("An error occured!")
                self.client.close()
                break
    def print_receive(self, message):
        print(message)

    def write(self,ms):
        message = '{}: {}'.format(self.nickname, ms)
        self.client.send(message.encode('ascii'))


class Interface(Client):
    def __init__(self, bg='background.png'):
        super().__init__()

        self.app = QtWidgets.QApplication([])
        path = f'background-image: url({bg})'
        self.app.setStyleSheet("QMainWindow{"+path+"}")

        self.dig = uic.loadUi("desig.ui")

        self.dig.textBrowser.setStyleSheet('font: 75 11pt "Arial";')
        self.dig.textBrowser.setAcceptRichText(True)
        self.dig.textBrowser.setOpenExternalLinks(True)

        self.dig.input_1.setStyleSheet('font: 75 11pt "Arial";')
        self.dig.user_name.setStyleSheet('font: 75 11pt "Arial";')

        self.dig.input_1.setReadOnly(True)
        self.dig.input_1.setPlaceholderText(" > Ingrese Usuario y podra unirce al chat ....") 

        self.dig.user_name.returnPressed.connect(self.log_in)
        self.dig.button_2.clicked.connect(self.log_in)
        self.dig.button_3.clicked.connect(self.sign_out)

        self.dig.show()
        self.app.exec()

    def send(self):
        message = self.dig.input_1.text()
        self.dig.input_1.clear()
        self.write(message)

    def print_receive(self, message):
        self.dig.textBrowser.append(message)
        self.update()

    def log_in(self):
        self.un = self.dig.user_name.text()
        if self.un.strip():
            self.dig.user_name.clear()
            self.run_client(self.un)
            self.dig.input_1.setReadOnly(False)
            self.dig.input_1.setPlaceholderText("")  
            self.dig.button_1.clicked.connect(self.send)
            self.dig.input_1.returnPressed.connect(self.send)

            self.dig.user_name.setPlaceholderText(self.un)  
            self.dig.user_name.setReadOnly(True)
            self.dig.button_2.setDisabled(True)

    def sign_out(self):
        self.dig.input_1.setReadOnly(True)
        self.dig.input_1.setPlaceholderText(" > Ingrese Usuario y podra unirse al chat ....")
        self.app.closeAllWindows()
        self.client.close()
        sys.exit(0)

    def update(self):
        val = self.dig.textBrowser.verticalScrollBar().maximum()
        self.dig.textBrowser.verticalScrollBar().setValue(val)

App = Interface()


