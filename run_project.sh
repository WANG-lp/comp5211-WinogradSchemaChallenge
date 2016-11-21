#!/usr/bin/env bash
PROJECT_DIR=`dirname $0`

export PATH=$PROJECT_DIR/miniconda/bin:$PATH

echo "Checking requirement package installation..."
if [ ! -f $PROJECT_DIR/.installation_done ]; then

bash ./environment_setup.sh

fi

echo "Running code..."

python ./scripts/src/Main.py "$@"