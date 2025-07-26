#create python image
FROM python:3.10-slim
# set working directory
WORKDIR /app
# copy requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Copy all project files
COPY . .
# EXPOSE FLASK PORT
EXPOSE 5001
# RUN FLASK APP
CMD ["python","app.py"]
