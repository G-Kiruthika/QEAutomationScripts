import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import yaml
import os
from datetime import datetime


def load_email_config():
    """Load email configuration from config.yaml"""
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config.get('email', {})


def send_report(subject, body, attachments=None, recipients=None):
    """Send email report with optional attachments
    
    Args:
        subject (str): Email subject
        body (str): Email body content
        attachments (list): List of file paths to attach (optional)
        recipients (list): List of recipient email addresses (optional, uses config if None)
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        config = load_email_config()
        
        smtp_server = config.get('smtp_server', 'smtp.gmail.com')
        smtp_port = config.get('smtp_port', 587)
        sender_email = config.get('sender_email')
        sender_password = config.get('sender_password', '')
        
        if recipients is None:
            receiver_email = config.get('receiver_email')
            recipients = [receiver_email] if isinstance(receiver_email, str) else receiver_email
        
        # Create message
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = ', '.join(recipients)
        message['Subject'] = subject
        message['Date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Add body
        message.attach(MIMEText(body, 'html'))
        
        # Add attachments if provided
        if attachments:
            for filepath in attachments:
                if os.path.exists(filepath):
                    with open(filepath, 'rb') as file:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(file.read())
                        encoders.encode_base64(part)
                        part.add_header(
                            'Content-Disposition',
                            f'attachment; filename={os.path.basename(filepath)}'
                        )
                        message.attach(part)
        
        # Send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            if sender_password:
                server.login(sender_email, sender_password)
            server.send_message(message)
        
        print(f"Email sent successfully to {', '.join(recipients)}")
        return True
    
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        return False


def send_test_failure_notification(test_name, error_message, screenshot_path=None):
    """Send notification for test failure
    
    Args:
        test_name (str): Name of the failed test
        error_message (str): Error message or stack trace
        screenshot_path (str): Path to failure screenshot (optional)
    
    Returns:
        bool: True if notification sent successfully, False otherwise
    """
    subject = f"Test Failure Alert: {test_name}"
    
    body = f"""
    <html>
        <body>
            <h2 style="color: red;">Test Failure Notification</h2>
            <p><strong>Test Name:</strong> {test_name}</p>
            <p><strong>Timestamp:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p><strong>Error Details:</strong></p>
            <pre style="background-color: #f4f4f4; padding: 10px; border-radius: 5px;">{error_message}</pre>
            <p>Please investigate and take necessary action.</p>
        </body>
    </html>
    """
    
    attachments = [screenshot_path] if screenshot_path and os.path.exists(screenshot_path) else None
    
    return send_report(subject, body, attachments)


def send_test_suite_summary(total_tests, passed, failed, skipped, duration, report_path=None):
    """Send test suite execution summary
    
    Args:
        total_tests (int): Total number of tests
        passed (int): Number of passed tests
        failed (int): Number of failed tests
        skipped (int): Number of skipped tests
        duration (float): Execution duration in seconds
        report_path (str): Path to detailed HTML report (optional)
    
    Returns:
        bool: True if summary sent successfully, False otherwise
    """
    pass_rate = (passed / total_tests * 100) if total_tests > 0 else 0
    status_color = 'green' if failed == 0 else 'red'
    
    subject = f"Test Execution Summary - {'PASSED' if failed == 0 else 'FAILED'}"
    
    body = f"""
    <html>
        <body>
            <h2 style="color: {status_color};">Test Suite Execution Summary</h2>
            <p><strong>Execution Date:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <table style="border-collapse: collapse; width: 50%;">
                <tr style="background-color: #f2f2f2;">
                    <th style="border: 1px solid #ddd; padding: 8px; text-align: left;">Metric</th>
                    <th style="border: 1px solid #ddd; padding: 8px; text-align: left;">Value</th>
                </tr>
                <tr>
                    <td style="border: 1px solid #ddd; padding: 8px;">Total Tests</td>
                    <td style="border: 1px solid #ddd; padding: 8px;">{total_tests}</td>
                </tr>
                <tr style="background-color: #d4edda;">
                    <td style="border: 1px solid #ddd; padding: 8px;">Passed</td>
                    <td style="border: 1px solid #ddd; padding: 8px;">{passed}</td>
                </tr>
                <tr style="background-color: #f8d7da;">
                    <td style="border: 1px solid #ddd; padding: 8px;">Failed</td>
                    <td style="border: 1px solid #ddd; padding: 8px;">{failed}</td>
                </tr>
                <tr style="background-color: #fff3cd;">
                    <td style="border: 1px solid #ddd; padding: 8px;">Skipped</td>
                    <td style="border: 1px solid #ddd; padding: 8px;">{skipped}</td>
                </tr>
                <tr>
                    <td style="border: 1px solid #ddd; padding: 8px;">Pass Rate</td>
                    <td style="border: 1px solid #ddd; padding: 8px;">{pass_rate:.2f}%</td>
                </tr>
                <tr>
                    <td style="border: 1px solid #ddd; padding: 8px;">Duration</td>
                    <td style="border: 1px solid #ddd; padding: 8px;">{duration:.2f} seconds</td>
                </tr>
            </table>
            <p>Detailed report is attached.</p>
        </body>
    </html>
    """
    
    attachments = [report_path] if report_path and os.path.exists(report_path) else None
    
    return send_report(subject, body, attachments)


def send_account_lockout_notification(username, ip_address=None):
    """Send notification for account lockout event
    
    Args:
        username (str): Username that was locked out
        ip_address (str): IP address of the lockout attempt (optional)
    
    Returns:
        bool: True if notification sent successfully, False otherwise
    """
    subject = f"Security Alert: Account Lockout - {username}"
    
    body = f"""
    <html>
        <body>
            <h2 style="color: orange;">Account Lockout Notification</h2>
            <p><strong>Username:</strong> {username}</p>
            <p><strong>Timestamp:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            {f'<p><strong>IP Address:</strong> {ip_address}</p>' if ip_address else ''}
            <p><strong>Reason:</strong> Multiple failed login attempts detected</p>
            <p>The account has been temporarily locked for security purposes.</p>
            <p>Please contact support to unlock the account or wait for the automatic unlock period.</p>
        </body>
    </html>
    """
    
    return send_report(subject, body)
