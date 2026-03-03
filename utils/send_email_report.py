import smtplib
import yaml
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_report(message, subject=None, recipients=None):
    """Send email report with test results or error messages"""
    try:
        # Load configuration
        with open('config/config.yaml') as f:
            config = yaml.safe_load(f)
        
        if not config.get('reporting', {}).get('email_enabled', False):
            logger.info("Email reporting is disabled")
            return
        
        # Email configuration
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = "automation@example.com"
        sender_password = "app_password"  # Use app password for Gmail
        
        # Recipients
        if recipients is None:
            recipients = config.get('reporting', {}).get('email_recipients', [])
        
        if not recipients:
            logger.warning("No email recipients configured")
            return
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = ", ".join(recipients)
        msg['Subject'] = subject or f"Test Automation Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        # Email body
        body = f"""
        Test Automation Report
        =====================
        
        Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        Environment: {config.get('environment', 'Unknown')}
        
        Message:
        {message}
        
        ---
        This is an automated message from the QA Automation Framework.
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, recipients, text)
        server.quit()
        
        logger.info(f"Email report sent successfully to {recipients}")
        
    except Exception as e:
        logger.error(f"Failed to send email report: {str(e)}")

def send_test_summary(passed, failed, skipped, total_time):
    """Send test execution summary report"""
    summary_message = f"""
    Test Execution Summary
    =====================
    
    Total Tests: {passed + failed + skipped}
    Passed: {passed}
    Failed: {failed}
    Skipped: {skipped}
    Execution Time: {total_time:.2f} seconds
    
    Success Rate: {(passed / (passed + failed) * 100):.1f}%
    """
    
    subject = f"Test Summary - {passed}P/{failed}F/{skipped}S"
    send_report(summary_message, subject)

def send_failure_report(test_name, error_message, screenshot_path=None):
    """Send detailed failure report for a specific test"""
    failure_message = f"""
    Test Failure Report
    ==================
    
    Test Name: {test_name}
    Failure Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    
    Error Details:
    {error_message}
    
    Screenshot: {screenshot_path or 'Not available'}
    
    Please investigate this failure and take appropriate action.
    """
    
    subject = f"Test Failure Alert - {test_name}"
    send_report(failure_message, subject)