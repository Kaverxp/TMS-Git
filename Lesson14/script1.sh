#!/bin/bash

if [ "$(id -u)" != 0 ]; then
echo "root permissions required" >&2
exit 1
fi

#Variables
file=/var/users
shell=/sbin/nologin
oldIFS=$IFS

#Functions
create_user(){
IFS=$oldIFS
groupadd $groupname
# Создаем пользователя с домашней директорией
useradd -m -g $groupname $username -s $shell
passwd -d $username 2>/dev/null
echo "Done! User: $username, Group: $groupname"
}

#check parameters
if [ ! -z $2 ];then
   username=$1
   groupname=$2
   echo Username: $username   Group:  $groupname
   create_user
elif [ -f $file ]; then
   IFS=$'\n'
   for line in $(cat /var/users)
   do
     username=$(echo $line | cut -d' ' -f1)
     groupname=$(echo $line | cut -d' ' -f2)
     echo Username: $username Group: $groupname
     create_user
   done
else 
   # Если оба параметра отсутствуют
   echo "Welcome!"
   read -p "Print username: " username
   read -p "Print groupname: " groupname
   create_user
fi

# Sudoers
if [ "$groupname" = it ] || [ "$groupname" = security ];
 then
    if ! grep "%$groupname" /etc/sudoers; then
    cp /etc/sudoers{,.bkp}
    echo '%'$groupname' ALL=(ALL) ALL' >> /etc/sudoers
    fi
    shell=/bin/bash
elif [ "$username" = admin ]; then
	if ! grep "$username" /etc/sudoers; then
    	cp /etc/sudoers{,.bkp}
    	echo $username' ALL=(ALL) ALL' >> /etc/sudoers
    	fi
    shell=/bin/bash
fi