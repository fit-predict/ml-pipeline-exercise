#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: fmillan
"""

from flask import Flask, request, jsonify, send_file
import joblib
import os
import pymongo
import numpy as np
from json2html import *

THRESHOLD = 80

assert(THRESHOLD >=0 & THRESHOLD <= 100)

client = pymongo.MongoClient("mongodb://localhost:27017")
mongodb = client["mlpipeline"]
collection = mongodb["lowerback"]

scaler = joblib.load('1_scaler.pkl')
p_transformer = joblib.load('2_transformer.pkl')
clf = joblib.load('3_best_clf.pkl')

app = Flask(__name__)


def transform_predict(new_sample):
    scaled_sample = scaler.transform(new_sample)
    trasformed_sample = p_transformer.transform(scaled_sample)
    res50 = clf.predict(trasformed_sample)[0]
    proba = clf.predict_proba(trasformed_sample)[:,1][0] * 100
    res = 1 if proba >= THRESHOLD else 0
    return res, proba, res50


def check_values(arr):
    res = []
    for v in arr:
        try:
            float(v)
            res.append(float(v))
        except:
            res.append(np.nan)
    return res


@app.route("/")
def index():
    with open('index.html', 'r') as content_file:
        content = content_file.read()
    return content


@app.route("/gimme/<file>")
def send(file):
    lf = ["ml_pip_adv_slides.pdf", "nothing_to_see_here.gif", "Dockerfile", "requirements.txt", "Spine.html",
          "Spine_key.html", "Spine_missing_values_prediction.html", "supervisord.conf", "app.py"]
    if file in lf:
        return send_file(file)


@app.route("/api/1/show")
def api_show():
    try:
        res = [c for c in collection.find({}, {'_id': 0}).sort([("_id", pymongo.DESCENDING)])]
        d = {}
        for i in range(len(res)):
            d[str(i)] = res[i]

        return dict(d)
    except Exception as e:
        return str(e)


@app.route("/api/1/predict", methods=['GET', 'POST'])
def api_predict():
    if request.method == 'POST':
        labels = ["pelvic_incidence", "pelvic_tilt", "lumbar_lordosis_angle", "pelvic_radius",
                  "degree_spondylolisthesis",
                  "pelvic_slope", "Direct_tilt", "thoracic_slope", "cervical_tilt", "sacrum_angle", "scoliosis_slope"]
        content = request.json

        try:
            values = []
            for l in labels:
                values.append(float(content[l]))
        except Exception as e:
            return jsonify({"ERROR!": "Tag " + str(e) + " not found!"})

        values = check_values(values)

        new_sample = np.array([values])

        try:
            res, proba, _ = transform_predict(new_sample)

            json_sample = dict(zip(labels, [v for v in new_sample.astype(str)][0]))

            json_sample["RESULT"] = str(res)
            json_sample["PROBABILITY"] = str(proba)

            collection.insert_one(dict(json_sample))

            return json_sample
        except Exception as e:
            return jsonify({"ERROR!": str(e)})

    elif request.method == 'GET':
        with open('ERROR.html', 'r') as content_file:
            content = content_file.read()
        return content


@app.route(
    "/predict")  # http://localhost:8080/predict?pelvic_incidence=63.027818&pelvic_tilt=22.552586&lumbar_lordosis_angle=39.609117&pelvic_radius=98.672917&degree_spondylolisthesis=-0.254400&pelvic_slope=0.744503&Direct_tilt=12.5661&thoracic_slope=14.5386&cervical_tilt=15.30468&sacrum_angle=-28.658501&scoliosis_slope=43.5123
def predict_get():
    labels = ["pelvic_incidence", "pelvic_tilt", "lumbar_lordosis_angle", "pelvic_radius", "degree_spondylolisthesis",
              "pelvic_slope", "Direct_tilt", "thoracic_slope", "cervical_tilt", "sacrum_angle", "scoliosis_slope"]

    pelvic_incidence = request.args.get('pelvic_incidence')
    pelvic_tilt = request.args.get('pelvic_tilt')
    lumbar_lordosis_angle = request.args.get('lumbar_lordosis_angle')
    sacral_slope = request.args.get('sacral_slope')
    pelvic_radius = request.args.get('pelvic_radius')
    degree_spondylolisthesis = request.args.get('degree_spondylolisthesis')
    pelvic_slope = request.args.get('pelvic_slope')
    Direct_tilt = request.args.get('Direct_tilt')
    thoracic_slope = request.args.get('thoracic_slope')
    cervical_tilt = request.args.get('cervical_tilt')
    sacrum_angle = request.args.get('sacrum_angle')
    scoliosis_slope = request.args.get('scoliosis_slope')

    values = [pelvic_incidence, pelvic_tilt, lumbar_lordosis_angle, pelvic_radius, degree_spondylolisthesis,
              pelvic_slope, Direct_tilt, thoracic_slope, cervical_tilt, sacrum_angle, scoliosis_slope]

    values = check_values(values)

    new_sample = np.array([values])

    try:
        res, proba, _ = transform_predict(new_sample)

        json_sample = dict(zip(labels, [v for v in new_sample.astype(str)][0]))

        json_sample["RESULT"] = str(res)
        json_sample["PROBABILITY"] = str(proba)

        collection.insert_one(json_sample)

        label = "NORMAL" if res == 0 else "ABNORMAL"
    except Exception as e:
        return str(e)

    return '''<h1>RESULT</h1>
              The lower back pain is: <strong>{}</strong>.</br> 
              (Probability of having an abnormal spin is {:2f}%).\nTHRESHOLD: {}%.'''.format(label, proba, THRESHOLD)


@app.route("/backup")
def backup():
    try:
        os.system("mongodump --db mlpipeline --gzip --out .")
        bckp = "mlpipeline/lowerback.bson.gz"
    except Exception as e:
        return str(e)
    return send_file(bckp, as_attachment=True)


@app.route("/show")
def show():
    try:
        return json2html.convert([c for c in collection.find({}, {'_id': 0}).sort([("_id", pymongo.DESCENDING)])])
    except Exception as e:
        return str(e)


@app.route("/last")
def last():
    try:
        return json2html.convert(
            [c for c in collection.find({}, {'_id': 0}).sort([("_id", pymongo.DESCENDING)]).limit(1)])
    except Exception as e:
        return str(e)


@app.route('/get/<n>')
def getn(n):
    try:
        return json2html.convert([c for c in collection.find({}, {'_id': 0}).sort([("_id", pymongo.DESCENDING)]).limit(
            int(n))])
    except Exception as e:
        return str(e)


@app.route('/form', methods=['GET', 'POST'])  # allow both GET and POST requests
def form_example():
    if request.method == 'POST':  # this block is only entered when the form is submitted
        labels = ["pelvic_incidence", "pelvic_tilt", "lumbar_lordosis_angle", "pelvic_radius",
                  "degree_spondylolisthesis",
                  "pelvic_slope", "Direct_tilt", "thoracic_slope", "cervical_tilt", "sacrum_angle", "scoliosis_slope"]

        pelvic_incidence = request.form['pelvic_incidence']
        pelvic_tilt = request.form['pelvic_tilt']
        lumbar_lordosis_angle = request.form['lumbar_lordosis_angle']
        sacral_slope = request.form['sacral_slope']
        pelvic_radius = request.form['pelvic_radius']
        degree_spondylolisthesis = request.form['degree_spondylolisthesis']
        pelvic_slope = request.form['pelvic_slope']
        Direct_tilt = request.form['Direct_tilt']
        thoracic_slope = request.form['thoracic_slope']
        cervical_tilt = request.form['cervical_tilt']
        sacrum_angle = request.form['sacrum_angle']
        scoliosis_slope = request.form['scoliosis_slope']

        values = [pelvic_incidence, pelvic_tilt, lumbar_lordosis_angle, pelvic_radius, degree_spondylolisthesis,
                  pelvic_slope, Direct_tilt, thoracic_slope, cervical_tilt, sacrum_angle, scoliosis_slope]

        values = check_values(values)

        new_sample = np.array([values])

        try:
            res, proba, _ = transform_predict(new_sample)

            json_sample = dict(zip(labels, [v for v in new_sample.astype(str)][0]))

            json_sample["RESULT"] = str(res)
            json_sample["PROBABILITY"] = str(proba)

            collection.insert_one(json_sample)

            label = "NORMAL" if res == 0 else "ABNORMAL"
        except Exception as e:
            return str(e)

        return '''<h1>RESULT</h1>
              The lower back pain is: <strong>{}</strong>.</br> 
              (Probability of having an abnormal spin is {:2f}%).\nTHRESHOLD: {}%.'''.format(label, proba, THRESHOLD)

    with open('form.html', 'r') as form_file:
        html_form = form_file.read()
    return html_form


if __name__ == "__main__":
    print("Lower back pain webservice started!")
    app.run(host='0.0.0.0', port=8080)
