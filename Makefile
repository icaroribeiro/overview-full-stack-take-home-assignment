#
# All applications' containers
# Set of tasks related to the starting up and shutting down of the containers of all applications.
#
startup-apps:
	docker-compose up -d --build

shutdown-apps:
	docker-compose down -v --rmi all