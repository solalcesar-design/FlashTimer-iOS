import toga
from toga.style import Pack
from toga.style.pack import COLUMN, CENTER
import threading
import time

# Chargement de la bibliothèque rubicon-objc pour communiquer avec l'iPhone
try:
    from rubicon.objc import objc_cls
    AVCaptureDevice = objc_cls('AVCaptureDevice')
except ImportError:
    AVCaptureDevice = None

class FlashTimer(toga.App):
    def startup(self):
        """Création de l'interface utilisateur"""
        self.main_window = toga.MainWindow(title="FlashTimer iOS")
        
        # Saisie du temps par l'utilisateur
        self.input_time = toga.TextInput(
            placeholder='Minutes (ex: 5)', 
            style=Pack(width=200, padding=10)
        )
        
        # Affichage de l'état actuel
        self.label_status = toga.Label('Prêt', style=Pack(padding=10))
        
        # Bouton pour lancer le compte à rebours
        self.button = toga.Button(
            'Lancer le Chrono', 
            on_press=self.start_timer, 
            style=Pack(padding=10, width=150)
        )

        # Mise en page (Layout)
        container = toga.Box(
            children=[self.input_time, self.button, self.label_status],
            style=Pack(direction=COLUMN, alignment=CENTER, padding=30)
        )
        
        self.main_window.content = container
        self.main_window.show()

    def set_torch(self, state):
        """Allume (True) ou éteint (False) la LED de l'iPhone"""
        if AVCaptureDevice:
            try:
                # Accès au matériel de l'iPhone
                device = AVCaptureDevice.defaultDeviceWithMediaType_('vide')
                if device and device.hasTorch():
                    device.lockForConfiguration_(None)
                    # 1 = ON, 0 = OFF
                    device.setTorchMode_(1 if state else 0)
                    device.unlockForConfiguration()
            except Exception as e:
                print(f"Erreur iOS: {e}")
        else:
            print("Environnement iOS non détecté.")

    def start_timer(self, widget):
        """Déclenche la lampe et le minuteur"""
        try:
            # Gestion de la saisie (remplacement de la virgule par un point)
            val = self.input_time.value.replace(',', '.')
            if not val:
                return
            
            minutes = float(val)
            seconds = int(minutes * 60)
            
            # Allumage et mise à jour de l'interface
            self.set_torch(True)
            self.button.enabled = False
            self.label_status.text = f"Allumé pour {minutes} min"
            
            # Lancement du chrono dans un thread pour ne pas bloquer l'app
            def run_timer():
                time.sleep(seconds)
                self.set_torch(False)
                self.label_status.text = "Terminé !"
                self.button.enabled = True
                
            threading.Thread(target=run_timer, daemon=True).start()
        except ValueError:
            self.label_status.text = "Entrez un nombre valide"

def main():
    return FlashTimer()