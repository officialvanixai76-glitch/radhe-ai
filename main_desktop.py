import sys
from PyQt6.QtWidgets import QApplication, QDialog
from backend.database import init_database
from backend.settings import load_settings
from ui.splash_screen import SplashScreen
from ui.dialogs.login_dialog import LoginDialog
from ui.dashboard import DashboardWindow


def main():
    # Initialize SQLite database schema
    init_database()

    # Load local configurations
    load_settings()

    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    # Initialize and show splash screen
    splash = SplashScreen()
    splash.show()

    def handle_splash_finished():
        # Close splash screen
        splash.close()

        # Launch Login Dialog modal
        login_dlg = LoginDialog()
        if login_dlg.exec() == QDialog.DialogCode.Accepted:
            # Login successful: create and display Main Navigation Dashboard
            app.setQuitOnLastWindowClosed(True)
            dashboard = DashboardWindow()
            dashboard.show()
            
            # Prevent Python garbage collection of main window
            app.main_window = dashboard
        else:
            # User canceled or login failed: terminate app
            sys.exit(0)

    # Transition to login after splash completes loading
    splash.finished.connect(handle_splash_finished)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
