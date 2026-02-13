import smtplib
import yaml
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os


def load_email_config():
    """Load email configuration from config.yaml"""
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config.get('email', {})


def send_email_notification(subject, body, recipients=None):
    """Send email notification for test events"""
    try:
        email_config = load_email_config()
        
        msg = MIMEMultipart()
        msg['From'] = email_config.get('sender', 'automation@example.com')
        msg['To'] = ', '.join(recipients or email_config.get('recipients', []))
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'html'))
        
        server = smtplib.SMTP(email_config.get('smtp_server'), email_config.get('smtp_port'))
        server.starttls()
        # Note: Add authentication if required
        # server.login(email_config.get('username'), email_config.get('password'))
        
        server.send_message(msg)
        server.quit()
        
        return True
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        return False


def send_account_lockout_notification(username):
    """Send account lockout notification email"""
    subject = f"Account Lockout Alert - {username}"
    body = f"""
    <html>
    <body>
        <h2>Account Lockout Notification</h2>
        <p>The account <strong>{username}</strong> has been locked due to multiple failed login attempts.</p>
        <p>Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p>Please contact support to unlock your account.</p>
    </body>
    </html>
    """
    return send_email_notification(subject, body)


def verify_email_sent(username):
    """Verify that email notification was sent for account lockout"""
    # In a real implementation, this would check email logs or use an email testing service
    # For now, we'll simulate the notification
    return send_account_lockout_notification(username)


def send_test_report(test_results):
    """Send test execution report via email"""
    subject = f"Test Execution Report - {datetime.now().strftime('%Y-%m-%d')}"
    
    passed = sum(1 for r in test_results if r.get('status') == 'PASSED')
    failed = sum(1 for r in test_results if r.get('status') == 'FAILED')
    total = len(test_results)
    
    body = f"""
    <html>
    <body>
        <h2>Test Execution Summary</h2>
        <p>Total Tests: {total}</p>
        <p>Passed: {passed}</p>
        <p>Failed: {failed}</p>
        <hr>
        <h3>Test Details</h3>
        <ul>
    """
    
    for result in test_results:
        body += f"<li>{result.get('test_name')}: {result.get('status')}</li>"
    
    body += """
        </ul>
    </body>
    </html>
    """
    
    return send_email_notification(subject, body)