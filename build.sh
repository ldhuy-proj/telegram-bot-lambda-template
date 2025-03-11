source config.env

echo "Login to ECR..."
aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com
echo "Done!"

# ECR handling
echo "Checking if ECR repo exists..."
ECR_EXISTS=$(aws ecr describe-repositories --repository-names "$REPO_NAME" --region "$REGION" 2>&1)
if [[ $ECR_EXISTS == *"RepositoryNotFoundException"* ]]; then
    echo "ECR repo is not yet existed, creating new one..."
    aws ecr create-repository --repository-name "$REPO_NAME" --region "$REGION" --no-cli-pager
    echo "Done!"
else
    echo "ECR repo existed. Done!"
fi


# DEV
echo "Building and pushing Docker image to ECR..."
docker build --platform linux/arm64 -t $IMAGE_NAME .
docker tag $IMAGE_NAME:latest $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$REPO_NAME:latest
docker push $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$REPO_NAME:latest
echo "Done!"

# Lambda function handling
ROLE_NAME="lambda-basic-role"
POLICY_ARN="arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"

# Create lambda role if not exists
echo "Checking if Lambda role exists..."
ROLE_EXISTS=$(aws iam get-role --role-name "$ROLE_NAME" 2>&1)

if [[ $ROLE_EXISTS == *"NoSuchEntity"* ]]; then
    echo "IAM Role not yet existed, creating a new one..."

    # Creating new role
    aws iam create-role \
        --role-name "$ROLE_NAME" \
        --assume-role-policy-document '{
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "lambda.amazonaws.com"
                    },
                    "Action": "sts:AssumeRole"
                }
            ]
        }'

    # Set policy for role
    aws iam attach-role-policy \
        --role-name "$ROLE_NAME" \
        --policy-arn "$POLICY_ARN"

    # Wait for 5 secs to make sure the role is created
    sleep 5
else
    echo "IAM Role already existed. Done!"
fi

LAMBDA_ROLE_ARN=$(aws iam get-role --role-name "$ROLE_NAME" --query 'Role.Arn' --output text)
echo "Using IAM Role ARN: $LAMBDA_ROLE_ARN"

echo "Checking if Lambda function exists..."
LAMBDA_EXISTS=$(aws lambda get-function --function-name "$FUNCTION_NAME" 2>&1)

if [[ $LAMBDA_EXISTS == *"ResourceNotFoundException"* ]]; then
    echo "Lambda function is not yet existed, creating a new one..."
    aws lambda create-function \
        --function-name "$FUNCTION_NAME" \
        --package-type Image \
        --code ImageUri="$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$REPO_NAME:latest" \
        --role "$LAMBDA_ROLE_ARN" \
        --architectures arm64 \
        --timeout 60 \
        --memory-size 128 \
        --no-cli-pager
else
    echo "Updating Lambda function code with pushed Docker image..."
    aws lambda update-function-code \
        --function-name $FUNCTION_NAME \
        --image-uri $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$REPO_NAME:latest \
        --no-cli-pager
fi

echo "Waiting for Lambda function to be updated..."
aws lambda wait function-updated \
    --function-name $FUNCTION_NAME
echo "Done!"

echo "Updating Lambda function environment variables..."
aws lambda update-function-configuration \
    --function-name $FUNCTION_NAME \
    --environment "Variables={$ENVIRONMENNT_VARIABLES}"\
    --no-cli-pager
echo "Done!"

echo "Set policy for invoking Lambda URL..."
LAMBDA_ARN=$(aws lambda get-function --function-name "$FUNCTION_NAME" --query 'Configuration.FunctionArn' --output text)
POLICY_NAME="LambdaInvokeFunctionUrlPolicy"
echo "Lambda ARN: $LAMBDA_ARN"
STATEMENT_ID="AllowFunctionURLPublicAccess"

# Check if the permission already exists
EXISTING_POLICY=$(aws lambda get-policy --function-name "$FUNCTION_NAME" --query 'Policy' --output text 2>/dev/null | grep "$STATEMENT_ID")
if [[ -n "$EXISTING_POLICY" ]]; then
    echo "Permission '$STATEMENT_ID' already exists for Lambda: $FUNCTION_NAME"
else
    echo "Permission '$STATEMENT_ID' is not yet created. Creating new one..."

    aws lambda add-permission \
        --function-name "$FUNCTION_NAME" \
        --statement-id "$STATEMENT_ID" \
        --action "lambda:InvokeFunctionUrl" \
        --principal "*" \
        --function-url-auth-type "NONE"
fi
echo "Done!"

echo "Checking if Function URL exists..."
URL_EXISTS=$(aws lambda get-function-url-config --function-name "$FUNCTION_NAME" 2>&1)

if [[ $URL_EXISTS == *"FunctionUrlConfigNotFoundException"* ]]; then
    echo "🔹 Function URL is not yet existed, creating new one..."
    aws lambda create-function-url-config \
        --function-name "$FUNCTION_NAME" \
        --auth-type NONE
else
    echo "Function URL existed!"
fi
echo "Done!"


# Set webhook
echo "Setting up webhook..."
export BOT_TOKEN=$BOT_TOKEN
LAMBDA_FUNCTION_URL=$(aws lambda get-function-url-config \
    --function-name $FUNCTION_NAME \
    --query 'FunctionUrl' --output text)

echo "Lambda Function URL: $LAMBDA_FUNCTION_URL"


# Run Python script
python3 tlg_set_webhook.py
if [[ $? -eq 0 ]]; then
    echo "Webhook is set up successfully!"
else
    echo "Setting up webhook failed!"
fi
