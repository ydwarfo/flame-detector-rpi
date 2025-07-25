#!/usr/bin/env python3
"""
Détecteur de Flamme Raspberry Pi - Version de Base
=================================================

Application simple pour détecter la présence d'une flamme de bougie
avec un capteur IR et un Raspberry Pi 4.

Auteur: Assistant IA
Date: Juillet 2025
Matériel requis:
- Raspberry Pi 4
- Capteur de flamme IR (760-1100nm)
- Câbles de connexion

Connexions:
- VCC du capteur -> Pin 2 (5V) du Raspberry Pi
- GND du capteur -> Pin 6 (GND) du Raspberry Pi  
- DO du capteur -> Pin 11 (GPIO17) du Raspberry Pi
"""

import time
import signal
import sys
from datetime import datetime

try:
    from gpiozero import InputDevice
except ImportError:
    print("Erreur: La bibliothèque gpiozero n'est pas installée.")
    print("Installez-la avec: sudo apt install python3-gpiozero")
    sys.exit(1)

class FlameDetector:
    """Classe principale pour la détection de flamme."""
    
    def __init__(self, gpio_pin=17):
        """
        Initialise le détecteur de flamme.
        
        Args:
            gpio_pin (int): Numéro du pin GPIO connecté au capteur (défaut: 17)
        """
        self.gpio_pin = gpio_pin
        self.flame_sensor = None
        self.running = False
        self.flame_detected = False
        self.detection_count = 0
        
        # Configuration du gestionnaire de signal pour arrêt propre
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
    def _signal_handler(self, signum, frame):
        """Gestionnaire pour arrêt propre du programme."""
        print(f"\n[{self._get_timestamp()}] Signal reçu ({signum}). Arrêt du détecteur...")
        self.stop()
        
    def _get_timestamp(self):
        """Retourne un timestamp formaté."""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
    def initialize(self):
        """Initialise le capteur GPIO."""
        try:
            self.flame_sensor = InputDevice(self.gpio_pin)
            print(f"[{self._get_timestamp()}] Détecteur de flamme initialisé sur GPIO{self.gpio_pin}")
            return True
        except Exception as e:
            print(f"[{self._get_timestamp()}] Erreur d'initialisation: {e}")
            return False
            
    def check_flame(self):
        """
        Vérifie la présence d'une flamme.
        
        Returns:
            bool: True si une flamme est détectée, False sinon
        """
        if not self.flame_sensor:
            return False
            
        # Le capteur retourne False (is_active=False) quand une flamme est détectée
        return not self.flame_sensor.is_active
        
    def start_monitoring(self, check_interval=1.0):
        """
        Démarre la surveillance continue.
        
        Args:
            check_interval (float): Intervalle entre les vérifications en secondes
        """
        if not self.initialize():
            return
            
        self.running = True
        print(f"[{self._get_timestamp()}] Démarrage de la surveillance (intervalle: {check_interval}s)")
        print("Appuyez sur Ctrl+C pour arrêter")
        print("-" * 50)
        
        try:
            while self.running:
                current_flame_state = self.check_flame()
                
                # Détection d'un changement d'état
                if current_flame_state != self.flame_detected:
                    self.flame_detected = current_flame_state
                    
                    if self.flame_detected:
                        self.detection_count += 1
                        print(f"[{self._get_timestamp()}] 🔥 FLAMME DÉTECTÉE! (Détection #{self.detection_count})")
                    else:
                        print(f"[{self._get_timestamp()}] ✅ Flamme éteinte")
                
                time.sleep(check_interval)
                
        except Exception as e:
            print(f"[{self._get_timestamp()}] Erreur pendant la surveillance: {e}")
        finally:
            self.stop()
            
    def stop(self):
        """Arrête la surveillance."""
        self.running = False
        if self.flame_sensor:
            self.flame_sensor.close()
        print(f"[{self._get_timestamp()}] Surveillance arrêtée. Total détections: {self.detection_count}")

def main():
    """Fonction principale."""
    print("=" * 60)
    print("    DÉTECTEUR DE FLAMME RASPBERRY PI - VERSION DE BASE")
    print("=" * 60)
    print()
    
    # Création et démarrage du détecteur
    detector = FlameDetector(gpio_pin=17)
    
    try:
        # Démarrage de la surveillance avec vérification toutes les secondes
        detector.start_monitoring(check_interval=1.0)
    except KeyboardInterrupt:
        print("\nArrêt demandé par l'utilisateur")
    except Exception as e:
        print(f"Erreur inattendue: {e}")
    finally:
        detector.stop()

if __name__ == "__main__":
    main()

