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
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
            return config.get('reporting', {})
    except FileNotFoundError:
        return {
            'email_enabled': False,
            'email_recipients': [],
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587
        }

def send_report(subject, body, attachment_path=None, recipients=None):
    """
    Send email report with optional attachment
    
    Args:
        subject (str): Email subject
        body (str): Email body content
        attachment_path (str): Path to attachment file (optional)
        recipients (list): List of recipient email addresses (optional, uses config if None)
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    email_config = load_email_config()
    
    # Check if email is enabled
    if not email_config.get('email_enabled', False):
        print("Email reporting is disabled in configuration")
        return False
    
    # Get recipients
    to_addresses = recipients or email_config.get('email_recipients', [])
    if not to_addresses:
        print("No recipients configured for email reporting")
        return False
    
    # Email configuration
    smtp_server = email_config.get('smtp_server', 'smtp.gmail.com')
    smtp_port = email_config.get('smtp_port', 587)
    from_address = email_config.get('from_address', 'automation@example.com')
    password = email_config.get('password', '')
    
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = from_address
        msg['To'] = ', '.join(to_addresses)
        msg['Subject'] = f"{subject} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        # Add body
        msg.attach(MIMEText(body, 'html'))
        
        # Add attachment if provided
        if attachment_path and os.path.exists(attachment_path):
            with open(attachment_path, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename= {os.path.basename(attachment_path)}'
                )
                msg.attach(part)
        
        # Send email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        
        # Only login if password is provided
        if password:
            server.login(from_address, password)
        
        server.send_message(msg)
        server.quit()
        
        print(f"Email report sent successfully to {', '.join(to_addresses)}")
        return True
    
    except Exception as e:
        print(f"Failed to send email report: {str(e)}")
        return False

def send_test_failure_report(test_name, error_message, screenshot_path=None):
    """
    Send test failure notification email
    
    Args:
        test_name (str): Name of the failed test
        error_message (str): Error message or stack trace
        screenshot_path (str): Path to failure screenshot (optional)
    
    Returns:
        bool: True if email sent successfully, False otherwise
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
            <p>Please investigate the failure and take necessary action.</p>
        </body>
    </html>
    """
    
    return send_report(subject, body, screenshot_path)

def send_test_summary_report(total_tests, passed, failed, skipped, duration, report_path=None):
    """
    Send test execution summary report
    
    Args:
        total_tests (int): Total number of tests executed
        passed (int): Number of passed tests
        failed (int): Number of failed tests
        skipped (int): Number of skipped tests
        duration (float): Total execution duration in seconds
        report_path (str): Path to detailed HTML report (optional)
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    subject = "Automation Test Execution Summary"
    
    pass_rate = (passed / total_tests * 100) if total_tests > 0 else 0
    status_color = "green" if failed == 0 else "red"
    
    body = f"""
    <html>
        <body>
            <h2 style="color: {status_color};">Test Execution Summary</h2>
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
            <p>For detailed results, please check the attached report.</p>
        </body>
    </html>
    """
    
    return send_report(subject, body, report_path)
