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
To describe the SQL instance:
```
gcloud sql instances describe beautynow
```
To perform migrations on the GCP SQL instance:
* The database host must be **localhost** or **127.0.0.1**. It must somehow be set temporarily to this value. But, in **settings.py**, make sure to keep the **cloudsql** URL intact. This is the value that must be present for the API to be able to connect to the database.
