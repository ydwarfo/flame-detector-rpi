#!/usr/bin/env python3
"""
Détecteur de Flamme Raspberry Pi - Version Avancée
=================================================

Application avancée pour détecter la présence d'une flamme avec:
- Journalisation des événements
- Notifications sonores
- Notifications email (optionnel)
- Configuration via fichier JSON
- Gestion des faux positifs

Auteur: Assistant IA
Date: Juillet 2025
"""

import time
import signal
import sys
import json
import logging
import smtplib
import threading
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

try:
    from gpiozero import InputDevice, Buzzer
except ImportError:
    print("Erreur: La bibliothèque gpiozero n'est pas installée.")
    print("Installez-la avec: sudo apt install python3-gpiozero")
    sys.exit(1)

class FlameDetectorAdvanced:
    """Classe avancée pour la détection de flamme avec fonctionnalités étendues."""
    
    def __init__(self, config_file="config.json"):
        """
        Initialise le détecteur de flamme avancé.
        
        Args:
            config_file (str): Chemin vers le fichier de configuration
        """
        self.config_file = config_file
        self.config = self._load_config()
        
        # Initialisation des composants
        self.flame_sensor = None
        self.buzzer = None
        self.running = False
        self.flame_detected = False
        self.detection_count = 0
        self.last_detection_time = None
        
        # Configuration du logging
        self._setup_logging()
        
        # Configuration du gestionnaire de signal
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
    def _load_config(self):
        """Charge la configuration depuis le fichier JSON."""
        default_config = {
            "gpio": {
                "flame_sensor_pin": 17,
                "buzzer_pin": 18
            },
            "detection": {
                "check_interval": 0.5,
                "debounce_time": 2.0,
                "min_detection_duration": 1.0
            },
            "notifications": {
                "sound_enabled": True,
                "sound_duration": 3.0,
                "email_enabled": False,
                "email_config": {
                    "smtp_server": "smtp.gmail.com",
                    "smtp_port": 587,
                    "sender_email": "",
                    "sender_password": "",
                    "recipient_email": ""
                }
            },
            "logging": {
                "level": "INFO",
                "file": "flame_detector.log",
                "max_size_mb": 10
            }
        }
        
        try:
            if Path(self.config_file).exists():
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                # Fusionner avec la configuration par défaut
                return {**default_config, **config}
            else:
                # Créer le fichier de configuration par défaut
                with open(self.config_file, 'w') as f:
                    json.dump(default_config, f, indent=4)
                return default_config
        except Exception as e:
            print(f"Erreur lors du chargement de la configuration: {e}")
            return default_config
            
    def _setup_logging(self):
        """Configure le système de journalisation."""
        log_level = getattr(logging, self.config["logging"]["level"].upper())
        log_file = self.config["logging"]["file"]
        
        # Configuration du format de log
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Configuration du logger
        self.logger = logging.getLogger('FlameDetector')
        self.logger.setLevel(log_level)
        
        # Handler pour fichier
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        
        # Handler pour console
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
    def _signal_handler(self, signum, frame):
        """Gestionnaire pour arrêt propre du programme."""
        self.logger.info(f"Signal reçu ({signum}). Arrêt du détecteur...")
        self.stop()
        
    def initialize(self):
        """Initialise les capteurs et composants."""
        try:
            # Initialisation du capteur de flamme
            gpio_pin = self.config["gpio"]["flame_sensor_pin"]
            self.flame_sensor = InputDevice(gpio_pin)
            self.logger.info(f"Capteur de flamme initialisé sur GPIO{gpio_pin}")
            
            # Initialisation du buzzer (optionnel)
            if self.config["notifications"]["sound_enabled"]:
                buzzer_pin = self.config["gpio"]["buzzer_pin"]
                try:
                    self.buzzer = Buzzer(buzzer_pin)
                    self.logger.info(f"Buzzer initialisé sur GPIO{buzzer_pin}")
                except Exception as e:
                    self.logger.warning(f"Impossible d'initialiser le buzzer: {e}")
                    
            return True
        except Exception as e:
            self.logger.error(f"Erreur d'initialisation: {e}")
            return False
            
    def check_flame(self):
        """Vérifie la présence d'une flamme avec anti-rebond."""
        if not self.flame_sensor:
            return False
            
        # Lecture du capteur
        flame_state = not self.flame_sensor.is_active
        
        # Anti-rebond: vérifier la stabilité du signal
        if flame_state:
            time.sleep(self.config["detection"]["min_detection_duration"])
            # Vérifier à nouveau
            return not self.flame_sensor.is_active
            
        return False
        
    def _play_alarm_sound(self):
        """Joue le son d'alarme."""
        if self.buzzer and self.config["notifications"]["sound_enabled"]:
            try:
                duration = self.config["notifications"]["sound_duration"]
                self.buzzer.on()
                time.sleep(duration)
                self.buzzer.off()
            except Exception as e:
                self.logger.error(f"Erreur lors de la lecture du son: {e}")
                
    def _send_email_notification(self, message):
        """Envoie une notification par email."""
        if not self.config["notifications"]["email_enabled"]:
            return
            
        try:
            email_config = self.config["notifications"]["email_config"]
            
            # Création du message
            msg = MIMEMultipart()
            msg['From'] = email_config["sender_email"]
            msg['To'] = email_config["recipient_email"]
            msg['Subject'] = "🔥 Alerte Détection de Flamme - Raspberry Pi"
            
            body = f"""
            Alerte de sécurité - Détection de flamme
            
            {message}
            
            Heure: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            Détecteur: Raspberry Pi Flame Sensor
            
            Vérifiez immédiatement la zone surveillée.
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Envoi de l'email
            server = smtplib.SMTP(email_config["smtp_server"], email_config["smtp_port"])
            server.starttls()
            server.login(email_config["sender_email"], email_config["sender_password"])
            text = msg.as_string()
            server.sendmail(email_config["sender_email"], email_config["recipient_email"], text)
            server.quit()
            
            self.logger.info("Notification email envoyée")
            
        except Exception as e:
            self.logger.error(f"Erreur lors de l'envoi de l'email: {e}")
            
    def _handle_flame_detection(self):
        """Gère la détection d'une flamme."""
        self.detection_count += 1
        self.last_detection_time = datetime.now()
        
        message = f"FLAMME DÉTECTÉE! (Détection #{self.detection_count})"
        self.logger.warning(message)
        print(f"🔥 {message}")
        
        # Notifications en parallèle pour ne pas bloquer la détection
        if self.config["notifications"]["sound_enabled"]:
            threading.Thread(target=self._play_alarm_sound, daemon=True).start()
            
        if self.config["notifications"]["email_enabled"]:
            threading.Thread(
                target=self._send_email_notification, 
                args=(message,), 
                daemon=True
            ).start()
            
    def start_monitoring(self):
        """Démarre la surveillance continue."""
        if not self.initialize():
            return
            
        self.running = True
        check_interval = self.config["detection"]["check_interval"]
        debounce_time = self.config["detection"]["debounce_time"]
        
        self.logger.info(f"Démarrage de la surveillance (intervalle: {check_interval}s)")
        print("=" * 60)
        print("    DÉTECTEUR DE FLAMME RASPBERRY PI - VERSION AVANCÉE")
        print("=" * 60)
        print(f"Surveillance active - Intervalle: {check_interval}s")
        print("Appuyez sur Ctrl+C pour arrêter")
        print("-" * 50)
        
        last_flame_time = None
        
        try:
            while self.running:
                current_flame_state = self.check_flame()
                current_time = datetime.now()
                
                if current_flame_state:
                    if not self.flame_detected:
                        # Première détection
                        last_flame_time = current_time
                        self.flame_detected = True
                        
                    elif last_flame_time and (current_time - last_flame_time).total_seconds() >= debounce_time:
                        # Détection confirmée après debounce
                        self._handle_flame_detection()
                        last_flame_time = None
                        
                else:
                    if self.flame_detected:
                        self.flame_detected = False
                        last_flame_time = None
                        self.logger.info("Flamme éteinte")
                        print("✅ Flamme éteinte")
                
                time.sleep(check_interval)
                
        except Exception as e:
            self.logger.error(f"Erreur pendant la surveillance: {e}")
        finally:
            self.stop()
            
    def stop(self):
        """Arrête la surveillance."""
        self.running = False
        
        if self.flame_sensor:
            self.flame_sensor.close()
            
        if self.buzzer:
            self.buzzer.close()
            
        self.logger.info(f"Surveillance arrêtée. Total détections: {self.detection_count}")
        print(f"Surveillance arrêtée. Total détections: {self.detection_count}")

def main():
    """Fonction principale."""
    detector = FlameDetectorAdvanced()
    
    try:
        detector.start_monitoring()
    except KeyboardInterrupt:
        print("\nArrêt demandé par l'utilisateur")
    except Exception as e:
        print(f"Erreur inattendue: {e}")
    finally:
        detector.stop()

if __name__ == "__main__":
    main()

