# Changelog

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-07-22

### Ajouté
- Version de base (`flame_detector_basic.py`) avec détection simple
- Version avancée (`flame_detector_advanced.py`) avec notifications
- Version web (`flame_detector_web.py`) avec interface responsive
- Configuration via fichier JSON
- Script d'installation automatique (`install.sh`)
- Script de test du capteur (`test_sensor.py`)
- Documentation complète (README.md)
- Guide de démarrage rapide (QUICK_START.md)
- Schémas de câblage illustrés
- API REST pour contrôle à distance
- Notifications email et sonores
- Journalisation avancée avec rotation
- Anti-rebond pour éviter les faux positifs
- Service systemd pour démarrage automatique
- Support multi-plateforme (simulation sur non-RPi)

### Fonctionnalités
- Détection temps réel de flammes IR (760-1100nm)
- Interface web responsive avec dashboard
- Historique des détections
- Configuration flexible via JSON
- Notifications multiples (console, son, email)
- Tests automatisés du capteur
- Installation en une commande
- Documentation technique complète

### Compatibilité
- Raspberry Pi 4 (recommandé)
- Raspberry Pi 3B/3B+
- Autres modèles RPi avec GPIO
- Python 3.7+
- Capteurs de flamme IR standard

## [Prévu] - Versions Futures

### [1.1.0] - À venir
- Interface mobile native
- Intégration MQTT/IoT
- Base de données pour historique long terme
- Graphiques de tendances
- Notifications push mobiles
- Support multi-capteurs
- Détection par caméra (IA)

### [1.2.0] - À venir
- Intégration domotique (Home Assistant)
- API GraphQL
- Tableau de bord avancé
- Alertes géolocalisées
- Support cloud (AWS IoT, Azure IoT)
- Machine learning pour réduction faux positifs

