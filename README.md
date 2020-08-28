# snapshare
photo sharing webapp - pythonDjango 

libraries reqd:
    django-rest-framework
    pillow (for image CRUS in django)
    django-cors-headers (For cross origin to work with react)
    django-cors-middleware  (For cross origin to work with react)
    psycopg2 (For django + postgres connection)
    dj-database-url (For django + postgres conn on Heroku server)
    boto3 and django-storages (For django + AWS S3)

Deployed on :
    Heroku:
    1) Webapp(source code from github)
    2) Postgres DB on Heroku default postgres db

    AWS S3 bucket :
    3) Images and Mediafiles uploaded (because heroku deletes entire file system in each deployment)

(DO NOT hardcode IAM access keys, instead use environment variables)

How to deploy on Heorku + AWS S3 bucket (for media files)
    1) Heroku
    app -> Deploy -> connect to github repo -> deploy

    2) Create new Heroku postgres DB from
    app -> Resources -> create new postgres DB
    Heroku CLI - heroku run python manage.py makemigrations and migrate and createsuperuser

    3) Heroku CLI set AWS S3 bucketname and IAM credentials as environment variables 
    Heroku CLI -> heroku config:set <key>:<value>             