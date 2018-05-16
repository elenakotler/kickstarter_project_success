import flask
from flask import request
import pickle
import numpy as np


# Initialize the app

app = flask.Flask(__name__)

with open("final_model_logreg_top10.pkl","rb") as f:
    logr = pickle.load(f)

with open("scaler.pkl","rb") as f:
    scaler = pickle.load(f)

hr_features = ['Project Goal ($)      ',
               'Project Length (days) ',
               'Number of Reward Tiers',
               'Is this your first project?',
              'Staff Pick',
               'publishing',
               'journalism',
               'music',
               'crafts',
               'food',
               'technology',
               'photography',
               'theater',
               'dance',
               'games',
               'comics',
               'art',
               'fashion',
               'design',
               'film & video']

@app.route("/", methods=["POST", "GET"])
def predict():


    print(request.args)

    x_input = []
    x_input_sp = []
    for i in range(len(hr_features[:3])):
        # f_value = 0
        f_value = int(
            request.args.get(hr_features[i], "0")
            )
        x_input.append(f_value)
        x_input_sp.append(f_value)

    # fill in 'first project' values
    key_val = hr_features[3]
    first_project = int(request.args.get(key_val,"1"))
    x_input.append(first_project)
    x_input_sp.append(first_project)

    # fill in 'staff pick as No' values
    x_input.append(0)
    x_input_sp.append(1)

    # add zeros for all categories
    x_input.extend([0] * len(hr_features[5:]))
    x_input_sp.extend([0] * len(hr_features[5:]))

    # get category input and update the input values
    cat = request.args.get('category','publishing')
    cat_idx = hr_features.index(cat)
    x_input[cat_idx] = 1
    x_input_sp[cat_idx] = 1

    x_input_std = scaler.transform(np.array(x_input).reshape((1, -1)))
    x_input_sp_std = scaler.transform(np.array(x_input_sp).reshape((1, -1)))

    pred_probs = logr.predict_proba(x_input_std)
    pred_probs_sp = logr.predict_proba(x_input_sp_std)

    success_proba = str(round(pred_probs[0][1] * 100, 1)) + "%"
    success_proba_sp = str(round(pred_probs_sp[0][1] * 100, 1)) + "%"


    # Return a response with a json in it
    # flask has a quick function for that that takes a dict
    return flask.render_template('predictor.html',
    feature_names=hr_features,
    categories = hr_features[5:],
    x_input=x_input,
    prediction=success_proba,
    prediction_sp =success_proba_sp
    )


# Start the server, continuously listen to requests.
# We'll have a running web app!

# For local development:
app.run(debug=True)

# For public web serving:
# app.run(host='0.0.0.0')
