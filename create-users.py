#!/usr/bin/python3

# INET4031
# Ram
# Data Created
# 3/23/26

# Importing required modules:
import os  # os -> used to execute system-level commands (like adduser, passwd)
import re  # re -> used for pattern matching (checking for comments in input)
import sys # sys -> used to read input from stdin (input redirection)


def main():
    for line in sys.stdin:

	# Check if the line starts with '#' which indicates a comment line
	# These lines should be ignored by the script
        match = re.match("^#",line)

	# Remove whitespace and split the line into fields using ':' delimiter
	# Expected format: username:password:lastname:firstname:groups
        fields = line.strip().split(':')

	# Skip processing if:
	# - The line is a comment (starts with '#')
	# - The line does not contain exactly 5 fields (invalid format)
	# This prevents errors and ensures only valid user entries are processed
        if match or len(fields) != 5:
            continue

	# Extract user information from the parsed fields
	# username -> login name
	# password -> account password
	# gecos -> formatted full name field stored in /etc/passwd
        username = fields[0]
        password = fields[1]
        gecos = "%s %s,,," % (fields[3],fields[2])

	# Split the group field by commas to allow multiple group assignments
        groups = fields[4].split(',')

	# Informational output showing user creation process
        print("==> Creating account for %s..." % (username))
	# Build command to create a new user account without password
	# --gecos sets user information (name, etc.)
        cmd = "/usr/sbin/adduser --disabled-password --gecos '%s' %s" % (gecos,username)


        os.system(cmd)
	# Informational output showing password setup
        print("==> Setting the password for %s..." % (username))
	# Command to set user password using echo and passwd
	# It pipes the password twice (required by passwd command)
        cmd = "/bin/echo -ne '%s\n%s' | /usr/bin/sudo /usr/bin/passwd %s" % (password,password,username)

        #print(cmd)
        os.system(cmd)
	# Loop through each group assigned to the user
        for group in groups:
	# Check if group is not '-' (which means no group assignment)
	# If valid, assign user to the group using adduser command
            if group != '-':
                print("==> Assigning %s to the %s group..." % (username,group))
                cmd = "/usr/sbin/adduser %s %s" % (username,group)
                #print(cmd)
                os.system(cmd)

if __name__ == '__main__':
    main()
