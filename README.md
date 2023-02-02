# GitHub Utilites

API for interacting with GitHub

## Create a personal access token

I created a classic token with the `repo` scope and all its children checked.

https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token

## Required Values

These are the values you'll need to pass in the query string to for a repo.

```
http://127.0.0.1:5000/?token={Personal Access Token}&owner={Repo Owner}&repo={Repo Name}
```

`token`: GitHub Personal Access Token for the user you want the forked repo associated with

`owner`: GitHub owner of the repository you want to fork

`repo`: GitHub repository you want to fork

## Configure App Environment

### Install virtualenv

```
pip install virtualenv
```

### Create new virtual environment

```
virtualenv venv
```

### Start virtual environment

#### Mac/Linux 

```
source venv/bin/activate
```

#### Windows

```
venv\Scripts\activate
```

### Install Modules

Once you've started your virtual environment run:

```
pip install -r requirements.txt
```

## Start the app

```
python main.py
```