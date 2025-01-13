FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

RUN npm run build

FROM nginx:latest

WORKDIR /usr/share/nginx/html

COPY --from=builder /app/dist/spa /usr/share/nginx/html

RUN rm /etc/nginx/conf.d/default.conf
COPY --from=builder /app/nginx.conf /etc/nginx/conf.d/default.conf

RUN mkdir -p /etc/nginx/ssl
RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/nginx/ssl/private.key \
    -out /etc/nginx/ssl/certificate.crt \
    -subj "/C=US/ST=Test/L=Test/O=Test/OU=Test/CN=localhost"

EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]
