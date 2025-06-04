#!/usr/bin/env python3
"""
📄 PDF Report Generator
Converts the project report to PDF format
"""

import os
import sys
from datetime import datetime

def install_requirements():
    """Install required packages for PDF generation"""
    try:
        import markdown
        import pdfkit
        print("✅ Required packages already installed")
        return True
    except ImportError:
        print("📦 Installing required packages...")
        try:
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", "markdown", "pdfkit"])
            print("✅ Packages installed successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to install packages: {e}")
            print("💡 Please install manually: pip install markdown pdfkit")
            return False

def check_wkhtmltopdf():
    """Check if wkhtmltopdf is installed"""
    try:
        import subprocess
        result = subprocess.run(['wkhtmltopdf', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ wkhtmltopdf is installed")
            return True
        else:
            print("❌ wkhtmltopdf not found")
            return False
    except FileNotFoundError:
        print("❌ wkhtmltopdf not installed")
        print("💡 Please install wkhtmltopdf:")
        print("   Windows: Download from https://wkhtmltopdf.org/downloads.html")
        print("   Mac: brew install wkhtmltopdf")
        print("   Linux: sudo apt-get install wkhtmltopdf")
        return False

def markdown_to_html(markdown_file, html_file):
    """Convert markdown to HTML"""
    try:
        import markdown
        
        # Read markdown file
        with open(markdown_file, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        # Convert to HTML
        html = markdown.markdown(markdown_content, extensions=['tables', 'toc'])
        
        # Add CSS styling
        styled_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Weather Dashboard Project Report</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #34495e;
            border-bottom: 2px solid #ecf0f1;
            padding-bottom: 5px;
            margin-top: 30px;
        }}
        h3 {{
            color: #7f8c8d;
            margin-top: 25px;
        }}
        code {{
            background-color: #f8f9fa;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }}
        pre {{
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            border-left: 4px solid #3498db;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 15px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }}
        th {{
            background-color: #f2f2f2;
            font-weight: bold;
        }}
        .emoji {{
            font-size: 1.2em;
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 10px;
        }}
        .footer {{
            text-align: center;
            margin-top: 30px;
            padding: 15px;
            background-color: #f8f9fa;
            border-radius: 5px;
            font-size: 0.9em;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🌤️ Real-Time Weather Monitoring Dashboard</h1>
        <p>Complete Project Report</p>
        <p>Generated on {datetime.now().strftime('%B %d, %Y at %H:%M')}</p>
    </div>
    
    {html}
    
    <div class="footer">
        <p>📊 Project Report Generated Automatically</p>
        <p>🚀 Technologies: Apache Kafka, Elasticsearch, Docker, Python, JavaScript</p>
    </div>
</body>
</html>
"""
        
        # Save HTML file
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(styled_html)
        
        print(f"✅ HTML report generated: {html_file}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to convert markdown to HTML: {e}")
        return False

def html_to_pdf(html_file, pdf_file):
    """Convert HTML to PDF"""
    try:
        import pdfkit
        
        options = {
            'page-size': 'A4',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8",
            'no-outline': None,
            'enable-local-file-access': None
        }
        
        pdfkit.from_file(html_file, pdf_file, options=options)
        print(f"✅ PDF report generated: {pdf_file}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to convert HTML to PDF: {e}")
        return False

def create_simple_pdf_alternative():
    """Create a simple text-based PDF alternative"""
    print("📄 Creating alternative PDF using text formatting...")
    
    try:
        # Read the text report
        with open('PROJECT_REPORT.txt', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Create a formatted version
        formatted_content = f"""
REAL-TIME WEATHER MONITORING DASHBOARD
COMPLETE PROJECT REPORT

Generated on: {datetime.now().strftime('%B %d, %Y at %H:%M')}

{content}

---
Report generated automatically by the Weather Dashboard Project
Technologies: Apache Kafka, Elasticsearch, Docker, Python, JavaScript
"""
        
        # Save as formatted text
        with open('PROJECT_REPORT_FORMATTED.txt', 'w', encoding='utf-8') as f:
            f.write(formatted_content)
        
        print("✅ Formatted text report created: PROJECT_REPORT_FORMATTED.txt")
        print("💡 You can convert this to PDF using online tools or print to PDF")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create formatted report: {e}")
        return False

def main():
    """Main PDF generation function"""
    print("📄 Weather Dashboard Project - PDF Report Generator")
    print("=" * 60)
    
    # Check if markdown report exists
    if not os.path.exists('PROJECT_REPORT.md'):
        print("❌ PROJECT_REPORT.md not found!")
        print("💡 Please run this script from the project root directory")
        return
    
    # Method 1: Try full PDF generation
    print("\n🔄 Attempting full PDF generation...")
    
    if install_requirements() and check_wkhtmltopdf():
        print("🔄 Converting markdown to HTML...")
        if markdown_to_html('PROJECT_REPORT.md', 'PROJECT_REPORT.html'):
            print("🔄 Converting HTML to PDF...")
            if html_to_pdf('PROJECT_REPORT.html', 'PROJECT_REPORT.pdf'):
                print("\n🎉 SUCCESS! PDF report generated successfully!")
                print("📁 Files created:")
                print("   📄 PROJECT_REPORT.pdf (Main PDF report)")
                print("   🌐 PROJECT_REPORT.html (HTML version)")
                print("   📝 PROJECT_REPORT.md (Markdown source)")
                print("   📋 PROJECT_REPORT.txt (Text version)")
                return
    
    # Method 2: Create alternative formats
    print("\n🔄 Creating alternative formats...")
    
    if create_simple_pdf_alternative():
        print("\n📁 Available report formats:")
        print("   📝 PROJECT_REPORT.md (Markdown - best formatting)")
        print("   📋 PROJECT_REPORT.txt (Plain text)")
        print("   📋 PROJECT_REPORT_FORMATTED.txt (Formatted text)")
        
        print("\n💡 To create PDF:")
        print("   1. Open PROJECT_REPORT.md in any markdown viewer")
        print("   2. Print to PDF from the viewer")
        print("   3. Or use online markdown to PDF converters")
        print("   4. Or open PROJECT_REPORT_FORMATTED.txt and print to PDF")
    
    print("\n✅ Report generation completed!")

if __name__ == "__main__":
    main()
