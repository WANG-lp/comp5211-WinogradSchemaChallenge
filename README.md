# comp5211-WinogradSchemaChallenge

## Installation

Full installation of this project code will need around `600MB disk space`, please ensure you have enough disk quota.

Or you can put this project code to `/tmp/<You CSD account>/`, we can use more than `30GB` space in this directory.


There is a script can help you to install requirement packages such as `NLTK` and `sklearn` before you running the project code:

```bash
$ cd DIR_OF_THIS_PROJECT_CODE
$ bash ./environment_setup.sh
```

## Running Project code

After installed requirement packages. You can use this command to run the project code:

```bash
$ bash ./run_project.sh  INPUT_DATA_SET(e.g. ./datasets/WSCollection.xml)
```

for example: 
```bash
$ bash ./run_project.sh ./datasets/WSCollection.xml
```

The results will been printed on screen and also been stored to `./scripts/output/answer-output.txt`


