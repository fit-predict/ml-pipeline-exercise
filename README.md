# Lower Back Pain Prediction Web Service

- [Original dataset](https://www.kaggle.com/sammy123/lower-back-pain-symptoms-dataset).

- Read the proposed exercise [here](https://github.com/fit-predict/ml-pipeline-exercise/blob/master/ml_pip_adv_slides.pdf).

  ## Use cases

  ### REST API

- Send `JSON` values using a `REST API`  [(link)](http://localhost:8080/api/1/predict).

  - Normal sample:

    - ```json
      {"pelvic_incidence": "61.73487533",
      "pelvic_tilt": "17.11431203",
      "lumbar_lordosis_angle": "46.89999999",
      "pelvic_radius": "120.9201997",
      "degree_spondylolisthesis": "3.087725997",
      "pelvic_slope": "0.455056082",
      "Direct_tilt": "8.866",
      "thoracic_slope": "14.9831",
      "cervical_tilt": "8.27541",
      "sacrum_angle": "-0.48876",
      "scoliosis_slope": "24.9564"}
      ```

  - Abnormal sample:

    - ```json
      {"pelvic_incidence": "57.52235608",
      "pelvic_tilt": "33.64707522",
      "lumbar_lordosis_angle": "50.90985841",
      "pelvic_radius": "140.9817119",
      "degree_spondylolisthesis": "148.7537109",
      "pelvic_slope": "0.597457003",
      "Direct_tilt": "21.5943",
      "thoracic_slope": "7.5666",
      "cervical_tilt": "7.81812",
      "sacrum_angle": "-27.570464",
      "scoliosis_slope": "17.8768"}
      ```

- Get a `JSON` with all the values using a `REST API`[(link)](http://localhost:8080/api/1/show). 

  ### Web requests

- Parametric [links](http://localhost:8080/predict?pelvic_incidence=63.027818&pelvic_tilt=22.552586&lumbar_lordosis_angle=39.609117&pelvic_radius=98.672917&degree_spondylolisthesis=-0.254400&pelvic_slope=0.744503&Direct_tilt=12.5661&thoracic_slope=14.5386&cervical_tilt=15.30468&sacrum_angle=-28.658501&scoliosis_slope=43.5123).

- Predict using a web form [(link)](http://localhost:8080/form).

- Show all the predictions made [(link)](http://localhost:8080/show).

- Get the last `n` predictions [(link)](http://localhost:8080/get/3).

- Show the last prediction [(link)](http://localhost:8080/last).

- Backup the database [(link)](http://localhost:8080/backup).

## Summary

- This solution was made using:

  - Docker
    - MongoDB as scratch image.
  - Flask.
  - Sklearn.
  - A Logistic Regression model.
  - Additional software:
    - Flask
    - joblib
    - pymongo
    - numpy
    - json2html

  ---

## Relevant files

- [Slides](https://github.com/fit-predict/ml-pipeline-exercise/blob/master/ml_pip_adv_slides.pdf)

- Jupyter Notebooks:

  - [Exercise](https://github.com/fit-predict/ml-pipeline-exercise/blob/master/Spine.ipynb)
  - [Solution](https://github.com/fit-predict/ml-pipeline-exercise/blob/master/Spine_key.ipynb)
  - [Missing values imputation](https://github.com/fit-predict/ml-pipeline-exercise/blob/master/Spine_missing_values_prediction.ipynb)

- [Dockerfile](https://github.com/fit-predict/ml-pipeline-exercise/blob/master/Dockerfile)

- [Requirements](https://github.com/fit-predict/ml-pipeline-exercise/blob/master/requirements.txt)

- [Supervisor's configuration](https://github.com/fit-predict/ml-pipeline-exercise/blob/master/supervisord.conf)

- [Application's code](https://github.com/fit-predict/ml-pipeline-exercise/blob/master/app.py)



## Build the image

```$ docker build --tag=mlpipeline . ```

## Create a container

```$ docker run --name mlpip -p 8080:8080 -p 27017:27017 mlpipeline```

## Authors

- Dr. Macarena Beigier-Bompadre
  - https://www.linkedin.com/in/macarena-beigier-bompadre/
- Fernando Millán
  - https://www.linkedin.com/in/fmiyca/
