from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("Received alert:", data)

    # Scale only if alert is "firing"
    if data and any(a['status'] == 'firing' for a in data.get("alerts", [])):
        # Count current running backend containers
        output = subprocess.check_output(
            ["docker", "ps", "--filter", "name=backend", "--format", "{{.Names}}"]
        )
        running = len(output.decode().splitlines())
        new_count = running + 1

        print(f"Scaling backend to {new_count} replicas")
        subprocess.run(["docker", "compose", "up", "--scale", f"backend={new_count}", "-d", "-f ../docker-compose.yml"])
        return "Scaled up", 200

    return "No action taken", 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)