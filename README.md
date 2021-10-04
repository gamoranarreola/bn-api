# Google Cloud
To deploy the app:
```
gcloud app deploy
```
To tail the logs:
```
gcloud app logs tail -s bn-api
```
To connect to the SQL instance:
```
export GOOGLE_CLOUD_PROJECT=beauty-now-313716
export USE_CLOUD_SQL_AUTH_PROXY=true
./cloud_sql_proxy -instances="beauty-now-313716:us-west2:beautynow"=tcp:5432
```
To create a secret from a file:
```
gcloud secrets create django_settings --data-file .env
```
