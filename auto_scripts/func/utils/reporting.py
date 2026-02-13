import json
import os
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class TestReporter:
    """Test reporting utility for generating test execution reports"""
    
    def __init__(self, report_dir="reports"):
        """Initialize test reporter
        
        Args:
            report_dir: Directory to store test reports
        """
        self.report_dir = report_dir
        self.test_results = []
        self.start_time = None
        self.end_time = None
        
        # Create report directory if it doesn't exist
        if not os.path.exists(report_dir):
            os.makedirs(report_dir)
    
    def start_test_suite(self):
        """Mark the start of test suite execution"""
        self.start_time = datetime.now()
        logger.info(f"Test suite started at {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    def end_test_suite(self):
        """Mark the end of test suite execution"""
        self.end_time = datetime.now()
        logger.info(f"Test suite ended at {self.end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    def add_test_result(self, test_name, status, duration, error_message=None, screenshot_path=None):
        """Add a test result to the report
        
        Args:
            test_name: Name of the test
            status: Test status (PASSED, FAILED, SKIPPED)
            duration: Test execution duration in seconds
            error_message: Error message if test failed
            screenshot_path: Path to screenshot if captured
        """
        result = {
            "test_name": test_name,
            "status": status,
            "duration": duration,
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        if error_message:
            result["error_message"] = error_message
        
        if screenshot_path:
            result["screenshot"] = screenshot_path
        
        self.test_results.append(result)
        logger.info(f"Test result added: {test_name} - {status}")
    
    def generate_json_report(self):
        """Generate JSON report of test execution
        
        Returns:
            str: Path to the generated JSON report
        """
        report_data = {
            "start_time": self.start_time.strftime('%Y-%m-%d %H:%M:%S') if self.start_time else None,
            "end_time": self.end_time.strftime('%Y-%m-%d %H:%M:%S') if self.end_time else None,
            "total_duration": str(self.end_time - self.start_time) if self.start_time and self.end_time else None,
            "summary": self._generate_summary(),
            "test_results": self.test_results
        }
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_path = os.path.join(self.report_dir, f"test_report_{timestamp}.json")
        
        with open(report_path, 'w') as f:
            json.dump(report_data, f, indent=4)
        
        logger.info(f"JSON report generated: {report_path}")
        return report_path
    
    def generate_html_report(self):
        """Generate HTML report of test execution
        
        Returns:
            str: Path to the generated HTML report
        """
        summary = self._generate_summary()
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Test Execution Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ color: #333; }}
                table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
                th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
                th {{ background-color: #4CAF50; color: white; }}
                tr:nth-child(even) {{ background-color: #f2f2f2; }}
                .passed {{ color: green; font-weight: bold; }}
                .failed {{ color: red; font-weight: bold; }}
                .skipped {{ color: orange; font-weight: bold; }}
                .summary {{ background-color: #e7f3fe; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
            </style>
        </head>
        <body>
            <h1>Test Execution Report</h1>
            <div class="summary">
                <h2>Summary</h2>
                <p><strong>Start Time:</strong> {self.start_time.strftime('%Y-%m-%d %H:%M:%S') if self.start_time else 'N/A'}</p>
                <p><strong>End Time:</strong> {self.end_time.strftime('%Y-%m-%d %H:%M:%S') if self.end_time else 'N/A'}</p>
                <p><strong>Total Duration:</strong> {str(self.end_time - self.start_time) if self.start_time and self.end_time else 'N/A'}</p>
                <p><strong>Total Tests:</strong> {summary['total']}</p>
                <p class="passed"><strong>Passed:</strong> {summary['passed']}</p>
                <p class="failed"><strong>Failed:</strong> {summary['failed']}</p>
                <p class="skipped"><strong>Skipped:</strong> {summary['skipped']}</p>
            </div>
            
            <h2>Test Results</h2>
            <table>
                <tr>
                    <th>Test Name</th>
                    <th>Status</th>
                    <th>Duration (s)</th>
                    <th>Timestamp</th>
                    <th>Error Message</th>
                </tr>
        """
        
        for result in self.test_results:
            status_class = result['status'].lower()
            error_msg = result.get('error_message', 'N/A')
            html_content += f"""
                <tr>
                    <td>{result['test_name']}</td>
                    <td class="{status_class}">{result['status']}</td>
                    <td>{result['duration']:.2f}</td>
                    <td>{result['timestamp']}</td>
                    <td>{error_msg}</td>
                </tr>
            """
        
        html_content += """
            </table>
        </body>
        </html>
        """
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_path = os.path.join(self.report_dir, f"test_report_{timestamp}.html")
        
        with open(report_path, 'w') as f:
            f.write(html_content)
        
        logger.info(f"HTML report generated: {report_path}")
        return report_path
    
    def _generate_summary(self):
        """Generate summary statistics of test execution
        
        Returns:
            dict: Summary statistics
        """
        total = len(self.test_results)
        passed = sum(1 for r in self.test_results if r['status'] == 'PASSED')
        failed = sum(1 for r in self.test_results if r['status'] == 'FAILED')
        skipped = sum(1 for r in self.test_results if r['status'] == 'SKIPPED')
        
        return {
            "total": total,
            "passed": passed,
            "failed": failed,
            "skipped": skipped
        }