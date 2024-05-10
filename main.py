import sys
from PyQt5.QtWidgets import QApplication
from smart_home.monitoring_dashboard import SmartHomeGUI
from smart_home.central_automation_system import CentralAutomationSystem

if __name__ == "__main__":
    """Main entry point for the smart home application."""
    automation_system = CentralAutomationSystem()

    app = QApplication(sys.argv)
    smart_home_gui = SmartHomeGUI(automation_system)
    smart_home_gui.show()
    sys.exit(app.exec_())
