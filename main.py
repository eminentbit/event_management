from PyQt5 import QtWidgets
from sign_in import LoginPage
from register import RegisterPage


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    login_window = LoginPage()
    register_window = RegisterPage()

    # Link windows
    login_window.register_window = register_window
    register_window.login_window = login_window

    login_window.show()
    sys.exit(app.exec_())