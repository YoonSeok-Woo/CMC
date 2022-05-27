# build stage
FROM node:lts-alpine as build-stage

WORKDIR /app
COPY package*.json ./
ADD . .
RUN npm install
COPY . .
RUN npm run build


FROM nginx:stable-alpine as production-stage
COPY  ./nginx/default.conf /etc/nginx/conf.d/default.conf
COPY --from=build-stage /app/dist /etc/nginx/html


EXPOSE 80 443
