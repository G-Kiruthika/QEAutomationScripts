import smtplib
import yaml
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

def send_email_report(test_results, config_path=None):
    """
    Send email report with test results
    Args:
        test_results: Dictionary containing test execution results
        config_path: Optional path to config file
    """
    if not config_path:
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
    
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    
    reporting_config = config.get('reporting', {})
    
    if not reporting_config.get('email_enabled', False):
        print("Email reporting is disabled")
        return
    
    # Email configuration (should be in environment variables in production)
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "qa-automation@example.com"
    sender_password = "your-app-password"  # Use app password for Gmail
    
    recipients = reporting_config.get('email_recipients', [])
    
    # Create message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = ", ".join(recipients)
    message["Subject"] = f"Test Execution Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    # Create email body
    body = f"""
    Test Execution Report
    =====================
    
    Execution Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    
    Test Results:
    - Total Tests: {test_results.get('total', 0)}
    - Passed: {test_results.get('passed', 0)}
    - Failed: {test_results.get('failed', 0)}
    - Skipped: {test_results.get('skipped', 0)}
    
    Success Rate: {(test_results.get('passed', 0) / max(test_results.get('total', 1), 1)) * 100:.2f}%
    
    Failed Tests:
    {chr(10).join(test_results.get('failed_tests', []))}
    
    Best regards,
    QA Automation Team
    """
    
    message.attach(MIMEText(body, "plain"))
    
    try:
        # Create SMTP session
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Enable security
        server.login(sender_email, sender_password)
        
        # Send email
        text = message.as_string()
        server.sendmail(sender_email, recipients, text)
        server.quit()
        
        print(f"Email report sent successfully to {recipients}")
        
    except Exception as e:
        print(f"Error sending email report: {str(e)}")