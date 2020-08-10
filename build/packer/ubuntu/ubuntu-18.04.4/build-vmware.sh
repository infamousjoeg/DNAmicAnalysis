#!/bin/bash
set -eo pipefail

packer build -only=vmware-iso ubuntu-18.04.4-minimal.json