### application git
https://github.com/FedericoTartarini/tool-risk-scale-football-nsw


## install
```
sudo apt install libcurl4-openssl-dev libssl-dev
pip install -r requirements.txt
```

# run
# local
gunicorn main:app --reload

# docker
docker build . -t tool-risk-scale

docker run --rm --name tool-risk-scale -e PORT=8080 -p 8080:8080 tool-risk-scale

# access docker shell
docker exec -it tool-risk-scale bash

# check exists
docker image ls

# gcloud

gcloud builds submit --tag gcr.io/pfolio-deploy-1/tool-risk-scale

gcloud run deploy --image gcr.io/pfolio-deploy-1/tool-risk-scale --platform managed --port=8080

```







### Create dependencies
```
pipenv run pip3 freeze > requirements.txt
```

### Build and run the container locally using Docker
```
docker build . --tag gcr.io/cloud-run-install/tool-risk-scale-football-nsw PORT=8080 && docker run -p 9090:${PORT} -e PORT=${PORT} gcr.io/cloud-run-install/tool-risk-scale-football-nsw
```
You should be able to access the application at this URL: `http://127.0.0.1:9090/`

### Push the container image to Container Registry and deploy
```
pipenv run pip3 freeze > requirements.txt
gcloud builds submit --tag gcr.io/cloud-run-install/tool-risk-scale-football-nsw  --project=cloud-run-install
gcloud run deploy extreme-heat-tool --image gcr.io/cloud-run-install/tool-risk-scale-football-nsw  --project=cloud-run-install --platform managed
```

