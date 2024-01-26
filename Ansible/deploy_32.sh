#!/usr/bin/env bash

# Deploy only 32 bits k3s cluster and applications

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

cd "$SCRIPT_DIR" && ansible-playbook -i "$SCRIPT_DIR/inventory/hosts_32.ini" "$SCRIPT_DIR/playbooks/32/deploy_all.yml"
