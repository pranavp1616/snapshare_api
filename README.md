# snapshare
photo sharing webapp - pythonDjango 

libraries reqd:
    django-rest-framework
    pillow (for image CRUS in django)
    django-cors-headers (For cross origin to work with react)
    django-cors-middleware  (For cross origin to work with react)
    psycopg2 (For django + postgres connection)
    dj-database-url (For django + postgres conn on Heroku server)


Deployed on :
    Heroku:
    1) Webapp(source code from github)
    2) Postgres DB on Heroku default postgres db

    AWS S3 bucket :
    3) Images and Mediafiles uploaded (because heroku deletes entire file system in each deployment)

(DO NOT hardcode IAM access keys, instead use environment variables)