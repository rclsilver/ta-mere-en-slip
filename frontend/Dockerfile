# development stage (lts-alpine)
FROM node:12.16.0-alpine3.11 as devel-stage
WORKDIR /app
COPY package*.json /app/
COPY . /app/
RUN mkdir /tmp/node_modules && ln -s /tmp/node_modules /app/node_modules

# build stage (lts-alpine)
FROM node:12.16.0-alpine3.11 as build-stage
WORKDIR /app
COPY package*.json /app/
RUN npm install
COPY . /app/
RUN npm run build

# production stage (stable-alpine)
FROM nginx:1.16.1-alpine as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
