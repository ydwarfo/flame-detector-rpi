#!/bin/bash
# Script d'installation pour le Détecteur de Flamme Raspberry Pi
# Auteur: Assistant IA
# Date: Juillet 2025

set -e

echo "=============================================="
echo "  Installation Détecteur de Flamme RPi"
echo "=============================================="
echo

# Vérification que nous sommes sur Raspberry Pi
if ! grep -q "Raspberry Pi" /proc/cpuinfo 2>/dev/null; then
    echo "⚠️  Attention: Ce script est conçu pour Raspberry Pi"
    echo "   Il peut fonctionner sur d'autres systèmes mais certaines fonctionnalités peuvent être limitées."
    echo
fi

# Mise à jour du système
echo "📦 Mise à jour du système..."
sudo apt update
sudo apt upgrade -y

# Installation des dépendances système
echo "📦 Installation des dépendances système..."
sudo apt install -y python3 python3-pip python3-venv git

# Installation des bibliothèques GPIO
echo "📦 Installation des bibliothèques GPIO..."
sudo apt install -y python3-gpiozero python3-rpi.gpio

# Installation de l'outil de lecture audio (MP3 via ALSA, sans display)
echo "📦 Installation de mpg123 (lecture audio)..."
sudo apt install -y mpg123

# Installation de Flask pour la version web
echo "📦 Installation de Flask..."
pip3 install flask

# Création du répertoire de travail
INSTALL_DIR="$HOME/flame_detector"
echo "📁 Création du répertoire d'installation: $INSTALL_DIR"
mkdir -p "$INSTALL_DIR"

# Copie des fichiers (si exécuté depuis le répertoire du projet)
if [ -f "flame_detector_basic.py" ]; then
    echo "📋 Copie des fichiers du projet..."
    cp *.py "$INSTALL_DIR/"
    cp config.json "$INSTALL_DIR/"
    cp README.md "$INSTALL_DIR/" 2>/dev/null || true
fi

# Configuration des permissions
echo "🔧 Configuration des permissions..."
chmod +x "$INSTALL_DIR"/*.py

# Création du service systemd pour démarrage automatique
echo "🔧 Création du service systemd..."
sudo tee /etc/systemd/system/flame-detector.service > /dev/null << EOF
[Unit]
Description=Flame Detector Service
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=$INSTALL_DIR
ExecStart=/usr/bin/python3 $INSTALL_DIR/flame_detector_advanced.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Activation du service (optionnel)
echo "🔧 Configuration du service systemd..."
sudo systemctl daemon-reload
echo "   Service créé. Pour l'activer au démarrage:"
echo "   sudo systemctl enable flame-detector"
echo "   sudo systemctl start flame-detector"

# Configuration du GPIO
echo "🔧 Configuration GPIO..."
echo "   Ajout de l'utilisateur au groupe gpio..."
sudo usermod -a -G gpio $USER

# Création d'un script de lancement rapide
echo "🔧 Création des scripts de lancement..."
cat > "$INSTALL_DIR/start_basic.sh" << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
python3 flame_detector_basic.py
EOF

cat > "$INSTALL_DIR/start_advanced.sh" << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
python3 flame_detector_advanced.py
EOF

cat > "$INSTALL_DIR/start_web.sh" << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
echo "Interface web disponible sur:"
echo "  - Local: http://localhost:5000"
echo "  - Réseau: http://$(hostname -I | awk '{print $1}'):5000"
echo
python3 flame_detector_web.py
EOF

chmod +x "$INSTALL_DIR"/*.sh

# Test de l'installation
echo "🧪 Test de l'installation..."
cd "$INSTALL_DIR"
python3 -c "
try:
    from gpiozero import InputDevice
    print('✅ gpiozero installé correctement')
except ImportError as e:
    print('❌ Erreur gpiozero:', e)

try:
    from flask import Flask
    print('✅ Flask installé correctement')
except ImportError as e:
    print('❌ Erreur Flask:', e)

import json
try:
    with open('config.json', 'r') as f:
        config = json.load(f)
    print('✅ Configuration chargée correctement')
except Exception as e:
    print('❌ Erreur configuration:', e)
"

echo
echo "=============================================="
echo "  ✅ Installation terminée avec succès!"
echo "=============================================="
echo
echo "📁 Répertoire d'installation: $INSTALL_DIR"
echo
echo "🚀 Pour démarrer le détecteur:"
echo "   Version de base:    $INSTALL_DIR/start_basic.sh"
echo "   Version avancée:    $INSTALL_DIR/start_advanced.sh"
echo "   Version web:        $INSTALL_DIR/start_web.sh"
echo
echo "🔧 Configuration:"
echo "   Éditez le fichier: $INSTALL_DIR/config.json"
echo
echo "🔌 Câblage du capteur de flamme:"
echo "   VCC (capteur) -> Pin 2 (5V) du Raspberry Pi"
echo "   GND (capteur) -> Pin 6 (GND) du Raspberry Pi"
echo "   DO (capteur)  -> Pin 11 (GPIO17) du Raspberry Pi"
echo
echo "📖 Consultez le README.md pour plus d'informations"
echo
echo "⚠️  N'oubliez pas de redémarrer pour que les permissions GPIO prennent effet!"
echo

