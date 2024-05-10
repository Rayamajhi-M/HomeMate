from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QLabel, QSlider, QTextEdit, QVBoxLayout, \
    QLineEdit, QComboBox, QMessageBox
from PyQt5.QtCore import QTimer

# Importing additional modules for enhanced styling
from PyQt5.QtGui import QFont

# Importing smart home device classes
from smart_home.smart_light import SmartLight
from smart_home.thermostat import Thermostat
from smart_home.security_camera import SecurityCamera


class SmartHomeGUI(QMainWindow):
    """Class representing the Smart Home Monitoring Dashboard."""
    def __init__(self, automation_system):
        """Initialize a SmartHomeGUI instance.

                Args:
                    automation_system: The central automation system for the smart home.
                """
        super().__init__()
        self.automation_system = automation_system
        self.smart_light = None
        self.thermostat = None
        self.security_camera = None

        self.setWindowTitle("Smart Home Dashboard")

        self.setWindowIcon(QIcon('icon.png'))

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.create_widgets()
        self.update_device_status()

        self.toggle_timer = QTimer()
        self.toggle_timer.timeout.connect(self.update_brightness_slider)

        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor("#F0F0F0"))  # Background color
        self.setPalette(p)

        self.setStyleSheet(
            """
            QPushButton {
                background-color: #4CAF50; /* Green */
                border: none;
                color: white;
                padding: 10px 24px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                transition-duration: 0.4s;
                cursor: pointer;
                border-radius: 8px;
            }

            QPushButton:hover {
                background-color: #45a049; /* Darker Green */
                color: white;
            }

            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #333333; /* Dark Gray */
            }

            QSlider {
                height: 20px;
            }

            QTextEdit {
                font-size: 16px;
                border: 1px solid #CCCCCC; /* Light Gray */
                padding: 10px;
                background-color: #FFFFFF; /* White */
                color: #333333; /* Dark Gray */
            }

            QLineEdit {
                border: 1px solid #CCCCCC; /* Light Gray */
                padding: 8px;
                background-color: #FFFFFF; /* White */
                color: #333333; /* Dark Gray */
            }

            QComboBox {
                border: 1px solid #CCCCCC; /* Light Gray */
                padding: 8px;
                background-color: #FFFFFF; /* White */
                color: #333333; /* Dark Gray */
            }
            """
        )

    def create_widgets(self):
        """Create the widgets for the Smart Home Monitoring Dashboard."""
        layout = QVBoxLayout()

        self.add_device_label = QLabel("Add New Device:")
        layout.addWidget(self.add_device_label)

        self.device_type_label = QLabel("Device Type:")
        layout.addWidget(self.device_type_label)

        self.device_type_dropdown = QComboBox()
        self.device_type_dropdown.addItems(["Smart Light", "Thermostat", "Security Camera"])
        layout.addWidget(self.device_type_dropdown)

        self.device_id_label = QLabel("Device ID:")
        layout.addWidget(self.device_id_label)

        self.device_id_textfield = QLineEdit()
        layout.addWidget(self.device_id_textfield)

        self.add_device_button = QPushButton("Add Device")
        self.add_device_button.clicked.connect(self.add_new_device)
        layout.addWidget(self.add_device_button)

        self.remove_device_label = QLabel("Remove Device:")
        layout.addWidget(self.remove_device_label)

        self.remove_device_dropdown = QComboBox()
        self.remove_device_dropdown.addItem("Select Device to Remove")
        layout.addWidget(self.remove_device_dropdown)

        self.remove_device_button = QPushButton("Remove Device")
        self.remove_device_button.clicked.connect(self.remove_selected_device)
        layout.addWidget(self.remove_device_button)

        # Monitoring Section
        self.monitoring_label = QLabel("Monitoring:")
        layout.addWidget(self.monitoring_label)

        self.monitoring_text = QTextEdit()
        layout.addWidget(self.monitoring_text)

        layout.setContentsMargins(20, 20, 20, 20)
        self.central_widget.setLayout(layout)

    def add_new_device(self):
        """Add a new device to the smart home system based on user input."""
        device_type = self.device_type_dropdown.currentText()
        device_id = self.device_id_textfield.text()

        if not device_id:
            self.show_message("Error", "Device ID is not provided.")
            return

        # Check if the device ID already exists for the given device type
        existing_ids = [device.get_id() for device in self.automation_system.get_devices() if
                        isinstance(device, SmartLight) and device_type == "Smart Light"
                        or isinstance(device, Thermostat) and device_type == "Thermostat"
                        or isinstance(device, SecurityCamera) and device_type == "Security Camera"]
        if device_id in existing_ids:
            self.show_message("Error", f"Device with ID '{device_id}' already exists for the selected device type.")
            return

        if device_type == "Smart Light":
            self.smart_light = SmartLight(id=device_id, status=False, brightness=0.0)
            try:
                self.automation_system.add_device(self.smart_light)
                self.update_remove_device_dropdown()
                self.show_message("Successful Operation", "Smart Light added successfully.")
            except Exception as e:
                self.show_message("Error", f"Error adding Smart Light: {str(e)}")
            self.update_device_status()
        elif device_type == "Thermostat":
            self.thermostat = Thermostat(id=device_id, status=False, temperature=0.0)
            try:
                self.automation_system.add_device(self.thermostat)
                self.update_remove_device_dropdown()
                self.show_message("Success", "Thermostat added successfully.")
            except Exception as e:
                self.show_message("Error", f"Error adding Thermostat: {str(e)}")
            self.update_device_status()
        elif device_type == "Security Camera":
            self.security_camera = SecurityCamera(id=device_id, status=False,
                                                  security_status="Click 'Show Security Status' to get the status")
            try:
                self.automation_system.add_device(self.security_camera)
                self.update_remove_device_dropdown()
                self.show_message("Success", "Security Camera added successfully.")
            except Exception as e:
                self.show_message("Error", f"Error adding Security Camera: {str(e)}")
            self.update_device_status()

    def show_message(self, title, message):
        """Show a message box with the given title and message."""
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()

    def update_remove_device_dropdown(self):
        """Update the remove device dropdown with the list of devices in the smart home system."""
        self.remove_device_dropdown.clear()
        self.remove_device_dropdown.addItem("Select Device to Remove")

        for device in self.automation_system.get_devices():
            if isinstance(device, SmartLight):
                item_text = f"SmartLight#{device.get_id()}"
            elif isinstance(device, SecurityCamera):
                item_text = f"SecurityCamera#{device.get_id()}"
            elif isinstance(device, Thermostat):
                item_text = f"Thermostat#{device.get_id()}"
            else:
                item_text = device.get_id()
            self.remove_device_dropdown.addItem(item_text, userData=device.get_id())

    def remove_selected_device(self):
        """Remove the selected device from the smart home system."""
        selected_device_index = self.remove_device_dropdown.currentIndex()
        if selected_device_index != 0:
            device_id = self.remove_device_dropdown.itemData(selected_device_index)
            if device_id:

                if self.smart_light and self.smart_light.get_id() == device_id:
                    self.smart_light = None

                elif self.thermostat and self.thermostat.get_id() == device_id:
                    self.thermostat = None

                elif self.security_camera and self.security_camera.get_id() == device_id:
                    self.security_camera = None

                self.automation_system.remove_device(device_id)
                self.update_remove_device_dropdown()
                self.update_device_status()

    def update_brightness_slider(self):
        """Update the brightness slider based on the status of the smart light."""
        current_value = self.light_brightness_slider.value()
        if self.smart_light.status:
            if current_value < 100:
                new_value = current_value + 1
                self.light_brightness_slider.setValue(new_value)
            else:
                self.toggle_timer.stop()
        else:
            if current_value > 0:
                new_value = current_value - 1
                self.light_brightness_slider.setValue(new_value)
            else:
                self.toggle_timer.stop()
        self.update_device_status()

    def update_device_status(self):
        """Update the status of devices on the monitoring dashboard."""
        if self.smart_light:
            light_status = "ON" if self.smart_light.status else "OFF"
            light_brightness = self.light_brightness_slider.value()
        else:
            light_status = "N/A"
            light_brightness = 0

        if self.thermostat:
            thermostat_status = "ON" if self.thermostat.status else "OFF"
            thermostat_temperature = self.thermostat_slider.value()
        else:
            thermostat_status = "N/A"
            thermostat_temperature = 0

        if self.security_camera:
            security_camera_status = "ON" if self.security_camera.status else "OFF"
            security_status = self.security_camera.security_status if self.security_camera.status else "Unable to get the security status, the camera is OFF"
        else:
            security_camera_status = "N/A"
            security_status = "N/A"

        self.show_security_status_button.setEnabled(self.security_camera.status if self.security_camera else False)
        self.thermostat_slider.setEnabled(self.thermostat.status if self.thermostat else False)
        self.light_brightness_slider.setEnabled(self.smart_light.status if self.smart_light else False)

        if self.smart_light and self.smart_light.status:
            # Slider is enabled
            self.light_brightness_slider.setEnabled(True)
            self.light_brightness_slider.setStyleSheet(
                """
               QSlider {
                   height: 20px; 
               }
               QSlider::groove:horizontal {
                   background-color: #e0e0e0; 
                   border: 1px solid #cccccc; 
                   height: 4px;
                   margin: 2px 0; 
               }
               QSlider::handle:horizontal {
                   background-color: green; 
                   border: 1px solid #cccccc; 
                   width: 16px; 
                   margin: -7px 0; 
                   border-radius: 8px; 
               }
               """
            )
        else:
            self.light_brightness_slider.setEnabled(False)
            self.light_brightness_slider.setStyleSheet(
                """
                QSlider {
                    height: 20px; /* Height of the slider track */
                }
                QSlider::groove:horizontal {
                    background-color: #e0e0e0; 
                    border: 1px solid #cccccc;
                    height: 4px; 
                    margin: 2px 0;
                }
                QSlider::handle:horizontal {
                    background-color: gray; 
                    border: 1px solid #cccccc; 
                    width: 16px; 
                    margin: -7px 0; 
                    border-radius: 8px; 
                }
                """
            )

        status_text = (
            f"Smart Light: {light_status} (Brightness: {light_brightness})\n"
            f"Thermostat: {thermostat_status} (Thermostat Temperature: {thermostat_temperature}℃)\n"
            f"Security Camera: {security_camera_status}\n"
            f"Security Status: {security_status}"
        )
        self.monitoring_text.setPlainText(status_text)

    def show_security_status(self):
        """Show the security status of the security camera."""
        if self.security_camera:
            self.security_camera.set_random_security_status()
            self.update_device_status()


# Example usage:
# Replace the following lines with your actual smart home system initialization
class AutomationSystem:
    def __init__(self):
        self.devices = []

    def add_device(self, device):
        self.devices.append(device)

    def remove_device(self, device_id):
        self.devices = [device for device in self.devices if device.get_id() != device_id]

    def get_devices(self):
        return self.devices


# Create a QApplication instance and run the event loop
import sys
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)

automation_system = AutomationSystem()
gui = SmartHomeGUI(automation_system)
gui.show()

sys.exit(app.exec_())
