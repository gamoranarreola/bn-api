# Google Cloud
To deploy the app:
```
gcloud app deploy
```
To tail the logs:
```
gcloud app logs tail -s bn-api
```
To create a secret from a file:
```
gcloud secrets create django_settings --data-file .env
```
To describe the SQL instance:
```
gcloud sql instances describe beautynow
```
## Running Migrations on GCP
To connect to the SQL instance, run the following in a terminal window:
```
./cloud_sql_proxy -instances="beauty-now-313716:us-west2:beautynow"=tcp:5432
```
Then, in a new window, set the following environment variables:
```
export GOOGLE_CLOUD_PROJECT=beauty-now-313716
export USE_CLOUD_SQL_AUTH_PROXY=true
```
To perform migrations on the GCP SQL instance, set **DATABASE['default']['HOST']** to **'localhost'** temporarily in **settings.py**. Once this is set, you can run migrations using (don't forget to undo this temporary change to the **settings.py** file):
```
python3.8 manage.py migrate
```
