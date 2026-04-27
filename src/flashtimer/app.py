import toga
from toga.style import Pack
from toga.style.pack import COLUMN, CENTER
import threading
import time

try:
    from rubicon.objc import objc_cls
    AVCaptureDevice = objc_cls('AVCaptureDevice')
except:
    AVCaptureDevice = None

class FlashTimer(toga.App):
    def startup(self):
        self.main_window = toga.MainWindow(title="FlashTimer")
        self.input_time = toga.TextInput(placeholder='Minutes', style=Pack(width=200, padding=10))
        self.label_status = toga.Label('Prêt', style=Pack(padding=10))
        self.button = toga.Button('Lancer', on_press=self.start_timer, style=Pack(padding=10, width=150))

        container = toga.Box(
            children=[self.input_time, self.button, self.label_status],
            style=Pack(direction=COLUMN, alignment=CENTER, padding=30)
        )
        self.main_window.content = container
        self.main_window.show()

    def set_torch(self, state):
        if AVCaptureDevice:
            device = AVCaptureDevice.defaultDeviceWithMediaType_('vide')
            if device and device.hasTorch():
                device.lockForConfiguration_(None)
                device.setTorchMode_(1 if state else 0)
                device.unlockForConfiguration()

    def start_timer(self, widget):
        try:
            minutes = float(self.input_time.value.replace(',', '.'))
            seconds = int(minutes * 60)
            self.set_torch(True)
            self.button.enabled = False
            self.label_status.text = f"Allumé ({minutes} min)"
            
            def run():
                time.sleep(seconds)
                self.set_torch(False)
                self.label_status.text = "Terminé !"
                self.button.enabled = True
            threading.Thread(target=run, daemon=True).start()
        except:
            self.label_status.text = "Erreur de saisie"

def main():
    return FlashTimer()
