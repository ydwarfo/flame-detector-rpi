# Développement Application Détection Flamme Raspberry Pi

## Phase 2: Développement de l'application Python

### Tâches à accomplir:
- [x] Créer l'application de base avec détection simple
- [x] Ajouter la journalisation des événements
- [x] Créer une version avec interface graphique (web)
- [x] Ajouter les notifications (email, son)
- [x] Créer une version avec serveur web
- [x] Ajouter la configuration via fichier JSON
- [x] Créer les tests unitaires (script de test)
- [x] Optimiser la sensibilité et réduire les faux positifs

### Fichiers créés:
- [x] flame_detector_basic.py - Version de base
- [x] flame_detector_advanced.py - Version avec notifications
- [x] flame_detector_web.py - Version avec interface web
- [x] config.json - Configuration
- [x] install.sh - Script d'installation
- [x] test_sensor.py - Tests du capteur

### Informations techniques collectées:
- Capteur: IR Flame Sensor Module (760-1100nm)
- Connexions: VCC->5V, GND->GND, DO->GPIO (17 ou 21)
- Bibliothèque: gpiozero (InputDevice)
- Logique: is_active = False quand flamme détectée

