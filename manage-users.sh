#!/bin/bash

# SAFA User Management Script
# This script provides utilities for managing users in the SAFA database

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Database credentials from docker-compose.yaml
DB_CONTAINER="mysql"
DB_NAME="safa-db"
DB_USER="root"
DB_PASS="secret2"

# Function to execute SQL query
execute_sql() {
    local query="$1"
    docker exec "$DB_CONTAINER" mysql -u "$DB_USER" -p"$DB_PASS" "$DB_NAME" -e "$query" 2>/dev/null || {
        echo -e "${RED}Error: Failed to execute query${NC}"
        return 1
    }
}

# Function to display header
show_header() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}  SAFA User Management Tool${NC}"
    echo -e "${BLUE}================================${NC}"
    echo ""
}

# Function to view all users
view_users() {
    echo -e "${YELLOW}Current Users:${NC}"
    echo ""
    execute_sql "SELECT user_id, email, superuser, verified FROM safa_user;" | column -t -s $'\t'
    echo ""
}

# Function to verify user and set as superuser
verify_and_promote() {
    echo -e "${YELLOW}Enter the email address of the user to verify and promote:${NC}"
    read -r email

    if [[ -z "$email" ]]; then
        echo -e "${RED}Error: Email cannot be empty${NC}"
        return 1
    fi

    # Check if user exists
    local user_count=$(execute_sql "SELECT COUNT(*) FROM safa_user WHERE email = '$email';" | tail -n 1)

    if [[ "$user_count" -eq 0 ]]; then
        echo -e "${RED}Error: User with email '$email' not found${NC}"
        return 1
    fi

    # Update user
    execute_sql "UPDATE safa_user SET verified = 1, superuser = 1 WHERE email = '$email';"

    echo -e "${GREEN}Success! User '$email' has been verified and promoted to superuser${NC}"
    echo ""
    echo -e "${YELLOW}Updated user details:${NC}"
    execute_sql "SELECT user_id, email, superuser, verified FROM safa_user WHERE email = '$email';" | column -t -s $'\t'
    echo ""
}

# Function to verify user (without superuser promotion)
verify_user() {
    echo -e "${YELLOW}Enter the email address of the user to verify:${NC}"
    read -r email

    if [[ -z "$email" ]]; then
        echo -e "${RED}Error: Email cannot be empty${NC}"
        return 1
    fi

    # Check if user exists
    local user_count=$(execute_sql "SELECT COUNT(*) FROM safa_user WHERE email = '$email';" | tail -n 1)

    if [[ "$user_count" -eq 0 ]]; then
        echo -e "${RED}Error: User with email '$email' not found${NC}"
        return 1
    fi

    # Update user
    execute_sql "UPDATE safa_user SET verified = 1 WHERE email = '$email';"

    echo -e "${GREEN}Success! User '$email' has been verified${NC}"
    echo ""
    echo -e "${YELLOW}Updated user details:${NC}"
    execute_sql "SELECT user_id, email, superuser, verified FROM safa_user WHERE email = '$email';" | column -t -s $'\t'
    echo ""
}

# Function to promote user to superuser
promote_user() {
    echo -e "${YELLOW}Enter the email address of the user to promote to superuser:${NC}"
    read -r email

    if [[ -z "$email" ]]; then
        echo -e "${RED}Error: Email cannot be empty${NC}"
        return 1
    fi

    # Check if user exists
    local user_count=$(execute_sql "SELECT COUNT(*) FROM safa_user WHERE email = '$email';" | tail -n 1)

    if [[ "$user_count" -eq 0 ]]; then
        echo -e "${RED}Error: User with email '$email' not found${NC}"
        return 1
    fi

    # Update user
    execute_sql "UPDATE safa_user SET superuser = 1 WHERE email = '$email';"

    echo -e "${GREEN}Success! User '$email' has been promoted to superuser${NC}"
    echo ""
    echo -e "${YELLOW}Updated user details:${NC}"
    execute_sql "SELECT user_id, email, superuser, verified FROM safa_user WHERE email = '$email';" | column -t -s $'\t'
    echo ""
}

