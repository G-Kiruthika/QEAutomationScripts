# utils/send_email_report.py

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import yaml
import os
from datetime import datetime

def send_report(subject=None, body=None, attachment_path=None):
    """
    Send email report with test results
    
    Args:
        subject (str): Email subject. If None, uses default
        body (str): Email body content
        attachment_path (str): Path to attachment file
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        # Load configuration
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
        with open(config_path) as f:
            config = yaml.safe_load(f)
        
        # Check if email reporting is enabled
        if not config.get('reporting', {}).get('email_enabled', False):
            print("Email reporting is disabled in configuration")
            return False
        
        # Email configuration (should be in environment variables or secure config)
        smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.getenv('SMTP_PORT', '587'))
        sender_email = os.getenv('SENDER_EMAIL', 'automation@example.com')
        sender_password = os.getenv('SENDER_PASSWORD', '')
        
        recipients = config.get('reporting', {}).get('email_recipients', [])
        
        if not recipients:
            print("No email recipients configured")
            return False
        
        # Create message
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = ', '.join(recipients)
        
        # Set subject
        if subject is None:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            subject = f"Test Automation Report - {timestamp}"
        message['Subject'] = subject
        
        # Set body
        if body is None:
            body = "Please find the test automation report attached."
        message.attach(MIMEText(body, 'plain'))
        
        # Attach file if provided
        if attachment_path and os.path.exists(attachment_path):
            with open(attachment_path, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                filename = os.path.basename(attachment_path)
                part.add_header('Content-Disposition', f'attachment; filename= {filename}')
                message.attach(part)
        
        # Send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            if sender_password:
                server.login(sender_email, sender_password)
            server.send_message(message)
        
        print(f"Email report sent successfully to {', '.join(recipients)}")
        return True
    
    except Exception as e:
        print(f"Failed to send email report: {str(e)}")
        return False

def send_failure_alert(test_name, error_message):
    """
    Send immediate alert for test failure
    
    Args:
        test_name (str): Name of failed test
        error_message (str): Error message or stack trace
    
    Returns:
        bool: True if alert sent successfully, False otherwise
    """
    subject = f"⚠️ Test Failure Alert: {test_name}"
    body = f"""
    Test Failure Detected
    
    Test Name: {test_name}
    Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    
    Error Details:
    {error_message}
    
    Please investigate immediately.
    """
    
    return send_report(subject=subject, body=body)

def send_summary_report(total_tests, passed, failed, skipped, duration, report_path=None):
    """
    Send test execution summary report
    
    Args:
        total_tests (int): Total number of tests
        passed (int): Number of passed tests
        failed (int): Number of failed tests
        skipped (int): Number of skipped tests
        duration (float): Total execution duration in seconds
        report_path (str): Path to detailed report file
    
    Returns:
        bool: True if report sent successfully, False otherwise
    """
    pass_rate = (passed / total_tests * 100) if total_tests > 0 else 0
    
    subject = f"Test Execution Summary - {datetime.now().strftime('%Y-%m-%d')}"
    body = f"""
    Test Automation Execution Summary
    
    Execution Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    Duration: {duration:.2f} seconds
    
    Results:
    --------
    Total Tests: {total_tests}
    Passed: {passed} ✓
    Failed: {failed} ✗
    Skipped: {skipped} ⊘
    Pass Rate: {pass_rate:.2f}%
    
    {'Status: SUCCESS ✓' if failed == 0 else 'Status: FAILURE ✗'}
    
    Please review the detailed report attached.
    """
    
    return send_report(subject=subject, body=body, attachment_path=report_path)
