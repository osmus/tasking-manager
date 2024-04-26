FROM python:3.7-alpine as base
WORKDIR /usr/src/app

# not sure if we actually need to list all the args
ARG TM_APP_API_VERSION
ARG TM_ORG_NAME
ARG TM_ORG_CODE
ARG TM_ORG_LOGO
ARG TM_ORG_URL
ARG TM_ORG_PRIVACY_POLICY_URL
ARG TM_ORG_TWITTER
ARG TM_ORG_FB
ARG TM_ORG_INSTAGRAM
ARG TM_ORG_YOUTUBE
ARG TM_ORG_GITHUB
ARG TM_DB
ARG TM_DB_URL
ARG ENABLE_PROXYFIX
ARG TM_EMAIL_CONTACT_ADDRESS
ARG TM_EMAIL_FROM_ADDRESS
ARG TM_ENV
ARG TM_LOG_LEVEL
ARG TM_SECRET
ARG TM_SMTP_HOST
ARG TM_SMTP_PASSWORD
ARG TM_SMTP_USER
ARG TZ
ARG TM_CLIENT_ID
ARG TM_CLIENT_SECRET
ARG POSTGRES_DB
ARG POSTGRES_USER
ARG POSTGRES_PASSWORD
ARG OSM_SERVER_URL
ARG OSM_NOMINATIM_SERVER_URL
ARG OSM_REGISTER_URL
ARG PD_SERVER_URL
ARG PD_CLIENT_ID
ARG PD_CLIENT_SECRET
ARG TM_APP_API_URL
ARG TM_APP_BASE_URL
ARG TM_REDIRECT_URI
ARG TM_SCOPE
ARG TM_USER_STATS_API_URL
ARG TM_HOMEPAGE_STATS_API_URL
ARG TM_DEFAULT_CHANGESET_COMMENT
ARG TM_DEFAULT_LOCALE

## BUILD
FROM base as builder

# Setup backend build dependencies
RUN apk update && apk add postgresql-dev gcc g++ python3-dev musl-dev libffi-dev geos-dev proj-util proj-dev make

# Setup backend Python dependencies
COPY requirements.txt .
COPY cython_constraint.txt /tmp/
RUN PIP_CONSTRAINT=/tmp/cython_constraint.txt pip install --prefix=/install --no-warn-script-location -r requirements.txt

## DEPLOY
FROM base

# Setup backend runtime dependencies
RUN apk update && apk add postgresql-libs geos proj-util

COPY --from=builder /install /usr/local
COPY . .

ENV TZ UTC # Fix timezone (do not change - see issue #3638)
EXPOSE 5000

ENV WORKERS 3
ENV THREADS 3
ENV TIMEOUT 179

CMD ["sh", "-c", "exec gunicorn -b 0.0.0.0:5000 --worker-class gevent --workers $WORKERS --threads $THREADS --timeout $TIMEOUT manage:application"]
