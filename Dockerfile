FROM node:18 as build

WORKDIR /usr/src/app/frontend
COPY frontend .
COPY tasking-manager.env ..

## SETUP
# --legacy-peer-deps is a temporary hack to make `react-placeholder` install with react v18
RUN npm install --legacy-peer-deps

ARG TM_APP_API_URL=https://tasks-backend.openstreetmap.us/api
ARG TM_CONSUMER_KEY=94tWwKDLwq6xlzEcR9OHWDz8XeHT7tNrPz7jjcS5
ARG TM_CONSUMER_SECRET=wNQxVpkPogwVSZfjd4aUjcW03iPYU0WV0mcVtSKI

# SERVE
RUN npm run build

FROM nginx:stable-alpine
COPY --from=build /usr/src/app/frontend/build /usr/share/nginx/html
COPY --from=build /nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
