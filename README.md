# BrazilPrev Commerce

This project is a simple demonstration of a sales record application. Its functions are as described below:

- User, customer and product registration
- Registration of purchases as well as closing and adding products with their respective quantities.

## Technical details:

##### The following tools are highlighted in the project stack:
- Python 3.8
- Flask
- SqlAlchemy
- Docker
- Poetry

I made the commits of the project trying to make everything clearer and where each part is and how the modules and levels are divided: ex. application and environment



#### About using the project

I built this project thinking that everything was automated so I wrote a **Makefile** that contains everything you need from running locally, running tests and running in containers.

With some tool to make http requests, I used postman, you can use the project tests as examples to make ecommerce flows.

The commands in the makefile start with the prefix of the desired environment.

 ```sh
 ####################
 # Local development#
 ####################
 # Create env for project and install dependencies
 $ make dev-install
 # Run a local app instance
 $ make dev-run
 # Start database
 $ make dev_db-up
 # Create tables
 $ make dev_db-initialize
 # Stop Database 
 $ make dev_db-stop

 ###################
 # Local tests     #
 ###################
 # Run a local app instance
 $ make tests
 # Start database
 $ make test_db-up
 # Stop Database 
 $ make test_db-stop


 ###################
 # Run with Docker #
 ###################
 # Build all containers
 $ make docker-build
 # Run containers
 $ make docker-run
```
