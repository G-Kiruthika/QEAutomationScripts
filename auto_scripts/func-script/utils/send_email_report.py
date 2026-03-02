import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import yaml
import logging
from datetime import datetime


class EmailReporter:
    """Email reporting utility for test automation results"""
    
    def __init__(self):
        self.config = self._load_config()
        self.logger = logging.getLogger(__name__)
    
    def _load_config(self):
        """Load email configuration from config.yaml"""
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)
    
    def send_test_report(self, subject, body, attachments=None, recipients=None):
        """Send test report via email"""
        try:
            # Email configuration
            smtp_server = self.config['email']['smtp_server']
            smtp_port = self.config['email']['smtp_port']
            sender_email = self.config['email']['sender_email']
            sender_password = self.config['email']['sender_password']
            
            # Recipients
            if recipients is None:
                recipients = self.config['email']['recipients']
            
            # Create message
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = ", ".join(recipients)
            message["Subject"] = subject
            
            # Add body to email
            message.attach(MIMEText(body, "html"))
            
            # Add attachments if provided
            if attachments:
                for attachment_path in attachments:
                    if os.path.isfile(attachment_path):
                        self._attach_file(message, attachment_path)
            
            # Create secure connection and send email
            context = ssl.create_default_context()
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls(context=context)
                server.login(sender_email, sender_password)
                text = message.as_string()
                server.sendmail(sender_email, recipients, text)
            
            self.logger.info(f"Email sent successfully to {recipients}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send email: {str(e)}")
            return False
    
    def _attach_file(self, message, file_path):
        """Attach file to email message"""
        try:
            with open(file_path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
            
            encoders.encode_base64(part)
            
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= {os.path.basename(file_path)}'
            )
            
            message.attach(part)
            
        except Exception as e:
            self.logger.error(f"Failed to attach file {file_path}: {str(e)}")
    
    def generate_test_summary_html(self, test_results):
        """Generate HTML summary of test results"""
        total_tests = len(test_results)
        passed_tests = sum(1 for result in test_results if result['status'] == 'PASSED')
        failed_tests = sum(1 for result in test_results if result['status'] == 'FAILED')
        skipped_tests = sum(1 for result in test_results if result['status'] == 'SKIPPED')
        
        pass_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        html_template = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background-color: #f0f0f0; padding: 20px; border-radius: 5px; }}
                .summary {{ margin: 20px 0; }}
                .test-results {{ margin: 20px 0; }}
                .passed {{ color: green; }}
                .failed {{ color: red; }}
                .skipped {{ color: orange; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Test Automation Report</h1>
                <p>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
            
            <div class="summary">
                <h2>Test Summary</h2>
                <p><strong>Total Tests:</strong> {total_tests}</p>
                <p><strong class="passed">Passed:</strong> {passed_tests}</p>
                <p><strong class="failed">Failed:</strong> {failed_tests}</p>
                <p><strong class="skipped">Skipped:</strong> {skipped_tests}</p>
                <p><strong>Pass Rate:</strong> {pass_rate:.2f}%</p>
            </div>
            
            <div class="test-results">
                <h2>Test Results</h2>
                <table>
                    <tr>
                        <th>Test Name</th>
                        <th>Status</th>
                        <th>Duration</th>
                        <th>Error Message</th>
                    </tr>
        """
        
        for result in test_results:
            status_class = result['status'].lower()
            error_msg = result.get('error_message', '')
            duration = result.get('duration', 'N/A')
            
            html_template += f"""
                    <tr>
                        <td>{result['test_name']}</td>
                        <td class="{status_class}">{result['status']}</td>
                        <td>{duration}</td>
                        <td>{error_msg}</td>
                    </tr>
            """
        
        html_template += """
                </table>
            </div>
        </body>
        </html>
        """
        
        return html_template


# Convenience function for quick email sending
def send_report(message, subject="Test Automation Alert", recipients=None):
    """Quick function to send a simple text report"""
    try:
        email_reporter = EmailReporter()
        
        # Create simple HTML body
        html_body = f"""
        <html>
        <body>
            <h2>Test Automation Alert</h2>
            <p><strong>Timestamp:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p><strong>Message:</strong></p>
            <pre>{message}</pre>
        </body>
        </html>
        """
        
        return email_reporter.send_test_report(subject, html_body, recipients=recipients)
        
    except Exception as e:
        logging.error(f"Failed to send quick report: {str(e)}")
        return False


def send_test_completion_report(test_results, attachments=None):
    """Send comprehensive test completion report"""
    try:
        email_reporter = EmailReporter()
        
        # Generate subject based on results
        total_tests = len(test_results)
        failed_tests = sum(1 for result in test_results if result['status'] == 'FAILED')
        
        if failed_tests == 0:
            subject = f"✅ All Tests Passed - {total_tests} tests completed successfully"
        else:
            subject = f"❌ Test Failures Detected - {failed_tests}/{total_tests} tests failed"
        
        # Generate HTML report
        html_body = email_reporter.generate_test_summary_html(test_results)
        
        return email_reporter.send_test_report(subject, html_body, attachments)
        
    except Exception as e:
        logging.error(f"Failed to send test completion report: {str(e)}")
        return False