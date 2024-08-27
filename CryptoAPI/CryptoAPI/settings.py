import os

# Путь к шаблону и конечному файлу
template_path = "alembic.ini.template"
output_path = "alembic.ini"

# Чтение шаблона
with open(template_path, "r") as template_file:
    template_content = template_file.read()

# Подстановка переменных окружения
output_content = template_content.format(
    POSTGRES_USER=os.environ.get("POSTGRES_USER"),
    POSTGRES_PASSWORD=os.environ.get("POSTGRES_PASSWORD"),
    POSTGRES_DB=os.environ.get("POSTGRES_DB")
)

# Запись сгенерированного файла
with open(output_path, "w") as output_file:
    output_file.write(output_content)

print(f"{output_path} generated successfully.")