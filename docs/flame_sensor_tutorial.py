#!/usr/bin/env python3
"""
TUTORIEL : Programmation Capteur de Flamme Raspberry Pi 4
========================================================

Ce fichier contient des exemples progressifs pour apprendre
à programmer avec votre capteur de flamme.

Matériel requis :
- Raspberry Pi 4
- Capteur de flamme IR (760-1100nm)
- Câbles de connexion

Connexions :
VCC (capteur) -> Pin 2 (5V) du Raspberry Pi
GND (capteur) -> Pin 6 (GND) du Raspberry Pi  
DO (capteur)  -> Pin 11 (GPIO17) du Raspberry Pi
"""

# ============================================================================
# EXEMPLE 1 : LECTURE SIMPLE DU CAPTEUR
# ============================================================================

def exemple_1_lecture_simple():
    """
    Premier exemple : lire l'état du capteur une seule fois
    """
    print("=== EXEMPLE 1 : Lecture Simple ===")
    
    # Importer la bibliothèque GPIO
    from gpiozero import InputDevice
    import time
    
    # Créer l'objet capteur sur GPIO17
    capteur_flamme = InputDevice(17)
    
    # Lire l'état du capteur
    if capteur_flamme.is_active:
        print("Aucune flamme détectée")
    else:
        print("🔥 FLAMME DÉTECTÉE!")
    
    # Fermer proprement
    capteur_flamme.close()

# ============================================================================
# EXEMPLE 2 : SURVEILLANCE CONTINUE
# ============================================================================

def exemple_2_surveillance_continue():
    """
    Deuxième exemple : surveiller en continu pendant 30 secondes
    """
    print("=== EXEMPLE 2 : Surveillance Continue ===")
    
    from gpiozero import InputDevice
    import time
    
    capteur_flamme = InputDevice(17)
    
    print("Surveillance pendant 30 secondes...")
    print("Approchez une flamme du capteur pour tester")
    
    debut = time.time()
    while time.time() - debut < 30:  # 30 secondes
        if not capteur_flamme.is_active:  # Flamme détectée
            print(f"🔥 FLAMME DÉTECTÉE à {time.strftime('%H:%M:%S')}")
            time.sleep(1)  # Éviter le spam
        else:
            print(".", end="", flush=True)  # Point pour montrer que ça fonctionne
            time.sleep(0.5)
    
    print("\nSurveillance terminée")
    capteur_flamme.close()

# ============================================================================
# EXEMPLE 3 : COMPTEUR DE DÉTECTIONS
# ============================================================================

def exemple_3_compteur_detections():
    """
    Troisième exemple : compter le nombre de détections
    """
    print("=== EXEMPLE 3 : Compteur de Détections ===")
    
    from gpiozero import InputDevice
    import time
    
    capteur_flamme = InputDevice(17)
    compteur = 0
    flamme_precedente = False
    
    print("Surveillance avec compteur (Ctrl+C pour arrêter)")
    
    try:
        while True:
            flamme_actuelle = not capteur_flamme.is_active
            
            # Détecter un changement d'état (nouvelle flamme)
            if flamme_actuelle and not flamme_precedente:
                compteur += 1
                print(f"🔥 Détection #{compteur} - {time.strftime('%H:%M:%S')}")
            elif not flamme_actuelle and flamme_precedente:
                print("✅ Flamme éteinte")
            
            flamme_precedente = flamme_actuelle
            time.sleep(0.2)  # Vérifier 5 fois par seconde
            
    except KeyboardInterrupt:
        print(f"\nArrêt demandé. Total détections: {compteur}")
    
    capteur_flamme.close()

# ============================================================================
# EXEMPLE 4 : AVEC NOTIFICATIONS SONORES
# ============================================================================

def exemple_4_avec_son():
    """
    Quatrième exemple : ajouter des bips sonores
    """
    print("=== EXEMPLE 4 : Avec Notifications Sonores ===")
    
    from gpiozero import InputDevice, Buzzer
    import time
    
    capteur_flamme = InputDevice(17)
    
    # Buzzer optionnel sur GPIO18 (si vous en avez un)
    try:
        buzzer = Buzzer(18)
        son_disponible = True
        print("Buzzer détecté sur GPIO18")
    except:
        buzzer = None
        son_disponible = False
        print("Pas de buzzer - notifications console seulement")
    
    print("Surveillance avec son (Ctrl+C pour arrêter)")
    
    try:
        while True:
            if not capteur_flamme.is_active:  # Flamme détectée
                print("🔥 ALERTE FLAMME!")
                
                if son_disponible:
                    # 3 bips courts
                    for i in range(3):
                        buzzer.on()
                        time.sleep(0.2)
                        buzzer.off()
                        time.sleep(0.1)
                
                time.sleep(2)  # Pause avant prochaine vérification
            else:
                time.sleep(0.5)
                
    except KeyboardInterrupt:
        print("\nArrêt demandé")
    
    capteur_flamme.close()
    if buzzer:
        buzzer.close()

# ============================================================================
# EXEMPLE 5 : SAUVEGARDE DANS UN FICHIER
# ============================================================================

