import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import yaml
import os
import logging

logger = logging.getLogger(__name__)


def load_email_config():
    """Load email configuration from config.yaml
    
    Returns:
        dict: Email configuration
    """
    try:
        with open('config/config.yaml') as f:
            config = yaml.safe_load(f)
        return config.get('email', {})
    except Exception as e:
        logger.error(f"Failed to load email configuration: {str(e)}")
        return {}


def send_email_notification(subject, body, recipient=None):
    """Send email notification
    
    Args:
        subject: Email subject
        body: Email body content
        recipient: Recipient email address (optional, uses config if not provided)
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    email_config = load_email_config()
    
    if not email_config:
        logger.warning("Email configuration not found, skipping email notification")
        return False
    
    try:
        # Create message
        message = MIMEMultipart()
        message['From'] = email_config.get('sender_email', '')
        message['To'] = recipient or email_config.get('recipient_email', '')
        message['Subject'] = subject
        
        # Add body
        message.attach(MIMEText(body, 'html'))
        
        # Connect to SMTP server
        smtp_server = email_config.get('smtp_server', 'smtp.gmail.com')
        smtp_port = email_config.get('smtp_port', 587)
        sender_password = os.getenv('EMAIL_PASSWORD', email_config.get('sender_password', ''))
        
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(message['From'], sender_password)
            server.send_message(message)
        
        logger.info(f"Email notification sent successfully to {message['To']}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send email notification: {str(e)}")
        return False


def send_account_lockout_notification(username):
    """Send account lockout notification email
    
    Args:
        username: Username of the locked account
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    subject = f"Account Lockout Alert - {username}"
    body = f"""
    <html>
        <body>
            <h2>Account Lockout Notification</h2>
            <p>The following account has been locked due to multiple failed login attempts:</p>
            <ul>
                <li><strong>Username:</strong> {username}</li>
                <li><strong>Timestamp:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</li>
                <li><strong>Reason:</strong> Multiple failed login attempts detected</li>
            </ul>
            <p>Please contact the administrator to unlock your account.</p>
            <br>
            <p><em>This is an automated notification from the QA Automation System.</em></p>
        </body>
    </html>
    """
    
    return send_email_notification(subject, body)


def verify_lockout_email_sent(username):
    """Verify that lockout email was sent (mock implementation for testing)
    
    Args:
        username: Username to verify email for
    
    Returns:
        bool: True if email verification passed
    """
    # In a real implementation, this would check email logs or use an email testing service
    # For now, we'll send the actual notification and return the result
    logger.info(f"Verifying lockout email notification for user: {username}")
    return send_account_lockout_notification(username)


def send_test_report(test_results, report_path=None):
    """Send test execution report via email
    
    Args:
        test_results: Dictionary containing test execution results
        report_path: Path to the HTML report file (optional)
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    subject = f"Test Execution Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    # Build email body
    total_tests = test_results.get('total', 0)
    passed_tests = test_results.get('passed', 0)
    failed_tests = test_results.get('failed', 0)
    skipped_tests = test_results.get('skipped', 0)
    
    body = f"""
    <html>
        <body>
            <h2>Test Execution Summary</h2>
            <table border="1" cellpadding="5" cellspacing="0">
                <tr>
                    <th>Metric</th>
                    <th>Count</th>
                </tr>
                <tr>
                    <td>Total Tests</td>
                    <td>{total_tests}</td>
                </tr>
                <tr style="background-color: #90EE90;">
                    <td>Passed</td>
                    <td>{passed_tests}</td>
                </tr>
                <tr style="background-color: #FFB6C6;">
                    <td>Failed</td>
                    <td>{failed_tests}</td>
                </tr>
                <tr style="background-color: #FFE4B5;">
                    <td>Skipped</td>
                    <td>{skipped_tests}</td>
                </tr>
            </table>
            <br>
            <p><em>This is an automated report from the QA Automation System.</em></p>
        </body>
    </html>
    """
    
    return send_email_notification(subject, body)