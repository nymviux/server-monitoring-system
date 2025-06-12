from flask import Flask, request
import subprocess
import os

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("Received alert:", data)

    # Check if Grafana alert is in 'alerting' state
    if data and data.get("state") == "alerting":
        # Count currently running metric_collector containers
        output = subprocess.check_output(
            ["docker", "ps", "--filter", "name=metric_collector", "--format", "{{.Names}}"]
        )
        running = len(output.decode().splitlines())
        new_count = running + 1

        env = os.environ.copy()
        env["SERVER_ID"] = str(new_count)

        print(f"Scaling metric_collector to {new_count} replicas")
        subprocess.run([
            "docker", "compose", "--file", "../metric_collector/docker-compose.yml",
            "up", "--scale", f"metric_collector={new_count}", "-d"
        ], env=env)
        return "Scaled up", 200

    return "No action taken", 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)
