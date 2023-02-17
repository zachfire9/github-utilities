# GitHub Utilites

App for interacting with GitHub

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

Set local environment variables (make sure to update) every time you start your environment:

```
env $(cat .env | xargs)
```

#### Windows

```
venv\Scripts\activate
```

Set local environment variables (make sure to update) every time you start your environment:

```
.\bin\env.ps1
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