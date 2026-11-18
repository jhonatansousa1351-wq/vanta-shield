from flask import Flask, request, jsonify
import random, string, os

app = Flask(__name__)

@app.route('/api/get_identity', methods=['GET'])
def get_identity():
    fake_id = ''.join(random.choices(string.hexdigits.upper(), k=32))
    fake_mac = "02:%02X:%02X:%02X:%02X:%02X" % tuple(random.randint(0,255) for _ in range(5))
    fake_imei = "86" + str(random.randint(100000000, 999999999))
    return jsonify({"device_id": fake_id, "mac": fake_mac, "imei": fake_imei}), 200

@app.route('/api/report', methods=['POST'])
def report():
    data = request.json
    packet = str(data.get("packet", "")).lower()
    bad = ["report", "ban", "security", "tlog", "cheat", "hack"]
    if any(k in packet for k in bad):
        return jsonify({"action": "drop"}), 200
    return jsonify({"action": "allow"}), 200

@app.route('/api/heartbeat', methods=['GET'])
def heartbeat():
    return jsonify({"status": "alive"}), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
