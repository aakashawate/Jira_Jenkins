from flask import Flask, request, jsonify
import requests
import logging
import os

app = Flask(__name__)

# Environment variables for configuration
jenkins_url = os.getenv("JENKINS_URL", "http://localhost:8080/job/demo/build?token=py")
jenkins_user = os.getenv("JENKINS_USER", "admin")
jenkins_token = os.getenv("JENKINS_TOKEN", "11f0fcc01bfdfc3124cb213e30d523a8d0")

# Setup basic logging
logging.basicConfig(level=logging.INFO)

# Create a session for HTTP requests
session = requests.Session()
session.auth = (jenkins_user, jenkins_token)

@app.route('/jira-webhook', methods=['POST'])
def handle_jira_webhook():
    try:
        payload = request.get_json()
        if not payload:
            logging.error("Invalid JSON payload")
            return jsonify({'status': 'error', 'message': 'Invalid JSON payload'}), 400
        
        logging.info("Received webhook payload")
        
        # Example logic: Trigger Jenkins job if an issue key is present in the payload
        issue_key = payload.get('issue', {}).get('key')
        if issue_key:
            # Trigger Jenkins job
            response = session.post(
                jenkins_url,
                headers={'Content-Type': 'application/json'}
            )
            
            logging.info(f'Response from Jenkins: {response.text}')
            return jsonify({'status': 'success', 'message': f'Jenkins job triggered with status {response.status_code}'}), 200
        else:
            logging.info("No issue key found in payload, no action taken")
            return jsonify({'status': 'ignored', 'message': 'No action taken'}), 200
    except requests.exceptions.RequestException as e:
        logging.error(f"Network error occurred while triggering Jenkins: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Failed to trigger Jenkins job due to network error'}), 500
    except Exception as e:
        logging.error(f"An error occurred while processing the webhook: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Failed to process webhook'}), 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)