import datetime
import json

import requests
from flask import render_template, redirect, request

from app import app
import appConfig 


MINING_NODE_ADDRESS=appConfig.getAppConfig("MINING_NODE_ADDRESS") 
#print(MINING_NODE_ADDRESS)
 


posts = []


def fetch_posts():
    """
    Function to fetch the chain from a blockchain node, parse the
    data and store it locally.
    """
    get_chain_address = "{}/chain".format(MINING_NODE_ADDRESS)
    response = requests.get(get_chain_address)
    if response.status_code == 200:
        content = []
        chain = json.loads(response.content)
        for block in chain["chain"]:
            for tx in block["transactions"]:
                tx["index"] = block["index"]
                tx["hash"] = block["previous_hash"]
                content.append(tx)

        global posts
        posts = sorted(content, key=lambda k: k['timestamp'],
                       reverse=True)


@app.route('/')
def index():
    fetch_posts()
    return render_template('index.html',
                           title='Secure System For Person Recognition Using Blockchain & DeepLearning',
                           posts=posts,
                           node_address=MINING_NODE_ADDRESS,
                           readable_time=timestamp_to_string)


@app.route('/submit', methods=['POST'])
def submit_textarea():
    """
    Endpoint to create a new transaction via our application.
    """
    detectedPersonEntryDetails = request.form["detectedPersonEntryDetails"]
    detectedPersonDetails = request.form["detectedPersonDetails"]

    post_object = {
        'detectedPersonDetails': detectedPersonDetails,
        'detectedPersonEntryDetails': detectedPersonEntryDetails,
    }
    print("post object: ",post_object)

    # Submit a transaction
    new_tx_address = "{}/new_transaction".format(MINING_NODE_ADDRESS)

    requests.post(new_tx_address,
                  json=post_object,
                  headers={'Content-type': 'application/json'})

    return redirect('/')


def timestamp_to_string(epoch_time):
    return datetime.datetime.fromtimestamp(epoch_time).strftime('%H:%M')
