import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
import yaml
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_email_config():
    """Load email configuration from config.yaml.
    
    Returns:
        dict: Email configuration settings
    """
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config.get('email', {})
    except FileNotFoundError:
        logger.warning("Config file not found, using default email settings")
        return {}

def send_report(message, subject=None, recipients=None, attachment_path=None):
    """Send email report with test results.
    
    Args:
        message (str): Email message content
        subject (str): Email subject line
        recipients (list): List of recipient email addresses
        attachment_path (str): Path to attachment file
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        # Load configuration
        email_config = load_email_config()
        
        # Default values
        smtp_server = email_config.get('smtp_server', 'smtp.gmail.com')
        smtp_port = email_config.get('smtp_port', 587)
        sender_email = email_config.get('sender_email', os.getenv('SENDER_EMAIL'))
        sender_password = email_config.get('sender_password', os.getenv('SENDER_PASSWORD'))
        default_recipients = email_config.get('recipients', [])
        
        # Use provided recipients or default
        recipients = recipients or default_recipients
        if not recipients:
            logger.warning("No recipients specified, email not sent")
            return False
        
        # Default subject
        if not subject:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            subject = f"Test Automation Report - {timestamp}"
        
        # Validate required settings
        if not sender_email or not sender_password:
            logger.error("Sender email or password not configured")
            return False
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = ', '.join(recipients)
        msg['Subject'] = subject
        
        # Add message body
        body = f"""
        Test Automation Report
        
        Timestamp: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        
        Message:
        {message}
        
        ---
        This is an automated message from the Test Automation Framework.
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Add attachment if provided
        if attachment_path and os.path.exists(attachment_path):
            with open(attachment_path, "rb") as attachment:
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
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, recipients, text)
        server.quit()
        
        logger.info(f"Email sent successfully to {recipients}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")
        return False

def send_test_failure_report(test_name, error_message, stack_trace=None):
    """Send specific test failure report.
    
    Args:
        test_name (str): Name of the failed test
        error_message (str): Error message from the test
        stack_trace (str): Stack trace of the error
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    subject = f"Test Failure Alert: {test_name}"
    
    message = f"""
    Test Failure Details:
    
    Test Name: {test_name}
    Error Message: {error_message}
    
    """
    
    if stack_trace:
        message += f"""
    Stack Trace:
    {stack_trace}
    """
    
    return send_report(message, subject)

def send_test_summary_report(total_tests, passed_tests, failed_tests, test_results=None):
    """Send test execution summary report.
    
    Args:
        total_tests (int): Total number of tests executed
        passed_tests (int): Number of tests that passed
        failed_tests (int): Number of tests that failed
        test_results (list): Detailed test results
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    subject = f"Test Execution Summary - {passed_tests}/{total_tests} Passed"
    
    message = f"""
    Test Execution Summary:
    
    Total Tests: {total_tests}
    Passed: {passed_tests}
    Failed: {failed_tests}
    Success Rate: {(passed_tests/total_tests)*100:.1f}%
    
    """
    
    if test_results:
        message += "\nDetailed Results:\n"
        for result in test_results:
            status = "PASS" if result.get('passed', False) else "FAIL"
            message += f"- {result.get('name', 'Unknown')}: {status}\n"
            if not result.get('passed', False) and result.get('error'):
                message += f"  Error: {result.get('error')}\n"
    
    return send_report(message, subject)