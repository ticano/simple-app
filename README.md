# simple-app

This project contains source code and supporting files for a serverless application that you can deploy with the SAM CLI. It includes the following files and folders.

- app - Code for the application's Lambda function.
- template.yaml - A template that defines the application's AWS resources.
- cf_pipeline - Cloudformation file to create the CI/CD pipeline to automate the stack update

The application uses several AWS resources, including Lambda functions, an API Gateway API and a DynamoDB table. These resources are defined in the `template.yaml` file in this project. You can update the template to add AWS resources through the same deployment process that updates your application code.

## Deploy the sample application with CI/CD

To automate the deployment process I decided to use the AWS Codepipeline because it is a managed service and also allows us to integrates easily with the other AWS services.

Before use it a few things are necessary:

1 - A Github account
2 - A Github repository with all this code
3 - A Github OAuth Token with full permissions on admin:repo_hook and repo

With this information you can create the Pipeline Stack using the command line or creating it using the AWS console.

Using the command line:

```bash

aws cloudformation create-stack --stack-name code-challenge-pipeline --template-body file://cf_pipeline/code_pipeline.yaml --parameters ParameterKey=GithubToken,ParameterValue=<YOUR_GITHUB_TOKEN> ParameterKey=GithubUser,ParameterValue=<GITHUB_USERNAME> ParameterKey=GithubRepo,ParameterValue=<GITHUB_REPO> ParameterKey=GithubBranch,ParameterValue=<GITHUB_BRANCH> --capabilities=CAPABILITY_NAMED_IAM

```

The Pipeline has 3 stages:

1 - **Source:** Used to download the Github source code from the Github repository
2 - **ApplicationBuild:** Will package the SAM template file to be used on the Deploy stage
3 - **ApplicationDeploy:** Will create a new cloudformation Stack that will create all the necessary resources to run the application, e.g, Lambda Functins, API GW, DynamodDB Table, S3 buckets, IAM Roles and etc.



### Get the application stack Output

```bash
aws cloudformation describe-stacks --stack-name challenge-application --query='Stacks[].Outputs[].{OutputKey: OutputKey, Description: Description, OutputValue: OutputValue}' --output=table
```

Use the **EndpointDomainName** address to send the requests.


### Test the API

To test API methods you can execute the commands below:

**POST** Creates a new item

```bash
curl --location --request POST '<API_GW_URL>/Prod/objects' \
--header 'Content-Type: application/json' \
--data-raw '{
    "make": "Volkswagen",
    "model": "Golf",
    "category": "Hatchback",
    "year": 2019
}'
```


**GET** List All items

```bash

curl --location --request GET '<API_GW_URL>/Prod/objects'

```

**GET** Get an items

```bash

curl --location --request GET '<API_GW_URL>/Prod/objects/<object_id>'

```
Example: https://hi7htjxbja.execute-api.eu-central-1.amazonaws.com/Stage/objects/77b31ad1-62dd-4f3e-b9ff-c4a4c18173c7


###
**PUT** Update an Item

```bash

curl --location --request PUT '<API_GW_URL>/Prod/objects/<object_id>'

```

Example: https://hi7htjxbja.execute-api.eu-central-1.amazonaws.com/Stage/objects/77b31ad1-62dd-4f3e-b9ff-c4a4c18173c712


**DELETE** Delete an items

```bash

curl --location --request DELETE '<API_GW_URL>/Prod/objects/<object_id>'

```

Example: https://hi7htjxbja.execute-api.eu-central-1.amazonaws.com/Stage/objects/77b31ad1-62dd-4f3e-b9ff-c4a4c18173c712



## Deploy the sample application without CI/CD

The Serverless Application Model Command Line Interface (SAM CLI) is an extension of the AWS CLI that adds functionality for building and testing Lambda applications. It uses Docker to run your functions in an Amazon Linux environment that matches Lambda. It can also emulate your application's build environment and API.

To use the SAM CLI, you need the following tools.

* SAM CLI - [Install the SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* [Python 3 installed](https://www.python.org/downloads/)
* Docker - [Install Docker community edition](https://hub.docker.com/search/?type=edition&offering=community)

To build and deploy your application for the first time, run the following in your shell:

```bash
sam build --use-container
sam deploy --guided
```

The first command will build the source of your application. The second command will package and deploy your application to AWS, with a series of prompts:

* **Stack Name**: The name of the stack to deploy to CloudFormation. This should be unique to your account and region, and a good starting point would be something matching your project name.
* **AWS Region**: The AWS region you want to deploy your app to.
* **Confirm changes before deploy**: If set to yes, any change sets will be shown to you before execution for manual review. If set to no, the AWS SAM CLI will automatically deploy application changes.
* **Allow SAM CLI IAM role creation**: Many AWS SAM templates, including this example, create AWS IAM roles required for the AWS Lambda function(s) included to access AWS services. By default, these are scoped down to minimum required permissions. To deploy an AWS CloudFormation stack which creates or modified IAM roles, the `CAPABILITY_IAM` value for `capabilities` must be provided. If permission isn't provided through this prompt, to deploy this example you must explicitly pass `--capabilities CAPABILITY_IAM` to the `sam deploy` command.
* **Save arguments to samconfig.toml**: If set to yes, your choices will be saved to a configuration file inside the project, so that in the future you can just re-run `sam deploy` without parameters to deploy changes to your application.

You can find your API Gateway Endpoint URL in the output values displayed after deployment.



## Add a resource to your application
The application template uses AWS Serverless Application Model (AWS SAM) to define application resources. AWS SAM is an extension of AWS CloudFormation with a simpler syntax for configuring common serverless application resources such as functions, triggers, and APIs. For resources not included in [the SAM specification](https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md), you can use standard [AWS CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-template-resource-type-ref.html) resource types.

## Fetch, tail, and filter Lambda function logs

To simplify troubleshooting, SAM CLI has a command called `sam logs`. `sam logs` lets you fetch logs generated by your deployed Lambda function from the command line. In addition to printing the logs on the terminal, this command has several nifty features to help you quickly find the bug.

`NOTE`: This command works for all AWS Lambda functions; not just the ones you deploy using SAM.

```bash
simple-app$ sam logs -n HelloWorldFunction --stack-name simple-app --tail
```

You can find more information and examples about filtering Lambda function logs in the [SAM CLI Documentation](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-logging.html).


## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
aws cloudformation delete-stack --stack-name simple-app
```

## Resources

See the [AWS SAM developer guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html) for an introduction to SAM specification, the SAM CLI, and serverless application concepts.

Next, you can use AWS Serverless Application Repository to deploy ready to use Apps that go beyond hello world samples and learn how authors developed their applications: [AWS Serverless Application Repository main page](https://aws.amazon.com/serverless/serverlessrepo/)
