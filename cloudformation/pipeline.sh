#!/bin/bash

# List available AWS CLI profiles
echo "AWS Profiles"
aws configure list-profiles

defaultGithubUsername=thearod5
defaultGithubRepository=ND-SAFA/tgen-api
fileName=pipeline.yaml
connectionName=gen

# PROFILE
echo "Enter your AWS CLI profile:"
read -e awsProfile
export AWS_PROFILE=$awsProfile

# GITHUB USERNAME
echo "Enter your GitHub username($defaultGithubUsername):"
# read -e githubUsername
githubUsername=${githubUsername:-$defaultGithubUsername}

# GITHUB REPOSITORY
echo "Entry the GitHub repository($defaultGithubRepository):"
# read -e githubRepository
githubRepository=${githubRepository:-$defaultGithubRepository}

# STACK
echo "Enter the stack name:"
read -e stackName

echo "Enter Account ID:"
read -e accountId



echo "Stack: $stackName"
echo "File: $fileName"
echo "GitHub username: $githubUsername"
echo "GitHub repository: $githubRepository"

# Get the GitHub connection ARN using AWS CLI
githubConnectionArn=$(aws codestar-connections list-connections \
    --profile "$awsProfile" \
    --provider-type GitHub \
    --query "Connections[?ConnectionName=='$connectionName'].ConnectionArn" \
    --output text)

# Define an array of variables
variables=(
  "$awsProfile"
  "$githubUsername"
  "$githubRepository"
  "$stackName"
  "$githubConnectionArn"
)

# Check if any of the variables are null
for variable in "${variables[@]}"; do
    if [ -z "$variable" ]; then
        echo "Error: All user variables must have a value. Please provide values for all variables."
        exit 1
    fi
done

# Deploy CloudFormation stack with parameters
aws cloudformation deploy \
  --profile "$awsProfile" \
  --template-file "$fileName" \
  --stack-name "$stackName" \
  --capabilities CAPABILITY_IAM \
  --parameter-overrides \
    AccountId="$accountId" \
    StackName="gen" \
    GitHubConnectionArn="$githubConnectionArn" \
    GithubRepository="$githubRepository"
