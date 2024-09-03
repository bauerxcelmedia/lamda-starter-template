
# Python - Repository Template for Serverless Applications on AWS

This repository provides a pre-configured template for building serverless applications on AWS using Python and the Serverless Framework. It offers a basic architecture that includes Lambda functions, API Gateway, Amazon DynamoDB (DocumentDB), and an S3 bucket, allowing you to focus on implementing your project's core logic.

## Key Features:

- Serverless architecture: Leverage the benefits of serverless computing for scalable and cost-effective applications.
- Python-based Lambda functions: Write your business logic in Python for a familiar and productive development experience.
- API Gateway: Expose your Lambda functions as RESTful APIs for easy integration with clients.
- DynamoDB: Store and retrieve data in a NoSQL database for efficient and scalable data management.
- S3 bucket: Utilize S3 for object storage to store files, images, or other static content.
- Unit and integration tests: Includes sample tests to ensure code quality and reliability.
- GitHub Actions workflow: Automated deployment to different environments (SIT and Prod).

## Getting Started:

1. Clone the repository:

```bash
git clone https://github.com/bauerxcelmedia/lamda-starter-template.git
cd lamda-starter-template
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure AWS credentials:
    Set up your AWS credentials using the AWS CLI configuration file (~/.aws/config or ~/.aws/credentials).

4. Configure environment variables:
    Create a .env file in the project root directory to store environment-specific variables.

5. Deploy to your desired environment:
    Use the Serverless Framework commands to deploy to SIT or Prod environments.

## Project Structure:

- `lambda/`: Contains Python code for your Lambda functions.
- `tests/`: Includes unit and integration tests.
- `serverless.yml`: Serverless Framework configuration file.
- `requirements.txt`: List of Python dependencies.
- `.github/workflows/`: GitHub Actions workflows for deployment.

## Additional Information:

- Refer to the Serverless Framework documentation for more details on configuration and deployment.
- Customize the template to suit your specific project requirements.
- Explore the sample Lambda functions and tests for guidance.

## Contributing:

Contributions are welcome! Feel free to submit pull requests or issues.