# Function to demote user from superuser
demote_user() {
    echo -e "${YELLOW}Enter the email address of the user to demote from superuser:${NC}"
    read -r email

    if [[ -z "$email" ]]; then
        echo -e "${RED}Error: Email cannot be empty${NC}"
        return 1
    fi

    # Check if user exists
    local user_count=$(execute_sql "SELECT COUNT(*) FROM safa_user WHERE email = '$email';" | tail -n 1)

    if [[ "$user_count" -eq 0 ]]; then
        echo -e "${RED}Error: User with email '$email' not found${NC}"
        return 1
    fi

    # Update user
    execute_sql "UPDATE safa_user SET superuser = 0 WHERE email = '$email';"

    echo -e "${GREEN}Success! User '$email' has been demoted from superuser${NC}"
    echo ""
    echo -e "${YELLOW}Updated user details:${NC}"
    execute_sql "SELECT user_id, email, superuser, verified FROM safa_user WHERE email = '$email';" | column -t -s $'\t'
    echo ""
}

# Function to delete user
delete_user() {
    echo -e "${RED}WARNING: This will permanently delete the user and all associated data!${NC}"
    echo -e "${YELLOW}Enter the email address of the user to delete:${NC}"
    read -r email

    if [[ -z "$email" ]]; then
        echo -e "${RED}Error: Email cannot be empty${NC}"
        return 1
    fi

    # Check if user exists
    local user_count=$(execute_sql "SELECT COUNT(*) FROM safa_user WHERE email = '$email';" | tail -n 1)

    if [[ "$user_count" -eq 0 ]]; then
        echo -e "${RED}Error: User with email '$email' not found${NC}"
        return 1
    fi

    # Show user details
    echo ""
    echo -e "${YELLOW}User to be deleted:${NC}"
    execute_sql "SELECT user_id, email, superuser, verified FROM safa_user WHERE email = '$email';" | column -t -s $'\t'
    echo ""

    # Confirm deletion
    echo -e "${RED}Are you sure you want to delete this user? (yes/no)${NC}"
    read -r confirmation

    if [[ "$confirmation" != "yes" ]]; then
        echo -e "${YELLOW}Deletion cancelled${NC}"
        return 0
    fi

    # Delete user
    execute_sql "DELETE FROM safa_user WHERE email = '$email';"

    echo -e "${GREEN}Success! User '$email' has been deleted${NC}"
    echo ""
}

# Function to show user count
show_user_stats() {
    echo -e "${YELLOW}User Statistics:${NC}"
    echo ""

    local total=$(execute_sql "SELECT COUNT(*) FROM safa_user;" | tail -n 1)
    local verified=$(execute_sql "SELECT COUNT(*) FROM safa_user WHERE verified = 1;" | tail -n 1)
    local superusers=$(execute_sql "SELECT COUNT(*) FROM safa_user WHERE superuser = 1;" | tail -n 1)

    echo -e "  Total Users:      ${BLUE}$total${NC}"
    echo -e "  Verified Users:   ${GREEN}$verified${NC}"
    echo -e "  Superusers:       ${GREEN}$superusers${NC}"
    echo ""
}

# Main menu
show_menu() {
    echo -e "${YELLOW}Select an action:${NC}"
    echo ""
    echo "  1) View all users"
    echo "  2) View user statistics"
    echo "  3) Verify user and promote to superuser"
    echo "  4) Verify user only"
    echo "  5) Promote user to superuser"
    echo "  6) Demote user from superuser"
    echo "  7) Delete user"
    echo "  0) Exit"
    echo ""
    echo -ne "${YELLOW}Enter your choice [0-7]: ${NC}"
}

# Main loop
main() {
    show_header

    # Check if docker container is running
    if ! docker ps | grep -q "$DB_CONTAINER"; then
        echo -e "${RED}Error: MySQL container '$DB_CONTAINER' is not running${NC}"
        echo -e "${YELLOW}Please start the container with: docker-compose up -d${NC}"
        exit 1
    fi

    while true; do
        show_menu
        read -r choice
        echo ""

        case $choice in
            1)
                view_users
                ;;
            2)
                show_user_stats
                ;;
            3)
                verify_and_promote
                ;;
            4)
                verify_user
                ;;
            5)
                promote_user
                ;;
            6)
                demote_user
                ;;
            7)
                delete_user
                ;;
            0)
                echo -e "${GREEN}Goodbye!${NC}"
                exit 0
                ;;
            *)
                echo -e "${RED}Invalid choice. Please try again.${NC}"
                echo ""
                ;;
        esac

        echo -e "${BLUE}Press Enter to continue...${NC}"
        read -r
        echo ""
    done
}

# Run main function
main
