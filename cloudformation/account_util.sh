extract_account_id() {
    local text="$1"
    local regex="Account: '([0-9]+)'"

    if [[ $text =~ $regex ]]; then
        accountId="${BASH_REMATCH[1]}"
        echo "$accountId"
    else
        echo "Unable to extract account ID: $text"
        exit 1
    fi
}

echo "Enter profile"
read -e profile

accountInfo=$(aws sts get-caller-identity --profile $profile 2>&1)
accountId=$(extract_account_id "$accountInfo")