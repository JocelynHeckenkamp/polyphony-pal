
FROM node:lts-alpine as builder

WORKDIR /app

COPY . .

RUN npm i
RUN npm run build

FROM nginx:alpine-slim

COPY --from=builder /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
#Use the below line for injecting ENV into client browser (might need after using auth for user accounts), also uncomment chmod line
#COPY inject_env.sh /usr/share/nginx/html/inject_env.sh

EXPOSE 80

WORKDIR /usr/share/nginx/html

RUN apk add --no-cache bash

#RUN chmod +x inject_env.sh


# ENTRYPOINT ["/bin/bash", "-c", "/usr/share/nginx/html/inject_env.sh && nginx -g \"daemon off;\""]