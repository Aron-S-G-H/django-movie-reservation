<h1 align="center"> Movie Reservation System </h1>
<h3 align="center">🌟 A system that allows users to reserve movie tickets with Poetry and Docker 🌟</h3>
<h4 align="center">🌟 This project is categorized as "Advanced" on the roadmap.sh website, and you can view the project details at the link below 🌟</h3>
<h5 align="center"><a href="https://roadmap.sh/projects/movie-reservation-system">Project detail</h3>
<br>

## 🏆 Project goal
<p>The goal of this project is to help you understand how to implement complex business logic i.e. seat reservation and scheduling, thinking about the data model and relationships, and complex queries</p>
  
## 📜 Features
- User Authentication and Authorization
  - JWT
- Movie Management
- Reservation Management
- Dockerized
- Using Poetry
- Fake data
- Fully api documentation (Swagger ui)
- Using nplusone for optimizing queries (N + 1)
- Using django debug toolbar for monitoring 

## 🛠 Installation
1. **Clone the repository**
   
   `git clone https://github.com/Aron-S-G-H/django-movie-reservation.git`
   
   `cd MovieReservation`
3. **Create and activate a virtual environment**

   `python3 -m venv venv` or `virtualenv venv`

   `source venv/bin/activate`
4. **Install dependencies**
   
   `pip install -r requirements.txt` or `poetry install --with dev`
5. **Setup DB**

   `python manage.py migrate`
6. **Generate fake data**
   
   `python manage.py generate_fake_data`     
7. **Start the app**

   `python manage.py runserver`

## 🚀 Run with Docker
---
<h4 align="center">⚠️ Ensure that you have Docker installed before you proceed</h4>

---

1. **Clone the repository**
   
   `git clone https://github.com/Aron-S-G-H/django-movie-reservation.git`

   then...

   `cd MovieReservation`
2. **Create an image**
   
   `docker build -t movieReservation:latest --no-cache .`
4. **Run a container**

   `docker run --name movieReservation -p 8000:8000 -d movieReservation:latest`
> **Note** : If you encounter the error 'ERROR: Exception TimeoutError: timed out' or something strange while creating the image, go to the Dockerfile and either remove or comment out line 20. Then, try building the image again.

## 🗂️ API documentation

`http://127.0.0.1:8000/api/schema/swagger-ui/` or `http://127.0.0.1:8000/api/schema/redoc/`

<br>

---
#### Any contributions are welcome
