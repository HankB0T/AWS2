mplementation Guide

* Prepare the CloudFormation Template
    * Save the Template: Store the provided CloudFormation template code as a .yaml or .json file on your local computer (e.g., iac-1.yaml).



* Deploy the CloudFormation Template
    * Access CloudFormation: Navigate to the CloudFormation service in the AWS console.
    * Click "Create Stack" and then "With new resources (standard)".
    * Select "Upload a template file"
    * Click "Choose file" and select your saved template file.



* Configure Stack:
    * Stack name: Provide a name for your stack (e.g., TestingAPIStack).
    * Parameters (optional): Enter values for the parameters you defined: 
        * LambdaFuncName
        * DynamoDBTableName
        * APIName
        * EnvironmentName
        * PolicyNameParam
    * Review the summary of your stack configuration.
    * Acknowledge IAM resource creation capabilities.
    * Click "Create Stack".



* Test the API
    * Once the stack creation is complete, go to the API Gateway service console.
    * Find your newly created API (using the APIName you provided).
    * Under "API Resources", select the POST method that was created.
    * Under the “Test” tab, enter the payload and click on “test”.
    * Verify that the success message has status code 200, and no errors.
    * Additionally, you can verify item creation in the respective DynamoDB table under “Explore Items” tab.
