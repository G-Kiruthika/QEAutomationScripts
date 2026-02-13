import os
import json
from datetime import datetime
from typing import Dict, List, Any

class TestReport:
    """Test reporting utility for generating and managing test reports"""
    
    def __init__(self, report_dir="reports"):
        self.report_dir = report_dir
        self.test_results = []
        self.start_time = None
        self.end_time = None
        
        # Create reports directory if it doesn't exist
        if not os.path.exists(self.report_dir):
            os.makedirs(self.report_dir)
    
    def start_test_run(self):
        """Mark the start of test execution"""
        self.start_time = datetime.now()
        self.test_results = []
    
    def end_test_run(self):
        """Mark the end of test execution"""
        self.end_time = datetime.now()
    
    def add_test_result(self, test_name: str, status: str, duration: float, error_message: str = None):
        """Add a test result to the report"""
        result = {
            "test_name": test_name,
            "status": status,
            "duration": duration,
            "timestamp": datetime.now().isoformat()
        }
        if error_message:
            result["error_message"] = error_message
        
        self.test_results.append(result)
    
    def generate_json_report(self, filename: str = None) -> str:
        """Generate JSON report of test results"""
        if filename is None:
            filename = f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        report_data = {
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "total_tests": len(self.test_results),
            "passed": len([r for r in self.test_results if r["status"] == "passed"]),
            "failed": len([r for r in self.test_results if r["status"] == "failed"]),
            "skipped": len([r for r in self.test_results if r["status"] == "skipped"]),
            "test_results": self.test_results
        }
        
        report_path = os.path.join(self.report_dir, filename)
        with open(report_path, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        return report_path
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary of test results"""
        return {
            "total": len(self.test_results),
            "passed": len([r for r in self.test_results if r["status"] == "passed"]),
            "failed": len([r for r in self.test_results if r["status"] == "failed"]),
            "skipped": len([r for r in self.test_results if r["status"] == "skipped"])
        }

def generate_html_report(json_report_path: str) -> str:
    """Generate HTML report from JSON report"""
    with open(json_report_path, 'r') as f:
        report_data = json.load(f)
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            h1 {{ color: #333; }}
            .summary {{ background: #f0f0f0; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
            .passed {{ color: green; }}
            .failed {{ color: red; }}
            .skipped {{ color: orange; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #4CAF50; color: white; }}
        </style>
    </head>
    <body>
        <h1>Test Execution Report</h1>
        <div class="summary">
            <h2>Summary</h2>
            <p>Total Tests: {report_data['total_tests']}</p>
            <p class="passed">Passed: {report_data['passed']}</p>
            <p class="failed">Failed: {report_data['failed']}</p>
            <p class="skipped">Skipped: {report_data['skipped']}</p>
            <p>Start Time: {report_data['start_time']}</p>
            <p>End Time: {report_data['end_time']}</p>
        </div>
        <h2>Test Results</h2>
        <table>
            <tr>
                <th>Test Name</th>
                <th>Status</th>
                <th>Duration (s)</th>
                <th>Timestamp</th>
            </tr>
    """
    
    for result in report_data['test_results']:
        status_class = result['status']
        html_content += f"""
            <tr>
                <td>{result['test_name']}</td>
                <td class="{status_class}">{result['status']}</td>
                <td>{result['duration']:.2f}</td>
                <td>{result['timestamp']}</td>
            </tr>
        """
    
    html_content += """
        </table>
    </body>
    </html>
    """
    
    html_report_path = json_report_path.replace('.json', '.html')
    with open(html_report_path, 'w') as f:
        f.write(html_content)
    
    return html_report_path
