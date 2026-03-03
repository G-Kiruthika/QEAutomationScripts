import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import yaml
from datetime import datetime


def send_email_report(test_results=None, report_path=None, recipients=None):
    """Send email report with test results
    
    Args:
        test_results (dict): Test execution results
        report_path (str): Path to HTML/JSON report file
        recipients (list): List of email recipients
    """
    
    # Load email configuration
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        email_config = config.get('email', {})
    except FileNotFoundError:
        print("Email configuration not found. Skipping email notification.")
        return
    
    # Email configuration
    smtp_server = email_config.get('smtp_server', 'smtp.gmail.com')
    smtp_port = email_config.get('smtp_port', 587)
    sender_email = email_config.get('sender_email')
    sender_password = email_config.get('sender_password')
    
    if not sender_email or not sender_password:
        print("Email credentials not configured. Skipping email notification.")
        return
    
    if not recipients:
        recipients = email_config.get('recipients', [])
    
    if not recipients:
        print("No email recipients configured. Skipping email notification.")
        return
    
    # Create message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ', '.join(recipients)
    msg['Subject'] = f"Test Automation Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    # Email body
    if test_results:
        body = f"""
        Test Execution Summary:
        
        Total Tests: {test_results.get('total', 0)}
        Passed: {test_results.get('passed', 0)}
        Failed: {test_results.get('failed', 0)}
        Skipped: {test_results.get('skipped', 0)}
        
        Execution Time: {test_results.get('duration', 'N/A')}
        
        Please find the detailed report attached.
        
        Best regards,
        QA Automation Team
        """
    else:
        body = """
        Test Automation Report
        
        Please find the test execution report attached.
        
        Best regards,
        QA Automation Team
        """
    
    msg.attach(MIMEText(body, 'plain'))
    
    # Attach report file if provided
    if report_path and os.path.exists(report_path):
        with open(report_path, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
        
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename= {os.path.basename(report_path)}'
        )
        msg.attach(part)
    
    # Send email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, recipients, text)
        server.quit()
        print(f"Email report sent successfully to: {', '.join(recipients)}")
    except Exception as e:
        print(f"Failed to send email report: {str(e)}")


def format_test_results(pytest_results):
    """Format pytest results for email reporting
    
    Args:
        pytest_results: Pytest execution results
        
    Returns:
        dict: Formatted test results
    """
    return {
        'total': pytest_results.get('total', 0),
        'passed': pytest_results.get('passed', 0),
        'failed': pytest_results.get('failed', 0),
        'skipped': pytest_results.get('skipped', 0),
        'duration': pytest_results.get('duration', 'N/A')
    }