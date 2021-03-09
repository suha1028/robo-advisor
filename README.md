# Robo Advisor

## Software needed
You should already have: Anaconda 3.7+, Python 3.7+, and Pip

## Installation
To begin, fork this remote repository and then clone/download it onto your own desktop. Then, please naviagte to command-line/terminal:

```sh
cd ~/Desktop/robo-advisor
```
Then, use Anaconda to create a virtual environment called "stocks-env":

```sh
conda create -n stocks-env python=3.8
conda activate stocks-env
```
Then, install the required packages specified in the "requirements.txt" file you created:

```sh
pip install -r requirements.txt
```
## Setup
Go to https://www.alphavantage.co and follow the prompts to obtain an API key.

Then, in the root directory of your local repository, please create a new file titled ".env" and then update the contents of this file to show your API key by typing:

```sh
ALPHAVANTAGE_API_KEY="abc123"
```
## Running the app
From the virtual environment, run the app through command-line:

```sh
python app/robo_advisor.py
```
