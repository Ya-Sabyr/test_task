# The project is a test task from Galmart
## To run the project:
Clone the repository:
```
$ gil clone https://github.com/Ya-Sabyr/test_task.git
```
Enter the project directory:
```
$ cd galmart_task
```
Build the docker container:
```
$ docker build -t my_django_app .
```
Run the container:
```
docker run -d -p 8000:8000 my_django_app
```
For a convinience testing, tests were added:
```
$ python3 manage.py test
```
<br>

### The project is made of three directories
galmart_task - Main folder
shop, test_api - App folders

Endpoints shop:
/api/v1/shops - operations with shops
/api/v1/orders - operations with orders

Enpoints test_api:
/test_api/login - obtain token
/test_api/order - update/create an order

Other endpoints:
/admin - django admin panel. To access it use - username: admin, password: admin
