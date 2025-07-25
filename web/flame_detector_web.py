#!/usr/bin/env python3
"""
Détecteur de Flamme Raspberry Pi - Version Web
==============================================

Application avec interface web pour surveillance à distance:
- Interface web responsive
- API REST
- Historique des détections
- Surveillance en temps réel
- Configuration via interface web

Auteur: Assistant IA
Date: Juillet 2025
"""

import time
import json
import threading
from datetime import datetime, timedelta
from pathlib import Path
from flask import Flask, render_template_string, jsonify, request
from collections import deque

try:
    from gpiozero import InputDevice
except ImportError:
    print("Mode simulation activé (gpiozero non disponible)")
    InputDevice = None

class FlameDetectorWeb:
    """Détecteur de flamme avec interface web."""
    
    def __init__(self):
        """Initialise le détecteur web."""
        self.flame_sensor = None
        self.running = False
        self.flame_detected = False
        self.detection_count = 0
        self.detection_history = deque(maxlen=100)  # Garde les 100 dernières détections
        self.status_log = deque(maxlen=50)  # Log des statuts
        self.gpio_pin = 17
        self.check_interval = 0.5
        
        # Simulation mode si pas de GPIO
        self.simulation_mode = InputDevice is None
        
        # Thread de surveillance
        self.monitor_thread = None
        
    def _log_status(self, message, level="INFO"):
        """Ajoute un message au log de statut."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.status_log.append({
            "timestamp": timestamp,
            "level": level,
            "message": message
        })
        print(f"[{timestamp}] {level}: {message}")
        
    def initialize(self):
        """Initialise le capteur."""
        try:
            if not self.simulation_mode:
                self.flame_sensor = InputDevice(self.gpio_pin)
                self._log_status(f"Capteur initialisé sur GPIO{self.gpio_pin}")
            else:
                self._log_status("Mode simulation activé", "WARNING")
            return True
        except Exception as e:
            self._log_status(f"Erreur d'initialisation: {e}", "ERROR")
            return False
            
    def check_flame(self):
        """Vérifie la présence d'une flamme."""
        if self.simulation_mode:
            # Simulation: flamme détectée aléatoirement
            import random
            return random.random() < 0.01  # 1% de chance de détecter une flamme
            
        if not self.flame_sensor:
            return False
            
        return not self.flame_sensor.is_active
        
    def _monitoring_loop(self):
        """Boucle de surveillance en arrière-plan."""
        self._log_status("Démarrage de la surveillance")
        
        while self.running:
            try:
                current_flame_state = self.check_flame()
                
                if current_flame_state != self.flame_detected:
                    self.flame_detected = current_flame_state
                    
                    if self.flame_detected:
                        self.detection_count += 1
                        detection_data = {
                            "timestamp": datetime.now().isoformat(),
                            "detection_id": self.detection_count,
                            "status": "FLAME_DETECTED"
                        }
                        self.detection_history.append(detection_data)
                        self._log_status(f"🔥 FLAMME DÉTECTÉE! (#{self.detection_count})", "WARNING")
                    else:
                        self._log_status("✅ Flamme éteinte")
                        
                time.sleep(self.check_interval)
                
            except Exception as e:
                self._log_status(f"Erreur de surveillance: {e}", "ERROR")
                time.sleep(1)
                
        self._log_status("Surveillance arrêtée")
        
    def start_monitoring(self):
        """Démarre la surveillance."""
        if not self.initialize():
            return False
            
        self.running = True
        self.monitor_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitor_thread.start()
        return True
        
    def stop_monitoring(self):
        """Arrête la surveillance."""
        self.running = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2)
        if self.flame_sensor:
            self.flame_sensor.close()
        self._log_status("Surveillance arrêtée")
        
    def get_status(self):
        """Retourne le statut actuel."""
        return {
            "running": self.running,
            "flame_detected": self.flame_detected,
            "detection_count": self.detection_count,
            "simulation_mode": self.simulation_mode,
            "gpio_pin": self.gpio_pin,
            "check_interval": self.check_interval,
            "uptime": datetime.now().isoformat()
        }
        
    def get_detection_history(self, limit=20):
        """Retourne l'historique des détections."""
        return list(self.detection_history)[-limit:]
        
    def get_status_log(self, limit=20):
        """Retourne le log de statut."""
        return list(self.status_log)[-limit:]

