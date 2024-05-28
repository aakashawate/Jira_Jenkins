from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Update Jenkins URL to reflect the new port
jenkins_url = "http://localhost:8080/job/demo/build?token=py"
auth = ("admin", "11f0fcc01bfdfc3124cb213e30d523a8d0")

@app.route('/jira-webhook', methods=['POST'])
def handle_jira_webhook():
    # Process the webhook payload here
    payload = request.json
    print("Received webhook:", payload)
    
    # Example logic: Trigger Jenkins job if an issue key is present in the payload
    if 'key' in payload['issue']:
        # Trigger Jenkins job
        response = requests.post(
            jenkins_url, auth=auth,
            headers={'Content-Type': 'application/json'}
        )
        
        return jsonify({'status': 'success', 'message': f'Jenkins job triggered with status {response.status_code}'}), 200
    else:
        return jsonify({'status': 'ignored', 'message': 'No action taken'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='192.168.0.104', port=5000)  # Change debug to False for production
