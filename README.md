# data_reporting_automation
🚀 Unlocking Efficiency: Automating Data Reporting 

Project Overview
The Data Reporting Automation project aims to streamline and automate the process of data extraction, processing, and upload to OneDrive. The primary objectives are to save time, reduce manual effort, enhance data accuracy, and improve cost efficiency.

Functional Requirements
Data Extraction

The system should connect to an AWS RDS PostgreSQL database using an SSH tunnel.
An SQL query must be executed to fetch data from the database.
Data Processing

The fetched data should be processed and converted into an Excel file.
Excel files must be organized by date ranges and project identifiers.
VeraCrypt Integration

The system should mount and dismount a VeraCrypt volume to secure data transfer.
Files should be copied to the mounted VeraCrypt drive.
The VeraCrypt drive should be dismounted after data transfer.
OneDrive Integration

The system must authenticate with OneDrive using provided credentials.
Files should be uploaded to a specific OneDrive location.
Large files should be chunked for upload.
Non-Functional Requirements
Security

Data transfer and storage must be secure. Sensitive data should be encrypted using VeraCrypt.
Credentials and keys must be stored securely and not hard-coded in the script.
Performance

The system should perform data extraction and processing efficiently.
Uploading large files should not cause performance degradation.
Reliability

The system should handle errors gracefully and provide meaningful error messages.
It must ensure data consistency and accuracy during the automation process.
Scalability

The script should be able to accommodate changes in data volume and structure.
User Documentation

Provide clear documentation on how to set up and configure the system.
Include usage instructions for stakeholders.
Constraints
Environment

The script is expected to run in a Unix-based environment.
Dependencies

Ensure that all required libraries and tools are available and up to date.
Data Reporting Schedule

The script should run at specific times or on a schedule as determined by the project requirements.
Future Enhancements
Monitoring and Alerting

Consider adding a monitoring and alerting system to track the script's execution and notify stakeholders of any issues.
Log and Audit Trail

Implement a log system for tracking the script's activities, errors, and successful completions.
User Management

Add user roles and access controls for managing data access and reporting.
Cloud Integration

Consider extending the script to support other cloud platforms for data storage and sharing.
