# E-commerce website project using Django

Work in progress!

Will feature Docker, Celery, Redis, PostgreSQL and DRF.

Release 0.3.4 features:
- main listing-related models
- generic list and detail CBVs
- flatpages and maintenance mode

Release 0.4.7 features:
- pagination and filtering for listing sections
- updating seller info page
- creating/updating pages for listings
- inline form for adding pictures to car listings
- some custom form validation
- codebase typing, documentation and cleanup

Release 0.7.5 features:
- separated app structure
- authorization via django-allauth & google
- user groups and rights
- newsletter emailing and sms messaging via celery
- celery using redis message broker
- redis running in docker-compose
- using local postgresql db on ubuntu
