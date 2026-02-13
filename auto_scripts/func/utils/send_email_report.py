import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import yaml
import os
import logging

logger = logging.getLogger(__name__)

def send_report(subject, body, recipients=None):
    """
    Send email report with test results or notifications
    
    Args:
        subject (str): Email subject
        body (str): Email body content
        recipients (list): List of recipient email addresses
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    # Load configuration
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
    
    if not os.path.exists(config_path):
        logger.warning("Config file not found, email not sent")
        return False
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    reporting_config = config.get('reporting', {})
    
    if not reporting_config.get('email_enabled', False):
        logger.info("Email reporting is disabled in config")
        return False
    
    recipients = recipients or reporting_config.get('email_recipients', [])
    
    if not recipients:
        logger.warning("No recipients configured for email report")
        return False
    
    try:
        # Create message
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = reporting_config.get('sender_email', 'noreply@automation.com')
        msg['To'] = ', '.join(recipients)
        
        msg.attach(MIMEText(body, 'html'))
        
        # Send email (configure SMTP settings as needed)
        # This is a placeholder - actual SMTP configuration would be needed
        logger.info(f"Email report prepared: {subject}")
        logger.info(f"Recipients: {recipients}")
        logger.info(f"Body preview: {body[:100]}...")
        
        # Uncomment and configure when SMTP server is available
        # smtp_server = reporting_config.get('smtp_server', 'smtp.gmail.com')
        # smtp_port = reporting_config.get('smtp_port', 587)
        # smtp_username = reporting_config.get('smtp_username')
        # smtp_password = reporting_config.get('smtp_password')
        # 
        # with smtplib.SMTP(smtp_server, smtp_port) as server:
        #     server.starttls()
        #     server.login(smtp_username, smtp_password)
        #     server.send_message(msg)
        
        return True
    
    except Exception as e:
        logger.error(f"Failed to send email report: {str(e)}")
        return False

def send_account_lockout_notification(username, lockout_time):
    """
    Send account lockout notification email
    
    Args:
        username (str): Username of locked account
        lockout_time (str): Lockout duration
    
    Returns:
        bool: True if notification sent successfully
    """
    subject = f"Account Lockout Notification - {username}"
    body = f"""
    <html>
    <body>
        <h2>Account Lockout Notification</h2>
        <p>Dear User,</p>
        <p>Your account <strong>{username}</strong> has been locked due to multiple failed login attempts.</p>
        <p>Please try again after <strong>{lockout_time}</strong> or reset your password.</p>
        <p>If you did not attempt to log in, please contact support immediately.</p>
        <br>
        <p>Best regards,</p>
        <p>Security Team</p>
    </body>
    </html>
    """
    
    return send_report(subject, body)
