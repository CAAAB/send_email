from flask import Flask, request, render_template_string
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import requests

smtp_username = os.environ.get('SMTP_USERNAME')
smtp_password = os.environ.get('SMTP_PASSWORD')

def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org')
        if response.status_code == 200:
            return response.text
        else:
            return "Could not determine public IP"
    except requests.RequestException as e:
        return f"Error occurred: {e}"

public_ip = get_public_ip()
print(f"Public IP Address: {public_ip}")



app = Flask(__name__)

@app.route('/')
def index():
    return '''
        <form method="POST" action="/send-email">
            Subject: <input type="text" name="subject"><br>
            Body: <textarea name="body"></textarea><br>
            Recipient: <input type="email" name="recipient"><br>
            From Name: <input type="text" name="from_name"><br>
            From Email: <input type="email" name="from_email"><br>
            <input type="submit" value="Send Email">
        </form>
    '''

@app.route('/send-email', methods=['POST'])
def send_email():
    subject = request.form['subject']
    body = request.form['body']
    recipient = request.form['recipient']
    from_name = request.form['from_name']
    from_email = request.form['from_email']

    # SMTP settings
    smtp_server = "smtp-relay.brevo.com"
    smtp_port = 587

    # Create MIMEMultipart object
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = f"{from_name} <{from_email}>"
    msg['To'] = recipient

    # Attach the message body
    msg.attach(MIMEText(body, 'plain'))

    # Send the email
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(smtp_username, smtp_password)
            server.sendmail(from_email, recipient, msg.as_string())
        return "Email sent successfully"
    except Exception as e:
        return f"Error sending email: {e}"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
