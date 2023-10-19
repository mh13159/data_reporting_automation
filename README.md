# data_reporting_automation
🚀 Unlocking Efficiency: Automating Data Reporting 

**Project Overview
The Data Reporting Automation project aims to streamline and automate the process of data extraction, processing, and upload to OneDrive. The primary objectives are to save time, reduce manual effort, enhance data accuracy, and improve cost efficiency.

**Functional Requirements

1.Data Extraction
The system should connect to an AWS RDS PostgreSQL database using an SSH tunnel.
An SQL query must be executed to fetch data from the database.

2.Data Processing
The fetched data should be processed and converted into an Excel file.
Excel files must be organized by date ranges and project identifiers.

3.VeraCrypt Integration
The system should mount and dismount a VeraCrypt volume to secure data transfer.
Files should be copied to the mounted VeraCrypt drive.
The VeraCrypt drive should be dismounted after data transfer.

4.OneDrive Integration
The system must authenticate with OneDrive using provided credentials.
Files should be uploaded to a specific OneDrive location.
Large files should be chunked for upload.

5.Non-Functional Requirements
  a.Security
  Data transfer and storage must be secure. Sensitive data should be encrypted using VeraCrypt.
  Credentials and keys must be stored securely and not hard-coded in the script.
  
  b.Performance
  The system should perform data extraction and processing efficiently.
  Uploading large files should not cause performance degradation.
  
  c.Reliability
  The system should handle errors gracefully and provide meaningful error messages.
  It must ensure data consistency and accuracy during the automation process.
  
  d.Scalability
  The script should be able to accommodate changes in data volume and structure.
  
  e.User Documentation
  Provide clear documentation on how to set up and configure the system.
  Include usage instructions for stakeholders.
  
  f.Constraints
   1.Environment
   The script is expected to run in a Unix-based environment.
   
   2.Dependencies
   Ensure that all required libraries and tools are available and up to date.
   
   3.Data Reporting Schedule
   The script should run at specific times or on a schedule as determined by the project requirements.

**Future Enhancements
  1. Monitoring and Alerting
     
  Consider adding a monitoring and alerting system to track the script's execution and notify stakeholders of any issues.
  
  2.Log and Audit Trail
  
  Implement a log system for tracking the script's activities, errors, and successful completions.
