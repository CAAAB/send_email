from flask import Flask, request, render_template_string
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import requests

smtp_username = os.environ.get('SMTP_USERNAME')
smtp_password = os.environ.get('SMTP_PASSWORD')

simple_form = """<!DOCTYPE html>
<html>
<head>
    <title>Email Form</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background-color: #f4f4f4;
        }
        form {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        input[type=text], input[type=email], textarea {
            width: 100%;
            padding: 8px;
            margin: 8px 0;
            display: inline-block;
            border: 1px solid #ccc;
            border-radius: 4px;
            box-sizing: border-box;
        }
        input[type=submit] {
            width: 100%;
            background-color: #4CAF50;
            color: white;
            padding: 14px 20px;
            margin: 8px 0;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        input[type=submit]:hover {
            background-color: #45a049;
        }
        label {
            margin-top: 10px;
            display: block;
        }
    </style>
</head>
<body>

    <form method="POST" action="/send-email">
        <label for="from_name">From Name:</label>
        <input type="text" id="from_name" name="from_name">
        
        <label for="from_email">From Email:</label>
        <input type="email" id="from_email" name="from_email">
        
        <label for="subject">Subject:</label>
        <input type="text" id="subject" name="subject">
        
        <label for="body">Body:</label>
        <textarea id="body" name="body"></textarea>
        
        <label for="recipient">Recipient:</label>
        <input type="email" id="recipient" name="recipient">
        
        <input type="submit" value="Send Email">
    </form>

</body>
</html>
"""

better_form = """
<!DOCTYPE html>
<html>
<head>
    <title>Email Form</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background-color: #f4f4f4;
        }
        form {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        input[type=text], input[type=email], textarea {
            width: 100%;
            padding: 8px;
            margin: 8px 0;
            display: inline-block;
            border: 1px solid #ccc;
            border-radius: 4px;
            box-sizing: border-box;
        }
        input[type=submit] {
            width: 100%;
            background-color: #4CAF50;
            color: white;
            padding: 14px 20px;
            margin: 8px 0;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        input[type=submit]:hover {
            background-color: #45a049;
        }
        label {
            margin-top: 10px;
            display: block;
        }
    </style>
</head>
<body>

    <form method="POST" action="/send-email">
        <label for="from_name">From Name:</label>
        <input type="text" id="from_name" name="from_name">
        
        <label for="from_email">From Email:</label>
        <input type="email" id="from_email" name="from_email">
        
        <label for="subject">Subject:</label>
        <input type="text" id="subject" name="subject">
        
        <label for="body">Body:</label>
        <textarea id="body" name="body"></textarea>
        
        <label for="recipient">Recipient:</label>
        <input type="email" id="recipient" name="recipient">
        
        <input type="submit" value="Send Email">
    </form>

</body>
</html>
"""
form = better_form

app = Flask(__name__)

@app.route('/')
def index():
    return form

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
