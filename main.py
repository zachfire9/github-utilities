import json
import os
import requests

from flask import Flask, jsonify, render_template, redirect, request, session
from flask_session import Session

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['GITHUB_CLIENT_ID'] = os.environ.get('GITHUB_CLIENT_ID')
app.config['GITHUB_CLIENT_SECRET'] = os.environ.get('GITHUB_CLIENT_SECRET')

app.secret_key = app.config['SECRET_KEY']
app.config['SESSION_TYPE'] = 'filesystem'
sess = Session()
sess.init_app(app)

@app.route('/')
def index():
    if session.get('access_token'):
        return redirect("/fork", code=302)

    return render_template('index.html')

@app.route('/callback')
def callback():
    args = request.args

    endpoint = f"https://github.com/login/oauth/access_token?client_id={app.config['GITHUB_CLIENT_ID']}&client_secret={app.config['GITHUB_CLIENT_SECRET']}&code={args.get('code')}"
    print(endpoint)
    headers = {
        'Accept': 'application/json',
    }
    response = requests.post(endpoint, headers=headers)
    if response.status_code != 200:
        return jsonify(error=response.reason), response.status_code
    response_dict = json.loads(response.text)

    session['access_token'] = response_dict.get('access_token')

    return redirect("/fork", code=302)

@app.route('/fork', methods = ['GET'])
def fork_repo_form():
    if not session.get('access_token'):
        return redirect("/", code=302)

    return render_template('fork.html')

@app.route('/fork', methods = ['POST'])
def fork_repo():
    """https://docs.github.com/en/rest/repos/forks?apiVersion=2022-11-28#create-a-fork"""
    if not request.form.get('owner'):
        return jsonify(error='Missing "owner" value in the form data'), 400
    owner = request.form['owner']

    if not request.form.get('repo'):
        return jsonify(error='Missing "repo" value in the form data'), 400
    repo = request.form['repo']

    if not session.get('access_token'):
        return jsonify(error='Missing "access_token" value for this user'), 400
    access_token = session['access_token']
    
    endpoint = f'https://api.github.com/repos/{owner}/{repo}/forks'
    headers = {
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28',
        'Authorization': f'Bearer {access_token}',
    }
    payload = {
        'name': f'{repo}',
        'default_branch_only': True
    }
    response = requests.post(endpoint, headers=headers, data=json.dumps(payload))

    response_dict = json.loads(response.text)
    if response_dict.get('message'):
        return jsonify(error=response_dict['message']), response.status_code

    return jsonify(message='Repo successfully forked'), 200

if __name__ == '__main__':
    app.run()