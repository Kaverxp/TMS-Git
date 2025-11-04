#!/bin/bash

set -euo pipefail  # Безопасный режим: выход при ошибках, неопределенные переменные, ошибки в пайпах

# Проверка прав root
if (( EUID != 0 )); then
    echo "Error: Root permissions required" >&2
    exit 1
fi

# Конфигурационные переменные
readonly USER_FILE="/var/users"
readonly DEFAULT_SHELL="/sbin/nologin"
readonly SUDO_GROUPS=("it" "security")
readonly ADMIN_USER="admin"

# Функции
log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >&2
}

check_group_exists() {
    local groupname="$1"
    if getent group "$groupname" >/dev/null 2>&1; then
        log_message "Warning: Group '$groupname' already exists"
        return 0
    fi
    return 1
}

check_user_exists() {
    local username="$1"
    if getent passwd "$username" >/dev/null 2>&1; then
        log_message "Warning: User '$username' already exists"
        return 0
    fi
    return 1
}

create_group() {
    local groupname="$1"
    if ! check_group_exists "$groupname"; then
        if groupadd "$groupname"; then
            log_message "Group '$groupname' created successfully"
        else
            log_message "Error: Failed to create group '$groupname'" 
            return 1
        fi
    fi
    return 0
}

create_user() {
    local username="$1" groupname="$2" user_shell="$3"
    
    if check_user_exists "$username"; then
        return 0
    fi

    if useradd -m -g "$groupname" "$username" -s "$user_shell" 2>/dev/null; then
        passwd -d "$username" >/dev/null 2>&1
        log_message "User '$username' created with group '$groupname' and shell '$user_shell'"
    else
        log_message "Error: Failed to create user '$username'"
        return 1
    fi
}

setup_sudo_access() {
    local username="$1" groupname="$2"
    local shell="$DEFAULT_SHELL"
    local sudoers_changed=false

    # Проверяем необходимость настройки sudo
    if [[ " ${SUDO_GROUPS[@]} " =~ " ${groupname} " ]]; then
        shell="/bin/bash"
        if ! grep -q "^%${groupname}" /etc/sudoers; then
            cp /etc/sudoers /etc/sudoers.bkp
            echo "%${groupname} ALL=(ALL) ALL" >> /etc/sudoers
            sudoers_changed=true
            log_message "Sudo access granted for group '$groupname'"
        fi
    elif [[ "$username" == "$ADMIN_USER" ]]; then
        shell="/bin/bash"
        if ! grep -q "^${username}" /etc/sudoers; then
            cp /etc/sudoers /etc/sudoers.bkp
            echo "${username} ALL=(ALL) ALL" >> /etc/sudoers
            sudoers_changed=true
            log_message "Sudo access granted for user '$username'"
        fi
    fi

    # Обновляем shell пользователя если нужно
    if [[ "$shell" != "$DEFAULT_SHELL" ]]; then
        if usermod -s "$shell" "$username" 2>/dev/null; then
            log_message "Shell changed to $shell for user '$username'"
        fi
    fi

    # Валидация sudoers файла если были изменения
    if [[ "$sudoers_changed" == true ]]; then
        if ! visudo -c >/dev/null 2>&1; then
            log_message "Error: Invalid sudoers file, restoring backup"
            cp /etc/sudoers.bkp /etc/sudoers
            return 1
        fi
    fi
    
    echo "$shell"
}

process_single_user() {
    local username="$1" groupname="$2"
    
    log_message "Processing: Username: $username, Group: $groupname"
    
    if create_group "$groupname" && create_user "$username" "$groupname" "$DEFAULT_SHELL"; then
        local final_shell
        final_shell=$(setup_sudo_access "$username" "$groupname")
        # Если shell изменился, обновляем пользователя
        if [[ "$final_shell" != "$DEFAULT_SHELL" ]]; then
            usermod -s "$final_shell" "$username" 2>/dev/null || true
        fi
        echo "Success: User '$username' with group '$groupname' completed"
    else
        echo "Error: Failed to process user '$username'" >&2
        return 1
    fi
}

process_file_users() {
    local user_file="$1"
    local success_count=0 error_count=0
    
    if [[ ! -f "$user_file" ]] || [[ ! -r "$user_file" ]]; then
        log_message "Error: User file '$user_file' not found or not readable"
        return 1
    fi

    if [[ ! -s "$user_file" ]]; then
        log_message "Error: User file '$user_file' is empty"
        return 1
    fi

    log_message "Processing users from file: $user_file"
    
    # Сохраняем и восстанавливаем IFS
    local old_ifs="$IFS"
    
    while IFS=$' \t' read -r username groupname || [[ -n "$username" ]]; do
        # Пропускаем пустые строки и комментарии
        [[ -z "$username" || "$username" =~ ^# ]] && continue
        
        if process_single_user "$username" "$groupname"; then
            ((success_count++))
        else
            ((error_count++))
        fi
    done < "$user_file"
    
    IFS="$old_ifs"
    
    log_message "File processing completed: $success_count success, $error_count errors"
    return "$error_count"
}

interactive_mode() {
    echo "Interactive User Creation"
    echo "========================="
    
    while true; do
        read -rp "Enter username (or 'quit' to exit): " username
        [[ "$username" == "quit" ]] && break
        [[ -z "$username" ]] && continue
        
        read -rp "Enter groupname: " groupname
        [[ -z "$groupname" ]] && continue
        
        process_single_user "$username" "$groupname"
        echo
    done
}

show_usage() {
    cat << EOF
Usage: $0 [USERNAME GROUPNAME]
       $0 (with no arguments for interactive mode or file processing)

If USERNAME and GROUPNAME are provided, creates a single user.
If no arguments, processes $USER_FILE or enters interactive mode.

Examples:
  $0 john developers    # Create single user
  $0                   # Process file or interactive mode
EOF
}

# Основная логика
main() {
    local username groupname
    
    case $# in
        0)
            if [[ -f "$USER_FILE" ]]; then
                process_file_users "$USER_FILE"
            else
                interactive_mode
            fi
            ;;
        2)
            username="$1"
            groupname="$2"
            process_single_user "$username" "$groupname"
            ;;
        *)
            show_usage
            exit 1
            ;;
    esac
}

# Обработка сигналов для cleanup
trap 'log_message "Script interrupted"; exit 130' INT TERM

# Запуск основной функции
main "$@"