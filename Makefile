#
# All applications' containers
# Set of tasks related to the starting up and shutting down of the containers of all applications.
#
# Startup
startup-apps:
	docker-compose up --build -d

startup-backend-app:
	docker-compose up --build -d backend-app

startup-frontend-app:
	docker-compose up --build -d frontend-app

startup-db:
	docker-compose up --build -d db


# Shutdown
shutdown-apps:
	docker-compose down -v --rmi all

shutdown-backend-app:
	docker-compose down -v --rmi local backend-app

shutdown-frontend-app:
	docker-compose down -v --rmi local frontend-app

shutdown-db:
	docker-compose down -v --rmi local db