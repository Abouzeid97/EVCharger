# 🚀 OCPP Backend with Django & WebSockets

This project implements an **OCPP (Open Charge Point Protocol) backend** using **Django, Django Channels, and WebSockets**. It allows communication between **EV chargers (simulated or real)** and a central system.

## 📌 Features
- ✅ WebSocket-based communication with EV chargers.
- ✅ Supports **OCPP 1.6** messages (e.g., BootNotification, Heartbeat).
- ✅ Django Channels for handling WebSocket connections.
- ✅ Simulator for testing charge point interactions.

## 🛠️ Installation & Setup

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO](https://github.com/Abouzeid97/EVCharger.git
```
### **2️⃣ Set Up a Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
### **3️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```
### **4️⃣ Apply Migrations**
```bash
python manage.py migrate
```
### **5️⃣ Start Django Server**
```bash
python manage.py runserver
```
### **6️⃣ Run the OCPP Simulator**
```bash
python ocpp_simulator.py
```
### **⚡ WebSocket Endpoint**
Your chargers should connect to:
```bash
ws://localhost:8000/ws/ocpp/{charger_id}/
```
where {charger_id} is a unique identifier for each charger.

