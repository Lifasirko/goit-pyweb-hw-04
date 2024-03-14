# Використовуйте офіційний образ Python як базовий
FROM python:3.10

# Встановіть робочий каталог у контейнері
WORKDIR /app

# Копіюйте вміст поточної директорії в робочу директорію контейнера
COPY . .

# Встановіть будь-які необхідні пакети, вказані в requirements.txt
#RUN pip install --no-cache-dir -r requirements.txt

# Вкажіть команду для запуску додатку
CMD ["python", "main.py"]

# docker build -t goit-pyweb-hw-04 .
# docker run -v C:\Users\MikeK\PycharmProjects\in_process\goit-pyweb-hw-04\front-init\front-init\storage:/app/front-init/front-init/storage -p 8000:8000 --name site goit-pyweb-hw-04