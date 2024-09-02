import re
import requests
import good_guard as GoodGuard


def parse_telegram_link(link: str) -> str | None:
	match = re.search(r't\.me/([a-zA-Z0-9_]+)', link)
	if match:
		username = match.group(1)
		return f'@{username}'
	return None

async def check_bot_in_chat_or_group(link: str) -> bool:
  url = f"https://api.telegram.org/bot{GoodGuard.TELEGRAM_API_TOKEN}/getChatMember"
  chat_id = parse_telegram_link(link)
  params = {
		"chat_id": chat_id,
		"user_id": GoodGuard.BOT_ID
	}
  response = requests.get(url, params=params)
  data = response.json()
  return data.get("ok") and data.get("result", {}).get("status") in ["member", "creator", "administrator"]

async def download_file(file_path: str) -> bytes:
	url = f"https://api.telegram.org/file/bot{GoodGuard.TELEGRAM_API_TOKEN}/{file_path}"
	response = requests.get(url)
	return response.content

async def get_chat_file_path(name: str) -> str | None:
	url = f"https://api.telegram.org/bot{GoodGuard.TELEGRAM_API_TOKEN}/getChat"
	params = {
		"chat_id": name
	}
	response = requests.get(url, params=params)
	data = response.json()
	if not data.get("ok"):
		return None
	file_id = data.get("result", {}).get("photo", {}).get("small_file_id")
	if not file_id:
		return None
	url = f"https://api.telegram.org/bot{GoodGuard.TELEGRAM_API_TOKEN}/getFile"
	params = {
		"file_id": file_id
	}
	response = requests.get(url, params=params)
	data = response.json()
	if not data.get("ok"):
		return None
	return data.get("result", {}).get("file_path")