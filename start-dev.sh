#!/bin/bash

# Функция для поиска URL туннеля в строке
find_tunnel_url() {
    local line="$1"
    if [[ $line =~ https://[a-zA-Z0-9.-]+\.trycloudflare\.com ]]; then
        echo "${BASH_REMATCH[0]}"
        return 0
    fi
    return 1
}

# Шаг 1: Запустить cloudflared tunnel
echo "Запуск cloudflared tunnel..."
tunnel_log="cloudflared_log.txt"

# Запуск cloudflared и запись логов в файл
cloudflared tunnel --url http://localhost:3000 > "$tunnel_log" 2>&1 &
CLOUDFLARED_PID=$!

# Ожидание пока найдется URL туннеля
tunnel_url=""
while IFS= read -r line; do
    echo "$line"
    if find_tunnel_url "$line"; then
        tunnel_url="${BASH_REMATCH[0]}"
        echo "Найден URL туннеля: $tunnel_url"
        break
    fi
done < <(tail -f "$tunnel_log")

# Если не удалось найти URL туннеля, завершаем скрипт с ошибкой
if [ -z "$tunnel_url" ]; then
    echo "Не удалось найти URL туннеля."
    kill $CLOUDFLARED_PID
    exit 1
fi

# Убедимся, что файл закрыт перед удалением
sleep 1

# Попытаемся удалить файл несколько раз, если возникнут ошибки
for _ in {1..5}; do
    if rm "$tunnel_log" 2>/dev/null; then
        break
    else
        echo "Не удалось удалить файл $tunnel_log, повторная попытка через 1 секунду..."
        sleep 1
    fi
done

# Шаг 2: Записать URL туннеля в .env файл
dotenv_path=".env"
webapp_url_key="WEBAPP_URL"

# Перезаписываем значение WEBAPP_URL
if grep -q "^$webapp_url_key=" "$dotenv_path"; then
    sed -i "s|^$webapp_url_key=.*|$webapp_url_key=$tunnel_url|" "$dotenv_path"
else
    echo "$webapp_url_key=$tunnel_url" >> "$dotenv_path"
fi
echo "URL туннеля записан в $dotenv_path как $webapp_url_key"

# Шаг 3: Запустить docker-compose
echo "Запуск docker-compose..."
docker compose -f docker-compose.dev.yaml up --build

# Чтение вывода команды docker-compose
if [ $? -ne 0 ]; then
    echo "Ошибка при запуске docker-compose"
    exit 1
fi
