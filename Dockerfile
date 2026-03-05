# 1. Start with a lightweight Python base image
FROM python:3.10-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy your requirements and install dependencies
# (We create a dummy requirements.txt if you don't have one yet)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt || true

# 4. Copy the rest of your application code
COPY . .

# 5. The command to run your bot
CMD ["python", "trading_bot.py"]