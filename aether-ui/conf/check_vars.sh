#!/bin/bash
set -e

# Production specific functions

check_variable() {
  if [ -n "$1" ];
  then
    echo "$2 in Ordnung!"
  else
    echo "Missing $2"
    exit -1
  fi
}

check_kernel() {
  # check if KERNEL env variables were set
  check_variable $AETHER_KERNEL_URL   "KERNEL url"
  check_variable $AETHER_KERNEL_TOKEN "KERNEL token"
}

check_kernel
check_variable $ADMIN_PASSWORD "ADMIN password"
