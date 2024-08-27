FROM node as vite-app

WORKDIR /app
COPY . .

RUN ["npm", "i", "--legacy-peer-deps"]
RUN ["npm", "run", "build"]

FROM nginx:alpine

WORKDIR /usr/share/nginx/

RUN rm -rf html
RUN mkdir html

WORKDIR /

COPY --chmod=765 --from=vite-app ./app/dist /usr/share/nginx/html

EXPOSE 3000

ENTRYPOINT ["nginx", "-g", "daemon off;"]