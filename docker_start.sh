#!/bin/sh
if [ "$CREATE_DATABASE" ] ; then
    python -m brprev_commerce.initialize_db
fi
gunicorn -w 2 -b 0.0.0.0:4000 'brprev_commerce.app:create_app()'
