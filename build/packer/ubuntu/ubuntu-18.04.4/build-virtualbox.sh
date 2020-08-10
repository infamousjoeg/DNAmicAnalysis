#!/bin/bash
set -eo pipefail

packer build -only=virtualbox-iso ubuntu-18.04.4-minimal.json