def exemple_5_sauvegarde_fichier():
    """
    Cinquième exemple : sauvegarder les détections dans un fichier
    """
    print("=== EXEMPLE 5 : Sauvegarde dans Fichier ===")
    
    from gpiozero import InputDevice
    import time
    from datetime import datetime
    
    capteur_flamme = InputDevice(17)
    nom_fichier = f"detections_flamme_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    print(f"Surveillance avec sauvegarde dans: {nom_fichier}")
    print("Ctrl+C pour arrêter")
    
    try:
        with open(nom_fichier, 'w') as fichier:
            fichier.write("=== LOG DÉTECTIONS FLAMME ===\n")
            fichier.write(f"Début: {datetime.now()}\n\n")
            
            flamme_precedente = False
            compteur = 0
            
            while True:
                flamme_actuelle = not capteur_flamme.is_active
                maintenant = datetime.now()
                
                if flamme_actuelle and not flamme_precedente:
                    compteur += 1
                    message = f"🔥 DÉTECTION #{compteur} - {maintenant}"
                    print(message)
                    fichier.write(message + "\n")
                    fichier.flush()  # Sauvegarder immédiatement
                
                elif not flamme_actuelle and flamme_precedente:
                    message = f"✅ Flamme éteinte - {maintenant}"
                    print(message)
                    fichier.write(message + "\n")
                    fichier.flush()
                
                flamme_precedente = flamme_actuelle
                time.sleep(0.3)
                
    except KeyboardInterrupt:
        print(f"\nArrêt demandé. Fichier sauvegardé: {nom_fichier}")
    
    capteur_flamme.close()

# ============================================================================
# EXEMPLE 6 : CLASSE COMPLÈTE RÉUTILISABLE
# ============================================================================

class DetecteurFlamme:
    """
    Classe complète pour gérer le capteur de flamme
    """
    
    def __init__(self, gpio_pin=17):
        """Initialiser le détecteur"""
        from gpiozero import InputDevice
        self.capteur = InputDevice(gpio_pin)
        self.compteur_detections = 0
        self.en_fonctionnement = False
        
    def detecter_flamme(self):
        """Retourne True si une flamme est détectée"""
        return not self.capteur.is_active
    
    def surveiller(self, duree_secondes=None, callback=None):
        """
        Surveiller pendant une durée donnée
        callback: fonction à appeler lors d'une détection
        """
        import time
        from datetime import datetime
        
        self.en_fonctionnement = True
        debut = time.time()
        flamme_precedente = False
        
        print(f"Surveillance démarrée - {datetime.now()}")
        
        try:
            while self.en_fonctionnement:
                # Vérifier la durée si spécifiée
                if duree_secondes and (time.time() - debut) > duree_secondes:
                    break
                
                flamme_actuelle = self.detecter_flamme()
                
                # Nouvelle détection
                if flamme_actuelle and not flamme_precedente:
                    self.compteur_detections += 1
                    
                    if callback:
                        callback(self.compteur_detections)
                    else:
                        print(f"🔥 Détection #{self.compteur_detections}")
                
                # Flamme éteinte
                elif not flamme_actuelle and flamme_precedente:
                    print("✅ Flamme éteinte")
                
                flamme_precedente = flamme_actuelle
                time.sleep(0.2)
                
        except KeyboardInterrupt:
            print("\nArrêt demandé par l'utilisateur")
        
        self.en_fonctionnement = False
        print(f"Surveillance terminée. Total: {self.compteur_detections} détections")
    
    def arreter(self):
        """Arrêter la surveillance"""
        self.en_fonctionnement = False
    
    def fermer(self):
        """Fermer proprement le capteur"""
        self.capteur.close()

def exemple_6_classe_complete():
    """
    Sixième exemple : utiliser la classe complète
    """
    print("=== EXEMPLE 6 : Classe Complète ===")
    
    # Fonction callback personnalisée
    def ma_fonction_alerte(numero_detection):
        print(f"🚨 ALERTE PERSONNALISÉE - Détection #{numero_detection}")
        # Ici vous pourriez ajouter d'autres actions :
        # - Envoyer un email
        # - Allumer une LED
        # - Jouer un son
        # - Envoyer une notification
    
    # Créer le détecteur
    detecteur = DetecteurFlamme(gpio_pin=17)
    
    # Surveiller pendant 60 secondes avec callback personnalisé
    detecteur.surveiller(duree_secondes=60, callback=ma_fonction_alerte)
    
    # Fermer proprement
    detecteur.fermer()

# ============================================================================
# MENU PRINCIPAL POUR TESTER LES EXEMPLES
# ============================================================================

def menu_principal():
    """Menu pour choisir quel exemple exécuter"""
    
    print("=" * 60)
    print("    TUTORIEL CAPTEUR DE FLAMME RASPBERRY PI 4")
    print("=" * 60)
    print()
    print("Choisissez un exemple à exécuter :")
    print("1. Lecture simple du capteur")
    print("2. Surveillance continue (30s)")
    print("3. Compteur de détections")
    print("4. Avec notifications sonores")
    print("5. Sauvegarde dans fichier")
    print("6. Classe complète réutilisable")
    print("0. Quitter")
    print()
    
    while True:
        try:
            choix = input("Votre choix (0-6) : ")
            
            if choix == "1":
                exemple_1_lecture_simple()
            elif choix == "2":
                exemple_2_surveillance_continue()
            elif choix == "3":
                exemple_3_compteur_detections()
            elif choix == "4":
                exemple_4_avec_son()
            elif choix == "5":
                exemple_5_sauvegarde_fichier()
            elif choix == "6":
                exemple_6_classe_complete()
            elif choix == "0":
                print("Au revoir !")
                break
            else:
                print("Choix invalide. Essayez encore.")
                continue
                
            print("\n" + "="*50)
            print("Exemple terminé. Choisissez le suivant ou 0 pour quitter.")
            
        except KeyboardInterrupt:
            print("\nAu revoir !")
            break
        except Exception as e:
            print(f"Erreur : {e}")

# ============================================================================
# POINT D'ENTRÉE DU PROGRAMME
# ============================================================================

if __name__ == "__main__":
    menu_principal()

