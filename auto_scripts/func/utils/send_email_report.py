# utils/send_email_report.py

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import yaml
import os
from datetime import datetime


def send_report(report_content, subject=None, attachment_path=None):
    """
    Send an email report with optional attachment.
    
    Args:
        report_content (str): Content of the email report
        subject (str): Email subject (optional, uses config default if not provided)
        attachment_path (str): Path to attachment file (optional)
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        # Load email configuration
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
        with open(config_path) as f:
            config = yaml.safe_load(f)
        
        email_config = config.get('email', {})
        
        smtp_server = email_config.get('smtp_server', 'smtp.gmail.com')
        smtp_port = email_config.get('smtp_port', 587)
        sender_email = email_config.get('sender_email')
        sender_password = email_config.get('sender_password')
        recipient_emails = email_config.get('recipient_emails', [])
        default_subject = email_config.get('subject', 'Automation Test Report')
        
        if not sender_email or not sender_password:
            print("Email credentials not configured in config.yaml")
            return False
        
        if not recipient_emails:
            print("No recipient emails configured in config.yaml")
            return False
        
        # Create message
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = ', '.join(recipient_emails)
        message['Subject'] = subject or f"{default_subject} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        # Add body
        body = f"""
        <html>
            <body>
                <h2>Automation Test Report</h2>
                <p><strong>Execution Time:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <hr>
                <pre>{report_content}</pre>
            </body>
        </html>
        """
        message.attach(MIMEText(body, 'html'))
        
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
                message.attach(part)
        
        # Send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)
        
        print(f"Email report sent successfully to {', '.join(recipient_emails)}")
        return True
    
    except Exception as e:
        print(f"Failed to send email report: {str(e)}")
        return False


def send_test_summary(passed, failed, skipped, total_time, details=None):
    """
    Send a formatted test execution summary report.
    
    Args:
        passed (int): Number of passed tests
        failed (int): Number of failed tests
        skipped (int): Number of skipped tests
        total_time (float): Total execution time in seconds
        details (str): Additional details about test execution
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    total_tests = passed + failed + skipped
    pass_rate = (passed / total_tests * 100) if total_tests > 0 else 0
    
    summary = f"""
    TEST EXECUTION SUMMARY
    =====================
    
    Total Tests: {total_tests}
    Passed: {passed}
    Failed: {failed}
    Skipped: {skipped}
    Pass Rate: {pass_rate:.2f}%
    
    Total Execution Time: {total_time:.2f} seconds
    
    """
    
    if details:
        summary += f"\n\nDETAILS:\n{details}"
    
    return send_report(
        report_content=summary,
        subject=f"Test Execution Summary - {passed}/{total_tests} Passed"
    )


def send_error_notification(error_message, test_name=None):
    """
    Send an error notification email.
    
    Args:
        error_message (str): Error message to send
        test_name (str): Name of the test that failed (optional)
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    subject = "Test Execution Error"
    if test_name:
        subject += f" - {test_name}"
    
    content = f"""
    TEST EXECUTION ERROR
    ===================
    
    Test: {test_name or 'Unknown'}
    Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    
    Error Message:
    {error_message}
    """
    
    return send_report(report_content=content, subject=subject)
