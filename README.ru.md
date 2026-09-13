# Экосистема Telegram Mini App для управления VPN

<p align="center">
  <strong>Комплексная экосистема управления VPN на базе Telegram Mini App</strong>
</p>

<p align="center">
  <a href="README.md"><b>English</b></a> | <a href="README.ru.md"><b>Русский</b></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D" alt="Vue.js 3" />
  <img src="https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white" alt="TypeScript" />
  <img src="https://img.shields.io/badge/Quasar-1976D2?style=for-the-badge&logo=quasar&logoColor=white" alt="Quasar" />
  <img src="https://img.shields.io/badge/Aiogram_3-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white" alt="Aiogram 3" />
  <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL" />
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker" />
  <img src="https://img.shields.io/badge/SQLAlchemy_2.0-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white" alt="SQLAlchemy 2.0" />
</p>

---

## 📖 О проекте

**Telegram Mini App VPN Ecosystem** — это self-hosted платформа для продажи и управления VPN-подписками, разработанная специально для работы внутри экосистемы Telegram. Проект объединяет высокопроизводительный бэкенд на **FastAPI**, нативное клиентское приложение (TMA) на **Vue 3 / Quasar** и асинхронного фонового демона на **Aiogram 3**.

Система полностью автоматизирует жизненный цикл пользователя:
1. **Бесшовная авторизация Zero-Trust исключительно через Telegram**: Веб-приложение изолировано от прямого открытия во внешних браузерах. При запуске Quasar boot-плагин извлекает криптографические данные Telegram WebApp `initData`. Попытка открыть ссылку вне Telegram блокируется страницей `403 Access Denied` (`/not-from-telegram`).
2. **Автоматический биллинг и оплата**: Прием платежей через шлюз ЮMoney (IPN-вебхуки) с обязательной криптографической валидацией подписи SHA-1.
3. **Мгновенная выдача VLESS/Xray ключей**: Интеграция с нодами **3X-UI** через REST API для автоматического создания клиентов, лимитов трафика и получения конфигураций.
4. **Уведомления о статусе подписки**: Воркер на Aiogram 3 заранее напоминает пользователям о продлении подписки (за 3 дня, за 1 день и в момент окончания).

---

## 🏛️ Архитектура системы

```mermaid
flowchart TD
    subgraph Telegram_Ecosystem["Клиент и Экосистема Telegram"]
        TG_USER["Пользователь Telegram"]
        TG_BOT["Telegram-бот (Воркер Aiogram 3)"]
    end

    subgraph Edge["Шлюз и Обратный прокси"]
        NGINX["Nginx Reverse Proxy & SSL Termination\n(:80 / :443)"]
    end

    subgraph Frontend["Клиентское приложение"]
        SPA["Telegram Mini App (TMA)\nVue 3 + Quasar + TypeScript + vue-tg"]
        AUTH_GUARD{"Запуск внутри\nTelegram (есть initData)?"}
        DENY_PAGE["403 Access Denied\n(/not-from-telegram)"]
    end

    subgraph Backend_Core["Бэкенд Core API (FastAPI)"]
        AUTH_EP["Слой роутеров\n(/api/v1/*)"]
        SVC_LAYER["Слой сервисов\n(Auth, Payment, Panel, Subscription)"]
        REPO_LAYER["Слой репозиториев\n(Async SQLAlchemy 2.0)"]
    end

    subgraph Persistence["База данных"]
        PG[("PostgreSQL 15")]
        PGADMIN["pgAdmin 4 (Панель управления)"]
    end

    subgraph External_Services["Внешние сервисы и интеграции"]
        XUI["Ноды 3X-UI\n(API создания VLESS / Xray конфигураций)"]
        YOOMONEY["Шлюз ЮMoney\n(HTTP IPN Webhook)"]
    end

    %% Трафик клиента и проверка окружения
    TG_USER -->|1. Нажатие кнопки WebApp в боте| NGINX
    NGINX -->|Отдает статику SPA| SPA
    SPA --> AUTH_GUARD
    AUTH_GUARD -- "Нет (Обычный браузер)" --> DENY_PAGE
    AUTH_GUARD -- "Да (Telegram клиент)" -->|2. Обмен initData на Bearer JWT| NGINX
    NGINX -->|3. Проксирование /api/v1/| AUTH_EP

    %% Внутренняя логика API
    AUTH_EP --> SVC_LAYER
    SVC_LAYER --> REPO_LAYER
    REPO_LAYER <-->|Асинхронный пул соединений (asyncpg)| PG

    %% Внешние интеграции
    SVC_LAYER -->|Создание VLESS-клиента и получение ключей| XUI
    YOOMONEY -->|Вебхук оплаты POST /payment/check/yoomoney| NGINX

    %% Бот и фоновый шедулер
    TG_BOT <-->|Запрос истекающих подписок| PG
    TG_BOT -->|Отправка уведомлений и инлайн-кнопок| TG_USER
```