# Instance globale du détecteur
detector = FlameDetectorWeb()

# Application Flask
app = Flask(__name__)

# Template HTML pour l'interface web
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Détecteur de Flamme Raspberry Pi</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container { 
            max-width: 1200px; 
            margin: 0 auto; 
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            overflow: hidden;
        }
        .header { 
            background: linear-gradient(45deg, #ff6b6b, #ee5a24);
            color: white; 
            padding: 30px;
            text-align: center;
        }
        .header h1 { font-size: 2.5em; margin-bottom: 10px; }
        .header p { font-size: 1.2em; opacity: 0.9; }
        .content { padding: 30px; }
        .status-card {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 25px;
            margin-bottom: 25px;
            border-left: 5px solid #007bff;
        }
        .status-card.flame-detected { border-left-color: #dc3545; background: #fff5f5; }
        .status-card.running { border-left-color: #28a745; background: #f0fff4; }
        .status-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-box {
            background: white;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .stat-number { font-size: 2.5em; font-weight: bold; color: #007bff; }
        .stat-label { color: #666; margin-top: 5px; }
        .controls {
            display: flex;
            gap: 15px;
            margin-bottom: 30px;
            flex-wrap: wrap;
        }
        .btn {
            padding: 12px 25px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 600;
            transition: all 0.3s;
        }
        .btn-primary { background: #007bff; color: white; }
        .btn-success { background: #28a745; color: white; }
        .btn-danger { background: #dc3545; color: white; }
        .btn:hover { transform: translateY(-2px); box-shadow: 0 4px 15px rgba(0,0,0,0.2); }
        .log-section {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .log-section h3 { margin-bottom: 15px; color: #333; }
        .log-entry {
            background: white;
            padding: 10px 15px;
            margin-bottom: 8px;
            border-radius: 5px;
            border-left: 3px solid #007bff;
            font-family: monospace;
            font-size: 14px;
        }
        .log-entry.WARNING { border-left-color: #ffc107; }
        .log-entry.ERROR { border-left-color: #dc3545; }
        .flame-indicator {
            display: inline-block;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            margin-right: 10px;
            background: #28a745;
        }
        .flame-indicator.detected { background: #dc3545; animation: pulse 1s infinite; }
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }
        .footer {
            background: #343a40;
            color: white;
            text-align: center;
            padding: 20px;
        }
        @media (max-width: 768px) {
            .header h1 { font-size: 2em; }
            .controls { justify-content: center; }
            .stat-number { font-size: 2em; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔥 Détecteur de Flamme</h1>
            <p>Surveillance Raspberry Pi en Temps Réel</p>
        </div>
        
        <div class="content">
            <div id="status-card" class="status-card">
                <h2><span class="flame-indicator" id="flame-indicator"></span>Statut: <span id="status-text">Chargement...</span></h2>
                <p id="status-details"></p>
            </div>
            
            <div class="status-grid">
                <div class="stat-box">
                    <div class="stat-number" id="detection-count">0</div>
                    <div class="stat-label">Détections Totales</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number" id="gpio-pin">17</div>
                    <div class="stat-label">Pin GPIO</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number" id="check-interval">0.5</div>
                    <div class="stat-label">Intervalle (s)</div>
                </div>
            </div>
            
            <div class="controls">
                <button class="btn btn-success" onclick="startMonitoring()">▶️ Démarrer</button>
                <button class="btn btn-danger" onclick="stopMonitoring()">⏹️ Arrêter</button>
                <button class="btn btn-primary" onclick="refreshData()">🔄 Actualiser</button>
            </div>
            
            <div class="log-section">
                <h3>📊 Historique des Détections</h3>
                <div id="detection-history"></div>
            </div>
            
            <div class="log-section">
                <h3>📝 Journal des Événements</h3>
                <div id="status-log"></div>
            </div>
        </div>
        
        <div class="footer">
            <p>Détecteur de Flamme Raspberry Pi - Version Web | Développé avec ❤️</p>
        </div>
    </div>

    <script>
        let refreshInterval;
        
        function updateStatus() {
            fetch('/api/status')
                .then(response => response.json())
                .then(data => {
                    const statusCard = document.getElementById('status-card');
                    const statusText = document.getElementById('status-text');
                    const statusDetails = document.getElementById('status-details');
                    const flameIndicator = document.getElementById('flame-indicator');
                    
                    if (data.flame_detected) {
                        statusCard.className = 'status-card flame-detected';
                        statusText.textContent = 'FLAMME DÉTECTÉE!';
                        flameIndicator.className = 'flame-indicator detected';
                    } else if (data.running) {
                        statusCard.className = 'status-card running';
                        statusText.textContent = 'Surveillance Active';
                        flameIndicator.className = 'flame-indicator';
                    } else {
                        statusCard.className = 'status-card';
                        statusText.textContent = 'Arrêté';
                        flameIndicator.className = 'flame-indicator';
                    }
                    
                    statusDetails.textContent = data.simulation_mode ? 
                        'Mode simulation activé' : 
                        `GPIO${data.gpio_pin} - Intervalle: ${data.check_interval}s`;
                    
                    document.getElementById('detection-count').textContent = data.detection_count;
                    document.getElementById('gpio-pin').textContent = data.gpio_pin;
                    document.getElementById('check-interval').textContent = data.check_interval;
                })
                .catch(error => console.error('Erreur:', error));
        }
        
        function updateHistory() {
            fetch('/api/history')
                .then(response => response.json())
                .then(data => {
                    const historyDiv = document.getElementById('detection-history');
                    if (data.length === 0) {
                        historyDiv.innerHTML = '<p>Aucune détection enregistrée</p>';
                    } else {
                        historyDiv.innerHTML = data.slice(-10).reverse().map(detection => 
                            `<div class="log-entry WARNING">
                                🔥 Détection #${detection.detection_id} - ${new Date(detection.timestamp).toLocaleString()}
                            </div>`
                        ).join('');
                    }
                })
                .catch(error => console.error('Erreur:', error));
        }
        
        function updateLog() {
            fetch('/api/log')
                .then(response => response.json())
                .then(data => {
                    const logDiv = document.getElementById('status-log');
                    if (data.length === 0) {
                        logDiv.innerHTML = '<p>Aucun événement enregistré</p>';
                    } else {
                        logDiv.innerHTML = data.slice(-10).reverse().map(entry => 
                            `<div class="log-entry ${entry.level}">
                                [${entry.timestamp}] ${entry.level}: ${entry.message}
                            </div>`
                        ).join('');
                    }
                })
                .catch(error => console.error('Erreur:', error));
        }
        
        function refreshData() {
            updateStatus();
            updateHistory();
            updateLog();
        }
        
        function startMonitoring() {
            fetch('/api/start', { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        setTimeout(refreshData, 500);
                    }
                })
                .catch(error => console.error('Erreur:', error));
        }
        
        function stopMonitoring() {
            fetch('/api/stop', { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        setTimeout(refreshData, 500);
                    }
                })
                .catch(error => console.error('Erreur:', error));
        }
        
        // Actualisation automatique toutes les 2 secondes
        refreshInterval = setInterval(refreshData, 2000);
        
        // Chargement initial
        refreshData();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Page d'accueil avec interface web."""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/status')
def api_status():
    """API: Retourne le statut actuel."""
    return jsonify(detector.get_status())

@app.route('/api/history')
def api_history():
    """API: Retourne l'historique des détections."""
    return jsonify(detector.get_detection_history())

@app.route('/api/log')
def api_log():
    """API: Retourne le journal des événements."""
    return jsonify(detector.get_status_log())

@app.route('/api/start', methods=['POST'])
def api_start():
    """API: Démarre la surveillance."""
    try:
        success = detector.start_monitoring()
        return jsonify({"success": success})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/stop', methods=['POST'])
def api_stop():
    """API: Arrête la surveillance."""
    try:
        detector.stop_monitoring()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

def main():
    """Fonction principale."""
    print("=" * 60)
    print("    DÉTECTEUR DE FLAMME RASPBERRY PI - VERSION WEB")
    print("=" * 60)
    print()
    print("Interface web disponible sur:")
    print("  - Local: http://localhost:5000")
    print("  - Réseau: http://[IP_RASPBERRY_PI]:5000")
    print()
    print("Appuyez sur Ctrl+C pour arrêter")
    print("-" * 60)
    
    try:
        app.run(host='0.0.0.0', port=5000, debug=False)
    except KeyboardInterrupt:
        print("\nArrêt du serveur web...")
    finally:
        detector.stop_monitoring()

if __name__ == "__main__":
    main()

