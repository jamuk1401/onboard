# Onboard Telematics

<!--- These are examples. See https://shields.io for others or to customize this set of shields. You might want to include dependencies, project status and licence info here --->

![GitHub repo size](https://img.shields.io/github/repo-size/jamuk1401/onboard.git/README.md)
![GitHub contributors](https://img.shields.io/github/contributors/jamuk1401/onboard.git/README.md)
![GitHub stars](https://img.shields.io/github/stars/jamuk1401/onboard.git/README.md?style=social)
![GitHub forks](https://img.shields.io/github/forks/jamuk1401/onboard.git/README.md?style=social)
![Twitter Follow](https://img.shields.io/twitter/follow/jam1401?style=social)

This project contains the following components

`./onboard.py ` Some Pyspark code for extracting, transforming and delivering vehicle data from a large compressed file.

`./data` Example data

`./ui` A flutter app for displaying the data exposed by pyspark

`./architecture` An architecture framework

## Prerequisites

The code was developed on macos with python running in a virtual env. Homebrew was used to install most of the dependencies

```
brew install scala
brew install scala
brew install apache-spark
brew install python
brew install pyenv
brew install py4j
```

The data once processed by pyspark was published to a local mqtt broker The following installs this component and starts it

```
brew install mosquitto
brew reinstall mosquitto
```

The graphical UI requires the installation of [flutter](https://flutter.dev/) T

## Using Onboard

To run the pyspark

`python ./onboad.py`

note this expects the file data/allVehicles.csv.gz to exist which is too big for git so need to be created from the source file.

he output can also be displayed on the command line using the following command

`mosquitto_sub -h localhost  -p 1883 --topic ortus/oboard/+ --remove-retained` and example of the output is shown [here](https://drive.google.com/file/d/1dGo21req2URmTSca-qbTJ8QyGpbdj3pB/view?usp=sharing)

The flutter UI can be run as a Mac App or a Web app. It can also be simply built and deployed for IOS and Android on a fully cloud deployed solution. The output can be seen [here](https://drive.google.com/file/d/1dI8rDulktmakJAeIiAaY951zfPCAzUZ0/view?usp=sharing)
