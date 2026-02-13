# Email reporting utility for automation framework
# Sends test execution reports via email

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import yaml
from datetime import datetime


def load_config():
    """Load configuration from config.yaml"""
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def send_report(subject=None, body=None, attachments=None, recipients=None):
    """Send email report
    
    Args:
        subject (str): Email subject
        body (str): Email body content
        attachments (list): List of file paths to attach
        recipients (list): List of recipient email addresses
    
    Returns:
        bool: True if sent successfully, False otherwise
    """
    config = load_config()
    
    if not config['reporting'].get('email_enabled', False):
        print("Email reporting is disabled in configuration")
        return False
    
    if recipients is None:
        recipients = config['reporting'].get('email_recipients', [])
    
    if not recipients:
        print("No recipients configured")
        return False
    
    if subject is None:
        subject = f"Automation Test Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    if body is None:
        body = "Please find the attached test execution report."
    
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = config['reporting'].get('email_from', 'automation@example.com')
        msg['To'] = ', '.join(recipients)
        msg['Subject'] = subject
        
        # Add body
        msg.attach(MIMEText(body, 'plain'))
        
        # Add attachments
        if attachments:
            for file_path in attachments:
                if os.path.exists(file_path):
                    with open(file_path, 'rb') as f:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(f.read())
                        encoders.encode_base64(part)
                        part.add_header(
                            'Content-Disposition',
                            f'attachment; filename={os.path.basename(file_path)}'
                        )
                        msg.attach(part)
        
        # Send email
        smtp_server = config['reporting'].get('smtp_server', 'smtp.gmail.com')
        smtp_port = config['reporting'].get('smtp_port', 587)
        smtp_username = config['reporting'].get('smtp_username', '')
        smtp_password = config['reporting'].get('smtp_password', '')
        
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        
        if smtp_username and smtp_password:
            server.login(smtp_username, smtp_password)
        
        server.send_message(msg)
        server.quit()
        
        print(f"Report sent successfully to {', '.join(recipients)}")
        return True
    
    except Exception as e:
        print(f"Failed to send email report: {str(e)}")
        return False


def send_failure_notification(test_name, error_message):
    """Send failure notification email
    
    Args:
        test_name (str): Name of failed test
        error_message (str): Error message
    
    Returns:
        bool: True if sent successfully, False otherwise
    """
    subject = f"Test Failure Alert: {test_name}"
    body = f"""Test Failure Notification
    
Test Name: {test_name}
Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Error Details:
{error_message}

Please investigate and take necessary action.
    """
    
    return send_report(subject=subject, body=body)
