import os

template_path = "CryptoAPI/alembic.ini.template"
output_path = "CryptoAPI/alembic.ini"

try:
    with open(template_path, "r") as template_file:
        template_content = template_file.read()

    output_content = template_content.format(
        POSTGRES_USER=os.environ.get("POSTGRES_USER"),
        POSTGRES_PASSWORD=os.environ.get("POSTGRES_PASSWORD"),
        POSTGRES_DB=os.environ.get("POSTGRES_DB")
    )

    with open(output_path, "w") as output_file:
        output_file.write(output_content)

    print(f"{output_path} generated successfully.")
except FileNotFoundError as e:
    print(f"Error: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")