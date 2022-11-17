### Create dependencies
```
pipenv run pip3 freeze > requirements.txt
```

### Build and run the container locally using Docker
```
docker build . --tag gcr.io/heat-stress-scale/hss-web-app
PORT=8080 && docker run -p 9090:${PORT} -e PORT=${PORT} gcr.io/heat-stress-scale/hss-web-app
```
You should be able to access the application at this URL: `http://127.0.0.1:9090/`

### Push the container image to Container Registry and deploy
```
pipenv run pip3 freeze > requirements.txt
gcloud builds submit --tag gcr.io/heat-stress-scale/hss-web-app  --project=heat-stress-scale
gcloud run deploy hss-web-app --image gcr.io/heat-stress-scale/hss-web-app  --project=heat-stress-scale --platform managed
```

