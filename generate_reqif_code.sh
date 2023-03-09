#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

xjc -d "$SCRIPT_DIR/src/main/java/" -p edu.nd.crc.safa.utilities.reqif.datatypes -mark-generated -b "$SCRIPT_DIR/custom-binding.xjb" "$SCRIPT_DIR/reqif.xsd"
