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
DB_CONTAINER="safa-mysql"
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

# Function to reset user password
reset_password() {
    echo -e "${YELLOW}Enter the email address of the user:${NC}"
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

    echo -e "${YELLOW}Enter new password:${NC}"
    read -s new_password
    echo ""

    if [[ -z "$new_password" ]]; then
        echo -e "${RED}Error: Password cannot be empty${NC}"
        return 1
    fi

    echo -e "${YELLOW}Generating password hash...${NC}"

    # Use the backend container to generate a BCrypt hash
    # Spring Boot uses BCrypt with strength 10 by default
    local hashed_password=$(docker exec safa-bend java -cp /app/classes:/app/lib/* \
        -Dloader.main=org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder \
        org.springframework.boot.loader.launch.PropertiesLauncher "$new_password" 2>/dev/null | grep -v "^$" | tail -1)

    # Fallback: use Python if available (generates BCrypt hash)
    if [[ -z "$hashed_password" ]]; then
        echo -e "${YELLOW}Using Python to generate hash...${NC}"
        hashed_password=$(python3 -c "import bcrypt; print(bcrypt.hashpw('$new_password'.encode(), bcrypt.gensalt(rounds=10)).decode())" 2>/dev/null)
    fi

    if [[ -z "$hashed_password" ]]; then
        echo -e "${RED}Error: Could not generate password hash${NC}"
        echo -e "${YELLOW}Please install python3-bcrypt or ensure the backend container is running${NC}"
        return 1
    fi

    # Update password in database
    execute_sql "UPDATE safa_user SET password = '$hashed_password' WHERE email = '$email';"

    echo -e "${GREEN}Success! Password has been reset for user '$email'${NC}"
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

# Function to view pending invites
view_invites() {
    echo -e "${YELLOW}Pending Member Invites:${NC}"
    echo ""
    execute_sql "SELECT HEX(id) as invite_id, HEX(entity_id) as org_id, expiration, role, uses FROM membership_invite_token ORDER BY expiration DESC;" | column -t -s $'\t'
    echo ""
}

# Function to delete/accept an invite token
accept_invite() {
    echo -e "${YELLOW}Enter the invite ID (hex format) to accept/verify:${NC}"
    echo -e "${BLUE}Tip: Use option 8 to view pending invites and get the invite_id${NC}"
    read -r invite_id

    if [[ -z "$invite_id" ]]; then
        echo -e "${RED}Error: Invite ID cannot be empty${NC}"
        return 1
    fi

    # Convert hex to binary for query
    local binary_id=$(echo "$invite_id" | sed 's/\(..\)/\\x\1/g')

    # Check if invite exists
    local invite_count=$(execute_sql "SELECT COUNT(*) FROM membership_invite_token WHERE HEX(id) = '$invite_id';" | tail -n 1)

    if [[ "$invite_count" -eq 0 ]]; then
        echo -e "${RED}Error: Invite with ID '$invite_id' not found${NC}"
        return 1
    fi

    # Show invite details
    echo ""
    echo -e "${YELLOW}Invite details:${NC}"
    execute_sql "SELECT HEX(id) as invite_id, HEX(entity_id) as org_id, expiration, role, uses FROM membership_invite_token WHERE HEX(id) = '$invite_id';" | column -t -s $'\t'
    echo ""

    # Confirm deletion
    echo -e "${YELLOW}Delete this invite token? This effectively 'accepts' the invite. (yes/no)${NC}"
    read -r confirmation

    if [[ "$confirmation" != "yes" ]]; then
        echo -e "${YELLOW}Operation cancelled${NC}"
        return 0
    fi

    # Delete the invite token
    execute_sql "DELETE FROM membership_invite_token WHERE HEX(id) = '$invite_id';"

    echo -e "${GREEN}Success! Invite token has been accepted/removed${NC}"
    echo ""
}

# Function to view all projects
view_projects() {
    echo -e "${YELLOW}Available Projects:${NC}"
    echo ""
    execute_sql "SELECT p.project_id, p.name, p.description, pv.version_id FROM project p LEFT JOIN project_version pv ON p.project_id = pv.project_id ORDER BY p.name;" | column -t -s $'\t'
    echo ""
}

# Function to view user's project memberships
view_user_projects() {
    echo -e "${YELLOW}Enter the email address of the user:${NC}"
    read -r email

    if [[ -z "$email" ]]; then
        echo -e "${RED}Error: Email cannot be empty${NC}"
        return 1
    fi

    # Get user_id
    local user_id=$(execute_sql "SELECT user_id FROM safa_user WHERE email = '$email';" | tail -n 1)

    if [[ -z "$user_id" ]]; then
        echo -e "${RED}Error: User with email '$email' not found${NC}"
        return 1
    fi

    echo ""
    echo -e "${YELLOW}Projects for user '$email':${NC}"
    echo ""
    execute_sql "SELECT upm.membership_id, upm.project_role, p.project_id, p.name FROM user_project_membership upm JOIN project p ON upm.project_id = p.project_id WHERE upm.user_id = '$user_id';" | column -t -s $'\t'
    echo ""
}

# Function to add user to project
add_user_to_project() {
    echo -e "${YELLOW}Step 1: Select User${NC}"
    echo ""
    execute_sql "SELECT user_id, email, verified FROM safa_user;" | column -t -s $'\t'
    echo ""
    echo -e "${YELLOW}Enter the email address of the user:${NC}"
    read -r email

    if [[ -z "$email" ]]; then
        echo -e "${RED}Error: Email cannot be empty${NC}"
        return 1
    fi

    # Get user_id
    local user_id=$(execute_sql "SELECT user_id FROM safa_user WHERE email = '$email';" | tail -n 1)

    if [[ -z "$user_id" ]]; then
        echo -e "${RED}Error: User with email '$email' not found${NC}"
        return 1
    fi

    echo ""
    echo -e "${GREEN}Selected user: $email${NC}"
    echo ""

    echo -e "${YELLOW}Step 2: Select Project${NC}"
    echo ""
    execute_sql "SELECT project_id, name, description FROM project ORDER BY name;" | column -t -s $'\t'
    echo ""
    echo -e "${YELLOW}Enter the project_id:${NC}"
    read -r project_id

    if [[ -z "$project_id" ]]; then
        echo -e "${RED}Error: Project ID cannot be empty${NC}"
        return 1
    fi

    # Check if project exists
    local project_count=$(execute_sql "SELECT COUNT(*) FROM project WHERE project_id = '$project_id';" | tail -n 1)

    if [[ "$project_count" -eq 0 ]]; then
        echo -e "${RED}Error: Project with ID '$project_id' not found${NC}"
        return 1
    fi

    # Get project name
    local project_name=$(execute_sql "SELECT name FROM project WHERE project_id = '$project_id';" | tail -n 1)

    echo ""
    echo -e "${GREEN}Selected project: $project_name${NC}"
    echo ""

    echo -e "${YELLOW}Step 3: Select Role${NC}"
    echo ""
    echo "  1) OWNER"
    echo "  2) EDITOR"
    echo "  3) VIEWER"
    echo ""
    echo -ne "${YELLOW}Enter role number [1-3]: ${NC}"
    read -r role_choice

    local role
    case $role_choice in
        1)
            role="OWNER"
            ;;
        2)
            role="EDITOR"
            ;;
        3)
            role="VIEWER"
            ;;
        *)
            echo -e "${RED}Invalid role choice${NC}"
            return 1
            ;;
    esac

    echo ""
    echo -e "${GREEN}Selected role: $role${NC}"
    echo ""

    # Check if membership already exists
    local existing=$(execute_sql "SELECT COUNT(*) FROM user_project_membership WHERE user_id = '$user_id' AND project_id = '$project_id';" | tail -n 1)

    if [[ "$existing" -gt 0 ]]; then
        echo -e "${YELLOW}User already has membership to this project. Update role? (yes/no)${NC}"
        read -r update_confirm

        if [[ "$update_confirm" == "yes" ]]; then
            execute_sql "UPDATE user_project_membership SET project_role = '$role' WHERE user_id = '$user_id' AND project_id = '$project_id';"
            echo -e "${GREEN}Success! Updated membership role to $role${NC}"
        else
            echo -e "${YELLOW}Operation cancelled${NC}"
            return 0
        fi
    else
        # Generate a UUID for membership_id
        local membership_id=$(uuidgen)

        # Insert membership
        execute_sql "INSERT INTO user_project_membership (membership_id, project_role, user_id, project_id) VALUES ('$membership_id', '$role', '$user_id', '$project_id');"

        echo -e "${GREEN}Success! Added user '$email' to project '$project_name' with role $role${NC}"
    fi

    echo ""
    echo -e "${YELLOW}Current memberships for this user:${NC}"
    execute_sql "SELECT upm.membership_id, upm.project_role, p.project_id, p.name FROM user_project_membership upm JOIN project p ON upm.project_id = p.project_id WHERE upm.user_id = '$user_id';" | column -t -s $'\t'
    echo ""
}

# Function to remove user from project
remove_user_from_project() {
    echo -e "${YELLOW}Enter the email address of the user:${NC}"
    read -r email

    if [[ -z "$email" ]]; then
        echo -e "${RED}Error: Email cannot be empty${NC}"
        return 1
    fi

    # Get user_id
    local user_id=$(execute_sql "SELECT user_id FROM safa_user WHERE email = '$email';" | tail -n 1)

    if [[ -z "$user_id" ]]; then
        echo -e "${RED}Error: User with email '$email' not found${NC}"
        return 1
    fi

    echo ""
    echo -e "${YELLOW}Current project memberships for '$email':${NC}"
    execute_sql "SELECT upm.membership_id, upm.project_role, p.project_id, p.name FROM user_project_membership upm JOIN project p ON upm.project_id = p.project_id WHERE upm.user_id = '$user_id';" | column -t -s $'\t'
    echo ""

    echo -e "${YELLOW}Enter the project_id to remove user from:${NC}"
    read -r project_id

    if [[ -z "$project_id" ]]; then
        echo -e "${RED}Error: Project ID cannot be empty${NC}"
        return 1
    fi

    # Check if membership exists
    local membership_count=$(execute_sql "SELECT COUNT(*) FROM user_project_membership WHERE user_id = '$user_id' AND project_id = '$project_id';" | tail -n 1)

    if [[ "$membership_count" -eq 0 ]]; then
        echo -e "${RED}Error: User does not have membership to this project${NC}"
        return 1
    fi

    # Confirm removal
    echo -e "${RED}Remove user '$email' from this project? (yes/no)${NC}"
    read -r confirmation

    if [[ "$confirmation" != "yes" ]]; then
        echo -e "${YELLOW}Operation cancelled${NC}"
        return 0
    fi

    # Delete membership
    execute_sql "DELETE FROM user_project_membership WHERE user_id = '$user_id' AND project_id = '$project_id';"

    echo -e "${GREEN}Success! Removed user from project${NC}"
    echo ""
}

# Main menu
show_menu() {
    echo -e "${YELLOW}Select an action:${NC}"
    echo ""
    echo "  ${BLUE}USER MANAGEMENT:${NC}"
    echo "  1) View all users"
    echo "  2) View user statistics"
    echo "  3) Verify user and promote to superuser"
    echo "  4) Verify user only"
    echo "  5) Promote user to superuser"
    echo "  6) Demote user from superuser"
    echo "  7) Reset user password"
    echo "  8) Delete user"
    echo ""
    echo "  ${BLUE}INVITE MANAGEMENT:${NC}"
    echo "  9) View pending member invites"
    echo "  10) Accept/remove invite token"
    echo ""
    echo "  ${BLUE}PROJECT MEMBERSHIP:${NC}"
    echo "  11) View all projects"
    echo "  12) View user's project memberships"
    echo "  13) Add user to project"
    echo "  14) Remove user from project"
    echo ""
    echo "  0) Exit"
    echo ""
    echo -ne "${YELLOW}Enter your choice [0-14]: ${NC}"
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
                reset_password
                ;;
            8)
                delete_user
                ;;
            9)
                view_invites
                ;;
            10)
                accept_invite
                ;;
            11)
                view_projects
                ;;
            12)
                view_user_projects
                ;;
            13)
                add_user_to_project
                ;;
            14)
                remove_user_from_project
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
