FROM python:3.11-slim  

WORKDIR /codebase

COPY requirements.txt /codebase  
RUN pip install --upgrade pip && pip install -r requirements.txt  

COPY . /codebase  

CMD [ "python", "main.py" ]
