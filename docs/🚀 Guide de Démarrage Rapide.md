# 🚀 Guide de Démarrage Rapide

## Installation en 5 Minutes

### 1. Préparation du Raspberry Pi
```bash
# Mise à jour du système
sudo apt update && sudo apt upgrade -y

# Installation des dépendances
sudo apt install -y python3 python3-pip python3-gpiozero
pip3 install flask
```

### 2. Câblage du Capteur
```
Capteur → Raspberry Pi
VCC    → Pin 2 (5V)
GND    → Pin 6 (GND)  
DO     → Pin 11 (GPIO17)
```

### 3. Test du Capteur
```bash
# Télécharger et tester
wget https://raw.githubusercontent.com/votre-repo/flame-detector/main/test_sensor.py
python3 test_sensor.py
```

### 4. Lancement de l'Application
```bash
# Version de base
python3 flame_detector_basic.py

# Version web (recommandée)
python3 flame_detector_web.py
# Puis ouvrir: http://localhost:5000
```

## Vérification Rapide

✅ **Le capteur fonctionne si :**
- Les LEDs du capteur s'allument
- Le test détecte une flamme de briquet
- Aucune erreur GPIO n'apparaît

❌ **Problèmes courants :**
- Vérifier les connexions (VCC, GND, DO)
- Ajouter l'utilisateur au groupe gpio : `sudo usermod -a -G gpio $USER`
- Redémarrer après changement de groupe

## Configuration Rapide

Éditez `config.json` pour :
- Changer le pin GPIO : `"flame_sensor_pin": 21`
- Ajuster la sensibilité : `"check_interval": 0.3`
- Activer les emails : `"email_enabled": true`

## Support

- 📖 Documentation complète : [README.md](README.md)
- 🔧 Dépannage : Section "Troubleshooting" du README
- 🐛 Problèmes : [GitHub Issues](https://github.com/votre-repo/flame-detector/issues)

