# Используем официальный образ Nginx
FROM nginx:latest

# Указываем рабочую директорию для копирования файлов
WORKDIR /usr/share/nginx/html

# Копируем билд проекта Vue.js (предварительно выполните npm run build)
COPY ./dist /usr/share/nginx/html

# Удаляем стандартный конфиг Nginx и добавляем свой
RUN rm /etc/nginx/conf.d/default.conf
COPY ./nginx.conf /etc/nginx/conf.d/default.conf

# Создаём директорию для SSL-сертификатов
RUN mkdir -p /etc/nginx/ssl

# Генерируем самоподписанный сертификат
RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/nginx/ssl/private.key \
    -out /etc/nginx/ssl/certificate.crt \
    -subj "/C=US/ST=Test/L=Test/O=Test/OU=Test/CN=localhost"

# Открываем порты для HTTP и HTTPS
EXPOSE 80 443

# Запускаем Nginx
CMD ["nginx", "-g", "daemon off;"]
