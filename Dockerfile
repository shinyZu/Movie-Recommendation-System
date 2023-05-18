# # Use an official Python runtime as a parent image
# FROM python:3

# # Set the working directory to /app
# WORKDIR /app

# # Copy the requirements file into the container at /app
# COPY requirements.txt .

# # Install any needed packages specified in requirements.txt
# RUN pip install --trusted-host pypi.python.org -r requirements.txt

# # Copy the rest of the application code into the container at /app
# COPY . .

# # Expose port 5000 to the outside world
# EXPOSE 5000

# # Define environment variable
# ENV FLASK_APP=app.py

# # Run app.py when the container launches
# CMD ["flask", "run", "--host=0.0.0.0"]


FROM python:3
# WORKDIR /app
# COPY requirements.txt .
# # RUN pip install --trusted-host pypi.python.org -r requirements.txt
# RUN pip install -r requirements.txt
# COPY . .
# EXPOSE 5000
# ENV FLASK_APP=app.py
# EXPOSE 5000/tcp
# CMD ["flask", "run", "--host=0.0.0.0"]
