#!/bin/bash

# Get a list of AWS profiles from the AWS CLI configuration file
profiles=$(grep '^\[profile' ~/.aws/config | awk -F'profile ' '{print $2}' | tr -d ']')

# Iterate through each profile and print the account information
for profile in $profiles; do
    echo "Profile: $profile"

    # Use the AWS CLI to get account information for the current profile
    account_info=$(aws sts get-caller-identity --profile $profile)

    # Print the account information
    echo "Account ID: $(echo $account_info | jq -r '.Account')"
    echo "Arn: $(echo $account_info | jq -r '.Arn')"

    echo "------------------------"
done