---

## 🧱 Обзор компонентов системы

### 1. Клиентское приложение Telegram WebApp (`tgbot_client`)
* **Стек**: [Vue 3](https://vuejs.org/) (Composition API, `<script setup>`), [Quasar Framework v2](https://quasar.dev/) (сборщик Vite) и [TypeScript](https://www.typescriptlang.org/).
* **Защита контекста запуска (Telegram-Only Guard)**:
  * На этапе инициализации приложения (`src/boot/auth.ts`) вызывается `useWebApp().initData`.
  * Если приложение запущено вне контекста Telegram (в стандартном браузере), происходит принудительный редирект на `/not-from-telegram` с отображением экрана `403 Access Denied`.
* **Адаптация под Telegram UX**: Библиотека [`vue-tg`](https://github.com/deptyped/vue-tg) автоматически синхронизирует тему приложения с цветовой палитрой Telegram пользователя (`tg-theme-bg-color`, `tg-theme-text-color`), управляет нативными кнопками MainButton / BackButton и обеспечивает виброотклик (Haptic Feedback).
* **Анимации и визуал**: Библиотека [Lottie](https://airbnb.io/lottie/) для статусных экранов, успешных платежей и пустых состояний.
* **Функциональность**:
  * Копирование конфигураций в один клик и быстрый импорт по диплинкам (`hiddify://`, `v2rayNG`).
  * Пополнение баланса с моментальным расчетом тарифов.
  * Выбор серверов с визуальными индикаторами стран и статусом доступности.
  * Интерактивные инструкции по настройке под iOS, Android, macOS и Windows.

### 2. Сервис Core API (`tgbot_server`)
* **Стек**: [FastAPI](https://fastapi.tiangolo.com/), запущенный на `uvicorn` в полностью асинхронном режиме.
* **Слоистая архитектура (Clean Layered Architecture)**:
  * **Роутеры (`app/api/v1/endpoints/`)**: Валидация входных данных, маршрутизация, внедрение зависимостей.
  * **Сервисы (`app/services/`)**: Бизнес-логика (обработка платежей, синхронизация подписок, работа с панелями).
  * **Репозитории (`app/repository/`)**: Изоляция слоя доступа к данным по интерфейсам (`interfaces.py`).
  * **Схемы (`app/schema/`)**: Строгая валидация и типизация через **Pydantic v2**.
* **База данных**: **SQLAlchemy 2.0** (`AsyncSession`), пул соединений через драйвер `asyncpg`. Управление версиями структуры базы через миграции **Alembic**.

### 3. Фоновый воркер и бот (`tgbot_main`)
* **Стек**: [Aiogram 3.x](https://github.com/aiogram/aiogram) с асинхронным циклом обработки событий.
* **Запуск WebApp и шедулер**:
  * Обрабатывает команду `/start` и отправляет инлайн-кнопку с `WebAppInfo` для запуска Mini App.
  * Фоновый шедулер непрерывно проверяет базу данных на наличие истекающих подписок.
  * Рассылает уведомления: **за 3 дня**, **за 1 день** и **при истечении срока**.
  * Автоматически деактивирует завершенные подписки в базе и отправляет пользователю кнопку для быстрого продления.

### 4. Внешние интеграции
* **Платежный шлюз ЮMoney**:
  * Формирование ссылок на оплату с перенаправлением обратно в Mini App.
  * Обработчик мгновенных уведомлений (IPN Webhook).
  * Проверка целостности и подлинности: вычисление SHA-1 HMAC с использованием секретного ключа `YOOMONEY_SECRET`.
* **Интеграция с узлами 3X-UI**:
  * Автоматическое управление клиентами на удаленных серверах через REST API.
  * Генерация UUID клиентов, установка лимитов трафика, создание инбаундов и получение готовых VLESS-конфигов.

---

## 🛡️ Безопасность и надежность

| Область | Реализация |
| :--- | :--- |
| **Изоляция Telegram-контекста** | Клиентский роутер блокирует запуск приложения без параметров `initData`, предотвращая сканирование интерфейса поисковыми ботами и доступ извне. |
| **Валидация `initData`** | Бэкенд проверяет криптографическую подпись входящей строки через HMAC-SHA256 с использованием секретного ключа бота. Подделка пользовательских параметров невозможна. |
| **Авторизация по JWT** | После верификации сессии генерируется Bearer JWT токен с ограниченным временем жизни, проверяемый в зависимостях FastAPI (`get_current_active_user`). |
| **Безопасность вебхуков** | Уведомления от ЮMoney проверяются по формуле SHA-1 хэша от параметров (`notification_type`, `operation_id`, `amount`, `currency`, `datetime`, `sender`, `codepro`, `secret`, `label`). |
| **Надежность БД** | Полная транзакционность (ACID), асинхронный пул соединений `asyncpg` и версионируемые миграции структуры через Alembic. |
| **Контейнеризация** | Multi-stage Dockerfile для фронтенда и бэкенда, изоляция сервисов во внутренней сети Docker, проверка готовности зависимостей (`wait-for-it.sh`). |
| **Nginx и SSL** | Обязательная поддержка HTTPS/TLS, отдача предсжатой статики SPA, заголовки безопасности и блокировка скрытых системных файлов. |

---

## 📡 Обзор API-эндпоинтов

Интерактивная документация Swagger доступна по адресу `/api/docs`.

| Группа эндпоинтов | Базовый путь | Назначение |
| :--- | :--- | :--- |
| **Авторизация** | `/api/v1/auth` | Обмен проверенных данных Telegram `initData` на сессионный Bearer JWT токен (`POST /login`). |
| **Профиль пользователя** | `/api/v1/user` | Получение информации о пользователе, текущего баланса и аватара в Base64. |
| **Подписки** | `/api/v1/subscription` | Получение активных подписок пользователя с группировкой по серверам. |
| **Управление узлами 3X-UI** | `/api/v1/panel` | Запрос данных клиента по UUID/email, добавление новых VLESS-клиентов и принудительная синхронизация. |
| **Платежи и баланс** | `/api/v1/payment` | Создание ссылки на оплату в ЮMoney (`/new/yoomoney`), прием вебхуков (`/check/yoomoney`) и история транзакций. |
| **Серверы** | `/api/v1/server` | Список активных серверов, локаций и доступных тарифов. |

---

## 📂 Структура репозитория

```
TelegramMiniAppBot/
├── docker-compose.yml       # Сборка и оркестрация контейнеров
├── nginx.conf               # Reverse proxy, SSL и маршрутизация SPA
├── .env.template            # Шаблон переменных окружения
├── README.md                # Документация на английском языке
├── README.ru.md             # Документация на русском языке
├── tgbot_client/            # Фронтенд Single Page App (Vue 3 / Quasar / Vite)
│   ├── src/
│   │   ├── api/             # Типизированные клиенты API и перехватчики Axios
│   │   ├── boot/            # Плагины Quasar (Auth guard для Telegram, Axios)
│   │   ├── components/      # UI-компоненты (списки подписок, платежи, карточки)
│   │   ├── pages/           # Страницы (подключение, биллинг, выбор тарифа)
│   │   │   └── errors/      # NotFromTelegram.vue (экран 403 Access Denied)
│   │   └── router/          # Маршрутизация и навигационные гарды
│   └── Dockerfile           # Многоэтапная сборка Node/Nginx
├── tgbot_server/            # Основной сервис API (FastAPI)
│   ├── alembic/             # Миграции базы данных
│   ├── app/
│   │   ├── api/v1/          # Эндпоинты (/auth, /user, /subscription, /payment и др.)
│   │   ├── core/            # Конфигурация, сессии БД, безопасность, зависимости
│   │   ├── model/           # Декларативные модели SQLAlchemy
│   │   ├── repository/      # Репозитории доступа к базе данных
│   │   ├── schema/          # Схемы валидации Pydantic v2
│   │   ├── services/        # Бизнес-логика, интеграции с 3X-UI и ЮMoney
│   │   └── utils/           # Валидаторы подписей и вспомогательные функции
│   └── Dockerfile           # Контейнер Python 3.11 slim
└── tgbot_main/              # Telegram-бот и фоновый воркер (Aiogram 3)
    ├── bot/
    │   ├── handlers/        # Команды (/start с кнопкой запуска WebApp)
    │   ├── services/        # Фоновый шедулер и логика напоминаний
    │   └── repositories/    # Асинхронные запросы к базе подписок
    └── Dockerfile           # Контейнер Python-демона
```

---

## 🚀 Руководство по развертыванию

> [!IMPORTANT]
> **Требование к HTTPS**: Telegram Mini Apps работают **исключительно по протоколу HTTPS** с валидным SSL-сертификатом. При локальной разработке для проброса домена можно использовать **Cloudflare Tunnel**, **ngrok** или **localtunnel**.

### Шаг 1: Создание бота и настройка WebApp в BotFather
1. Откройте [@BotFather](https://t.me/BotFather) в Telegram и выполните `/newbot`, чтобы создать бота. Сохраните полученный **Bot Token**.
2. Привяжите веб-приложение:
   * **Способ А (Кнопка меню / Menu Button)**: Введите команду `/setmenubutton`, выберите созданного бота и укажите ваш публичный HTTPS-домен (например, `https://vpn.yourdomain.com`).
   * **Способ Б (Создание отдельного Mini App через `/newapp`)**: Создайте Mini App шорткат, привязав его к боту и указав URL.

### Шаг 2: Настройка переменных окружения
Скопируйте шаблон `.env.template` в `.env`:

```bash
cp .env.template .env
```

Заполните конфигурационные параметры:

```env
# База данных PostgreSQL
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_secure_password
POSTGRES_DB=vpn_service_db

# Параметры подключения к БД (для FastAPI и Бота)
DB_HOST=postgres
DB_PORT=5432
DB_NAME=vpn_service_db
DB_USER=postgres
DB_PASSWORD=your_secure_password

# Панель управления pgAdmin
PGADMIN_DEFAULT_EMAIL=admin@example.com
PGADMIN_DEFAULT_PASSWORD=admin_password

# Данные Telegram-бота
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
WEBAPP_URL=https://vpn.yourdomain.com

# Безопасность и JWT
JWT_SECRET_KEY=сгенерируйте_случайный_64_символьный_ключ
ACCESS_TOKEN_EXPIRE_MINUTES=43200

# Интеграция с ЮMoney
YOOMONEY_WALLET=41001XXXXXXXXXXX
YOOMONEY_SECRET=секрет_для_уведомлений_из_настроек_юmoney
PAY_SUCCESS_URL=https://t.me/YourBotUsername/app

# Настройки подключения к узлам 3X-UI
TLS_VERIFY=False
```

### Шаг 3: Настройка SSL-сертификатов
Разместите действующие SSL-сертификаты для Nginx в директории `./ssl`:
* `./ssl/certificate.crt`
* `./ssl/private.key`

*(При использовании Let's Encrypt / Certbot примонтируйте директорию с сертификатами в `docker-compose.yml` в сервис `frontend`).*

### Шаг 4: Запуск в Docker Compose
Запустите весь стек контейнеров одной командой:

```bash
docker compose up -d --build
```

Порядок инициализации сервисов:
1. **`postgres`**: Запускает базу данных на порту `5432`.
2. **`fastapi`**: Скрипт `wait-for-it.sh` ожидает доступности БД, автоматически накатывает миграции `alembic upgrade head` и стартует API на порту `8000`.
3. **`bot`**: Подключается к БД и активирует обработчики событий и фоновый шедулер напоминаний.
4. **`frontend`**: Собирает Quasar SPA и запускает Nginx на портах `80` и `443`.
5. **`pgadmin`**: Доступен по адресу `http://localhost:5050` для управления базой через веб-интерфейс.

### Шаг 5: Проверка работоспособности
1. Перейдите в вашего бота в Telegram и отправьте команду `/start`.
2. Нажмите кнопку **«Запустить приложение 🚀»** (или системную кнопку Menu в левом нижнем углу).
3. Приложение откроется внутри Telegram, автоматически верифицирует пользователя через `initData` и загрузит личный кабинет.
4. *(Опционально)* Попробуйте открыть `https://vpn.yourdomain.com` напрямую в обычном браузере (Chrome / Firefox) — вы увидите экран блокировки `403 Access Denied`, подтверждающий изоляцию приложения.

---

## 📄 Лицензия
Проект распространяется под открытой лицензией **MIT**.
