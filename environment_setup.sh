#!/usr/bin/env bash
PROJECT_DIR=`dirname $0`


echo "Using $PROJECT_DIR as work dir..."

cd $PROJECT_DIR
mkdir -p ./scripts/output

echo "Downloading miniconda for python environment..."

wget -c https://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh

echo "Installing miniconda to $PROJECT_DIR/miniconda/"
rm ~/.cache/pip -r
bash ./Miniconda2-latest-Linux-x86_64.sh -b -f -p $PROJECT_DIR/miniconda/
export PATH=$PROJECT_DIR/miniconda/bin:$PATH

echo "Installing requirement package..."
rm ~/.cache/pip -r
pip install -U pip
pip install -r ./scripts/src/requirements.txt --force-reinstall

echo "Installing NLTK datasets..."
python -m nltk.downloader -d $PROJECT_DIR/nltk_data punkt
python -m nltk.downloader -d $PROJECT_DIR/nltk_data averaged_perceptron_tagger
python -m nltk.downloader -d $PROJECT_DIR/nltk_data universal_tagset
python -m nltk.downloader -d $PROJECT_DIR/nltk_data wordnet
python -m nltk.downloader -d $PROJECT_DIR/nltk_data wordnet_ic

touch $PROJECT_DIR/.installation_done

echo "Installation finished, you can run this project code now."
echo "Any question please contact me."