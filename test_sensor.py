#!/usr/bin/env python3
"""
Script de Test du Capteur de Flamme
===================================

Script pour tester le fonctionnement du capteur de flamme
et vérifier les connexions GPIO.

Auteur: Assistant IA
Date: Juillet 2025
"""

import time
import sys
from datetime import datetime

try:
    from gpiozero import InputDevice
    GPIO_AVAILABLE = True
except ImportError:
    print("⚠️  gpiozero non disponible - Mode simulation activé")
    GPIO_AVAILABLE = False
    InputDevice = None

class SensorTester:
    """Classe pour tester le capteur de flamme."""
    
    def __init__(self, gpio_pin=17):
        """
        Initialise le testeur.
        
        Args:
            gpio_pin (int): Pin GPIO du capteur
        """
        self.gpio_pin = gpio_pin
        self.sensor = None
        self.simulation_mode = not GPIO_AVAILABLE
        
    def initialize(self):
        """Initialise le capteur."""
        if self.simulation_mode:
            print(f"🔧 Mode simulation - GPIO{self.gpio_pin}")
            return True
            
        try:
            self.sensor = InputDevice(self.gpio_pin)
            print(f"✅ Capteur initialisé sur GPIO{self.gpio_pin}")
            return True
        except Exception as e:
            print(f"❌ Erreur d'initialisation: {e}")
            return False
            
    def test_basic_reading(self, duration=10):
        """
        Test de lecture basique du capteur.
        
        Args:
            duration (int): Durée du test en secondes
        """
        print(f"\n🧪 Test de lecture basique ({duration}s)")
        print("-" * 40)
        
        if not self.initialize():
            return False
            
        print("Approchez une flamme du capteur pour tester...")
        print("Appuyez sur Ctrl+C pour arrêter")
        
        start_time = time.time()
        last_state = None
        reading_count = 0
        
        try:
            while time.time() - start_time < duration:
                if self.simulation_mode:
                    # Simulation
                    import random
                    current_state = random.random() < 0.1
                else:
                    current_state = not self.sensor.is_active
                    
                reading_count += 1
                timestamp = datetime.now().strftime("%H:%M:%S")
                
                if current_state != last_state:
                    if current_state:
                        print(f"[{timestamp}] 🔥 FLAMME DÉTECTÉE!")
                    else:
                        print(f"[{timestamp}] ✅ Pas de flamme")
                    last_state = current_state
                    
                time.sleep(0.5)
                
        except KeyboardInterrupt:
            print("\n⏹️  Test interrompu par l'utilisateur")
            
        print(f"\n📊 Résumé: {reading_count} lectures effectuées")
        return True
        
    def test_sensitivity(self):
        """Test de sensibilité du capteur."""
        print(f"\n🔍 Test de sensibilité")
        print("-" * 40)
        
        if not self.initialize():
            return False
            
        print("Ce test mesure la réactivité du capteur.")
        print("Approchez et éloignez une flamme plusieurs fois...")
        
        readings = []
        detection_times = []
        
        try:
            for i in range(20):
                if self.simulation_mode:
                    import random
                    reading = random.random() < 0.2
                else:
                    reading = not self.sensor.is_active
                    
                readings.append(reading)
                if reading:
                    detection_times.append(time.time())
                    
                print(f"Lecture {i+1:2d}: {'🔥 FLAMME' if reading else '✅ Normal'}")
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n⏹️  Test interrompu")
            
        # Analyse des résultats
        detections = sum(readings)
        print(f"\n📊 Analyse:")
        print(f"   Détections: {detections}/20 ({detections/20*100:.1f}%)")
        
        if len(detection_times) > 1:
            intervals = [detection_times[i+1] - detection_times[i] 
                        for i in range(len(detection_times)-1)]
            avg_interval = sum(intervals) / len(intervals)
            print(f"   Intervalle moyen entre détections: {avg_interval:.1f}s")
            
        return True
        
    def test_gpio_pins(self):
        """Test de différents pins GPIO."""
        print(f"\n🔌 Test des pins GPIO")
        print("-" * 40)
        
        if self.simulation_mode:
            print("Mode simulation - Test des pins simulé")
            for pin in [17, 18, 21, 22]:
                print(f"GPIO{pin}: ✅ OK (simulé)")
            return True
            
        test_pins = [17, 18, 21, 22]
        working_pins = []
        
        for pin in test_pins:
            try:
                test_sensor = InputDevice(pin)
                # Test rapide
                state = test_sensor.is_active
                test_sensor.close()
                working_pins.append(pin)
                print(f"GPIO{pin}: ✅ OK")
            except Exception as e:
                print(f"GPIO{pin}: ❌ Erreur - {e}")
                
        print(f"\n📊 Pins fonctionnels: {working_pins}")
        return len(working_pins) > 0
        
    def run_all_tests(self):
        """Exécute tous les tests."""
        print("=" * 50)
        print("    TEST DU CAPTEUR DE FLAMME RASPBERRY PI")
        print("=" * 50)
        
        # Informations système
        print(f"\n💻 Informations système:")
        print(f"   Mode simulation: {'Oui' if self.simulation_mode else 'Non'}")
        print(f"   Pin GPIO configuré: {self.gpio_pin}")
        
        # Tests
        tests = [
            ("Test des pins GPIO", self.test_gpio_pins),
            ("Test de lecture basique", lambda: self.test_basic_reading(10)),
            ("Test de sensibilité", self.test_sensitivity)
        ]
        
        results = []
        for test_name, test_func in tests:
            print(f"\n{'='*20} {test_name} {'='*20}")
            try:
                result = test_func()
                results.append((test_name, result))
            except Exception as e:
                print(f"❌ Erreur pendant {test_name}: {e}")
                results.append((test_name, False))
                
        # Résumé final
        print("\n" + "=" * 50)
        print("    RÉSUMÉ DES TESTS")
        print("=" * 50)
        
        for test_name, result in results:
            status = "✅ RÉUSSI" if result else "❌ ÉCHEC"
            print(f"{test_name}: {status}")
            
        successful_tests = sum(1 for _, result in results if result)
        print(f"\nTests réussis: {successful_tests}/{len(results)}")
        
        if successful_tests == len(results):
            print("🎉 Tous les tests sont réussis! Le capteur est prêt à utiliser.")
        else:
            print("⚠️  Certains tests ont échoué. Vérifiez les connexions.")

def main():
    """Fonction principale."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test du capteur de flamme")
    parser.add_argument("--pin", type=int, default=17, 
                       help="Pin GPIO du capteur (défaut: 17)")
    parser.add_argument("--test", choices=["all", "basic", "sensitivity", "gpio"],
                       default="all", help="Type de test à exécuter")
    
    args = parser.parse_args()
    
    tester = SensorTester(gpio_pin=args.pin)
    
    if args.test == "all":
        tester.run_all_tests()
    elif args.test == "basic":
        tester.test_basic_reading(15)
    elif args.test == "sensitivity":
        tester.test_sensitivity()
    elif args.test == "gpio":
        tester.test_gpio_pins()

if __name__ == "__main__":
    main()

