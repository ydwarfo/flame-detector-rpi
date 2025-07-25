# 🚀 Guide de Démarrage - Programmation Capteur de Flamme

## 📋 Prérequis

### Matériel
- ✅ Raspberry Pi 4 (que vous avez)
- ✅ Capteur de flamme IR (que vous avez)
- ✅ Câbles de connexion
- ✅ Accès VNC ou clavier/souris

### Logiciels
- ✅ Raspberry Pi OS installé
- ✅ Python 3 (préinstallé)
- ✅ Bibliothèque gpiozero (préinstallée)

## 🔌 Vérification du Câblage

Avant de programmer, vérifiez vos connexions :

```
Capteur de Flamme    →    Raspberry Pi 4
================          ==============
VCC                →      Pin 2 (5V)
GND                →      Pin 6 (GND)
DO                 →      Pin 11 (GPIO17)
```

## 💻 Étape 1 : Ouvrir l'Environnement de Programmation

### Option A : Via VNC (Recommandée)
1. Connectez-vous via VNC depuis votre MacBook
2. Ouvrez le Terminal : Menu → Accessoires → Terminal
3. Ou ouvrez Thonny : Menu → Programmation → Thonny Python IDE

### Option B : Directement sur le Pi
1. Utilisez votre clavier/souris USB
2. Ouvrez le Terminal ou Thonny

## 💻 Étape 2 : Premier Test Simple

### Test Rapide en Une Ligne
```bash
# Dans le terminal, tapez :
python3 -c "from gpiozero import InputDevice; sensor=InputDevice(17); print('Flamme détectée!' if not sensor.is_active else 'Pas de flamme'); sensor.close()"
```

Si ça fonctionne, vous verrez :
- "Pas de flamme" (normal)
- "Flamme détectée!" (si vous approchez une flamme)

## 💻 Étape 3 : Votre Premier Programme

### Créer un fichier Python
```bash
# Créer un nouveau fichier
nano mon_premier_detecteur.py
```

### Code de base à copier :
```python
#!/usr/bin/env python3
from gpiozero import InputDevice
import time

# Créer l'objet capteur
capteur = InputDevice(17)

print("Détecteur de flamme démarré!")
print("Approchez une flamme pour tester...")
print("Ctrl+C pour arrêter")

try:
    while True:
        if not capteur.is_active:  # Flamme détectée
            print("🔥 FLAMME DÉTECTÉE!")
        else:
            print("Surveillance en cours...")
        
        time.sleep(1)  # Attendre 1 seconde
        
except KeyboardInterrupt:
    print("Arrêt du programme")

capteur.close()
print("Programme terminé")
```

### Exécuter votre programme :
```bash
python3 mon_premier_detecteur.py
```

## 🎯 Étape 4 : Programmes Plus Avancés

J'ai créé un fichier tutoriel complet avec 6 exemples progressifs :

### Télécharger le tutoriel :
```bash
# Télécharger le fichier tutoriel
wget https://raw.githubusercontent.com/votre-repo/flame_sensor_tutorial.py

# Ou créer le fichier et copier le contenu
nano flame_sensor_tutorial.py
```

### Exécuter le tutoriel :
```bash
python3 flame_sensor_tutorial.py
```

### Les 6 exemples inclus :
1. **Lecture simple** - Test basique du capteur
2. **Surveillance continue** - Monitoring pendant 30 secondes
3. **Compteur de détections** - Compter les flammes détectées
4. **Avec son** - Ajouter des bips d'alerte
5. **Sauvegarde fichier** - Enregistrer les détections
6. **Classe complète** - Code réutilisable et professionnel

## 🔧 Environnements de Développement

### Option 1 : Thonny (Recommandé pour débuter)
- Interface graphique simple
- Débogueur intégré
- Coloration syntaxique
- Menu → Programmation → Thonny Python IDE

### Option 2 : Terminal + nano
- Léger et rapide
- Parfait pour petits programmes
- `nano nom_fichier.py`

### Option 3 : VS Code (Avancé)
```bash
# Installer VS Code
sudo apt update
sudo apt install code
```

## 📚 Concepts Python Importants

### Bibliothèques essentielles :
```python
from gpiozero import InputDevice  # Pour le capteur
import time                       # Pour les pauses
from datetime import datetime     # Pour les timestamps
```

### Structure de base :
```python
# 1. Imports
from gpiozero import InputDevice

# 2. Configuration
capteur = InputDevice(17)

# 3. Boucle principale
try:
    while True:
        # Votre code ici
        pass
except KeyboardInterrupt:
    print("Arrêt")

# 4. Nettoyage
capteur.close()
```

## 🎯 Projets Suggérés (Progression)

### Niveau Débutant
1. ✅ Détecteur simple (fait)
2. Compteur avec affichage
3. Alarme avec LED

### Niveau Intermédiaire  
4. Sauvegarde avec horodatage
5. Interface web simple
6. Notifications email

### Niveau Avancé
7. Base de données SQLite
8. Graphiques en temps réel
9. Application mobile

## 🔍 Dépannage Courant

### Erreur "Permission denied"
```bash
sudo usermod -a -G gpio $USER
# Puis redémarrer
```

### Erreur "Module not found"
```bash
sudo apt install python3-gpiozero
```

### Capteur ne répond pas
- Vérifier les connexions
- Tester avec une flamme de briquet
- Ajuster le potentiomètre sur le capteur

## 📖 Ressources d'Apprentissage

### Documentation officielle :
- [GPIO Zero Documentation](https://gpiozero.readthedocs.io/)
- [Raspberry Pi GPIO Pinout](https://pinout.xyz/)

### Tutoriels Python :
- [Python.org Tutorial](https://docs.python.org/3/tutorial/)
- [Real Python](https://realpython.com/)

## 🎉 Prochaines Étapes

1. **Testez** le programme de base
2. **Explorez** les 6 exemples du tutoriel
3. **Modifiez** le code selon vos besoins
4. **Créez** votre propre projet personnalisé

**Prêt à commencer ? Lancez votre premier programme !** 🚀

