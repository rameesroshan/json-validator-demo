# JSON Schema Validator 

The python library can validate the schema of json records, log validation failures and generate report of user events.

 - The sample input file is located inside `data/`
 - Schema file for the sample input is stored inside `schemas/`. The schema definition is  based on the json records in the `input.json` file, which came with the take home task.
 - The reports are generated in CSV format and stored inside `reports/`
 - The logs are written to the file `logs/validator.log`

## Setup Instructions

###  Docker Container Setup
Execute the shell script **start_docker_app** with a docker app name of your choice as argument.

The script will build the docker image, run the docker container and log in to the container.

##### Syntax

    $ bash start_docker_app <app_name>

##### Example

     $ bash start_docker_app demoapp
 The python package and other depenedencies will be installed inside the container.
###  Run the Validator
Enter the following command in the container command line to run the validator and generate report:

    $ run-validator
The sample input file contains a total of 15 json records- 13 with valid schema and 2 with invalid schema for which the validation should fail.
## Testing

The sample test cases for checking the datatype, missing field, etc. are stored inside `tests/`

the **pytest** framework is used for running the tests.

To run the test suite, execute the command inside the docker container:

    $ pytest

