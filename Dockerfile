FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt --root-user-action=ignore
COPY . .
CMD ["python", "bot.py"]
