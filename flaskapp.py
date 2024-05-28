from flask import Flask, request, jsonify
import requests
import logging

app = Flask(__name__)

# Update Jenkins URL to reflect the new port
jenkins_url = "http://localhost:8080/job/demo/build?token=py"
auth = ("admin", "11f0fcc01bfdfc3124cb213e30d523a8d0")

# Setup basic logging
logging.basicConfig(level=logging.INFO)

@app.route('/jira-webhook', methods=['POST'])
def handle_jira_webhook():
    # Process the webhook payload here
    payload = request.json
    logging.info("Received webhook:", payload)
    
    # Example logic: Trigger Jenkins job if an issue key is present in the payload
    try:
        if 'key' in payload['issue']:
            # Trigger Jenkins job
            response = requests.post(
                jenkins_url, auth=auth,
                headers={'Content-Type': 'application/json'}
            )
            
            logging.info(f'Response from Jenkins: {response.text}')
            return jsonify({'status': 'success', 'message': f'Jenkins job triggered with status {response.status_code}'}), 200
        else:
            return jsonify({'status': 'ignored', 'message': 'No action taken'}), 200
    except Exception as e:
        logging.error(f"An error occurred while triggering Jenkins: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Failed to trigger Jenkins job'}), 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
