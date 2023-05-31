FROM node:18 as build

# there's maybe some issue with docker cacheing so run everything uncached
ADD "https://www.random.org/cgi-bin/randbyte?nbytes=10&format=h" skipcache

WORKDIR /usr/src/app/frontend
COPY frontend .
# create env file if it doesn't exist
RUN touch tasking-manager.env
COPY example.env tasking-manager.en[v] ../

## SETUP
# --legacy-peer-deps is a temporary hack to make `react-placeholder` install with react v18
RUN npm install --legacy-peer-deps

ARG TM_APP_BASE_URL
ARG TM_APP_API_URL
ARG TM_CLIENT_ID
ARG TM_CLIENT_SECRET
ARG TM_REDIRECT_URI
ARG TM_SCOPE
ARG PD_CONSUMER_KEY
ARG PD_CONSUMER_SECRET

# SERVE
RUN npm run build

FROM nginx:stable-alpine
COPY --from=build /usr/src/app/frontend/build /usr/share/nginx/html
COPY --from=build /usr/src/app/frontend/nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
