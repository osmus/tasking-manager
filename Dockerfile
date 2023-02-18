FROM node:18

WORKDIR /usr/src/app/frontend

## Dependencies Install
COPY package.json package-lock.json* ./
# --legacy-peer-deps is a temporary hack to make `react-placeholder` install with react v18
RUN npm ci --legacy-peer-deps && npm cache clean --force

COPY frontend .
COPY tasking-manager.env ..

ARG TM_APP_BASE_URL
ARG TM_APP_API_URL
ARG TM_CLIENT_ID
ARG TM_CLIENT_SECRET
ARG TM_REDIRECT_URI
ARG TM_SCOPE
ARG PD_CONSUMER_KEY
ARG PD_CONSUMER_SECRET

## Build
RUN npm run build && mkdir -p /usr/share/nginx/html && mv /usr/src/app/frontend/build/** /usr/share/nginx/html
