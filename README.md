# Assignment #3: CI/CD for Dishes/Meals Service

GitHub Actions CI/CD pipeline for the dishes and meals service that built in assignment #1.
This is the #3 assignment in Cloud Computing and Software Engineering

**Author:**
- [@benshimol.adir](https://github.com/AdirBens)
- ID. 315388850 | benshimol.adir@post.runi.ac.il

**Acknowledgements:**

This project is the third project in the course "Cloud Computing and Software Engineering (CS3961)",

taught by [Dr. Daniel Yellin](https://www.linkedin.com/in/danny-yellin-9878154/?originalSubdomain=il) 
at the School of Computer Science [Reichman University - Effi Arazi Computer Science School](https://www.linkedin.com/school/reichman-university/)

## Overview of Assignment #3
This assignment is made of the following components:

1. Nutrition-SVC application (meals and dishes services)
2. Dockerfile
4. Pytest tests
5. GitHub Actions workflow
- The GitHub Actions workflow should be triggered by a push event to the repository.

**The workflow must consist of 3 different jobs:**
### Job 1: Build

The first job is called the "build" job. Its purpose is to build the Docker image for your service. If the build is successful, it will proceed to the next job.

### Job 2: Test

The second job is called the "test" job. It will use the Docker image created in the previous job to run your service in a container. It will then use pytest to run the tests for your service. If all tests pass successfully, the workflow will proceed to the next job.

### Job 3: Query

The third job is called the "query" job. It will also run your service in a container using the Docker image from the first job. This job will issue specific requests to your service and record the results in a file.

## Image, Ports, and Workflow Name

- The Docker image is listen on localhost port 8000.
- The is stores the file `assignment3.yml` within the subdirectory `/.github/workflows` of this repository.
- The name of the workflow is "assignment3".

## Output Files

After the workflow terminates, the following artifacts should be available on GitHub:

1. **Log File:** A log file with information about the workflow execution (`log.txt`).
2. **Pytest Test Results:** The results of running the pytest tests for your service (`assn3_test_results.txt`).
3. **Query Results File:** An output file containing the results for specific queries specified in the 3rd job (`response.txt`).
4. **Image** The Docker image built in the build job (`nutrition-svc-image`).
We use `actions/upload-artifact@v3`, to make these artifacts available after the workflow terminates.
