### application git
https://github.com/FedericoTartarini/tool-risk-scale-football-nsw


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

