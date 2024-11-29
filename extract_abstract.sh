#!/usr/bin/env bash
set -eu

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

if ! command -v pdftk &> /dev/null; then
  echo "PDFtk was not found. Installing."
  sudo apt-get update
  sudo apt-get install pdftk
fi

pdftk "${SCRIPT_DIR}/main.pdf" cat 3 output "${SCRIPT_DIR}/abstract.pdf"
