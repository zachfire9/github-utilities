import json
import os
import requests

from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def fork_repo():
    """https://docs.github.com/en/rest/repos/forks?apiVersion=2022-11-28#create-a-fork"""
    args = request.args

    if not args.get('owner'):
        return jsonify(error='Missing "owner" value in the querystring'), 400
    owner = args['owner']

    if not args.get('repo'):
        return jsonify(error='Missing "repo" value in the querystring'), 400
    repo = args['repo']

    if not args.get('token'):
        return jsonify(error='Missing "token" value in the querystring'), 400
    token = args['token']
    
    endpoint = f'https://api.github.com/repos/{owner}/{repo}/forks'
    headers = {
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28',
        'Authorization': f'Bearer {token}',
    }
    payload = {
        'name':f'{repo}',
        'default_branch_only':True
    }
    response = requests.post(endpoint, headers=headers, data=json.dumps(payload))

    response_dict = json.loads(response.text)
    if response_dict.get('message'):
        return jsonify(error=response_dict['message']), response.status_code

    return jsonify(message='Repo successfully forked'), 200

if __name__ == '__main__':
    app.run()