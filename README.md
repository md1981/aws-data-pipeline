# AWS Data Processing Pipeline

This project sets up a basic data processing pipeline using AWS free tier services. The pipeline ingests data from an S3 bucket, processes it using a containerized application, and stores the results in an RDS PostgreSQL database.

## Architecture

The pipeline consists of the following components:

1. Amazon S3 bucket for data ingestion
2. Amazon ECS (Elastic Container Service) for running the containerized application
3. Amazon RDS PostgreSQL for storing results
4. AWS IAM for security roles and policies
5. AWS CloudFormation for infrastructure as code

## Prerequisites

- AWS CLI installed and configured
- Docker installed (for building and pushing the container image)
- Python 3.9 or later

## Deployment

1. Build and push the Docker image to Amazon ECR
2. Deploy the CloudFormation stack
3. Run the ECS task to process data

## Testing

1. Upload a test file to the S3 bucket
2. Run the ECS task
3. Check the task logs
4. Verify the data in the RDS database

## Security

This project implements the following security best practices:

- IAM roles with least privilege principle
- S3 bucket with versioning enabled
- RDS instance not publicly accessible
- Secrets (database password) managed through CloudFormation parameters

## License

This project is licensed under the MIT License.