python .\manage.py dumpdata core.tag core.comment core.snapshot core.location core.userimage core.UserProfile > fixtures/Sample_Data.json

python .\manage.py loaddata .\fixtures\Sample_Data.json