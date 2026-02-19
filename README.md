# Python Calculator - Azure-Pipeline-Initial-Integration (Azure DevOps)

In this report, we will discuss how we met the requirements for CA2 by utilizing DevOps practices. For the test, we implemented a GenAI Python code that acts as a calculator, which allowed us to apply our DevOps CI implementation practices.

## What this Repository Contains:

- 3 branches: main, dev, and test/ops
- Manual and automated testing with a target coverage of 80% and above
- Deployment of pytest for dynamic testing 
- Deployment of pylint for static code testing
- Azure Pipeline YAML for configuring the pipeline

## Technology Used

- **Python Programming Language**  
  Provides the source code for testing and measuring coverage.

- **Pytest**  
  A testing framework deployed in Azure and locally to evaluate the code coverage.

- **Azure Pipelines**  
  An automated DevOps testing platform that runs tests whenever code is pushed or a pull request is created on GitHub.

- **GitHub**  
  A platform for managing branches, version control, and handling pull or push requests (PRs).

- **GenAI - GPT**  
  A GenAI platform that provided the Python code as a source and assisted with research and error handling in the pipelines to complete the assignment.

**Chat Links Shared:**  
1. [Python Code with .gitignore setup](https://chatgpt.com/share/6919e15d-173c-8004-bb18-4bd1d85cd2cc)  
2. [Research links and error handling messages](https://chatgpt.com/share/6919ea5d-595c-8004-98dd-0eb57d4b14e5)  

## Local Deployment Setup in VS Code IDE

In VS Code, we first need to create a directory. In that directory, we initialize the environment:  
1. `git init`  
2. `git add README.md`  
3. `git commit -m "first commit of README"`  
4. `git branch -M main`  
5. `git remote add origin https://github.com/TheSamuelAttilaZemes/A00046191_CA2-Samuel-Attila-Zemes`  
6. `git push -u origin main`  

After this initialization, we deploy the GPT code provided. We first need to test the quality and coverage of the Python code. For that, we will run a separate local test using pytest in VS Code.

### Pytest Local Test in VS Code

Now, our strategy is to avoid unnecessary resource consumption in the parallel jobs provided by Microsoft (1800 minutes) by performing tests and deployments locally before pushing them to the pipelines.

To do this, we will create a local testing environment. The approach is as follows:  
- `python -m venv .venv`  
VS Code will detect the venv installation and prompt for the use of the interpreter. We should confirm this.  
- `pip install -r requirements.txt`  
This command directly installs pytest and pylint, allowing us to run tests locally and verify the code coverage to prevent resource waste in the Azure pipeline.

**requirements.txt Structure**  
```
pytest
pytest-cov
pylint
```

After that, we need to define the pytest configuration, which can be done via **pytest.ini**. This file specifies what to test, allowing us to avoid lengthy command-line inputs and clearly define our testing scope.

### Structure of `pytest.ini`

```
[pytest]
testpaths = tests  # Specifies the package for tests (setting a path to find the test files)
addopts = --cov=calculator --cov-report=term-missing 
```

- **addopts**: Additional settings for tests.
- **pytest-cov**: This is a testing plugin that allows you to see the percentage coverage of the Python tests.
- **--cov-report=term-missing**: Displays which lines are not covered by tests.

With this organized structure, we only need to run the command **pytest** in the terminal, and it will automatically run the tests in the local environment.

Next, we need to create a specialized folder to allow testing to occur. This will be our testing folder. 

The testing folder will be set up as a "package for testing," where we will add the testing Python code to cover all lines in the source code. To keep the testing environment organized, we use **`__init__.py`**. This file doesn’t require any specific structure since we define the entire folder as a package in the `pytest.ini` file.

This approach separates the testing environment from the source code, thereby distinguishing the testing environment from the deployment environment.

With this setup, we can run `pytest` locally and check the coverage, ensuring we meet the requirements outlined in the PDF.

### Pylint Setup for the Pipelines

Pylint is a static analysis tool for Python. It inspects our source code for any errors that may arise. With Pylint, we assess the code quality and structure. In CA2, we are using it to enforce our code to meet the quality standards outlined in the PDF, as well as to catch errors and improve our error handling.

**Setup:**
- **Master**: Global configuration for Pylint.
- **ignore = __pycache__**: This line specifies to ignore all cache files generated during testing.
- **jobs**: Specifies how many times processes will run.
- **message control**: Here we specify which messages should be muted. While it’s not ideal to mute all potential messages, we do this initially to assess what coverage can achieve, and then we can address any warnings or errors shown by Pylint.
- **max-line-length = 100**: Sets the maximum character limit for error message display.
- **output-format = colorized**: Helps us easily identify error messages by displaying them in color.

### Azure Pipelines Setup

In Azure Pipelines, we log into our project and navigate to Pipelines. Here, we need to establish a connection between **GitHub** and **Azure Pipelines**. We will be prompted with an authentication challenge and, after authenticating, we will grant the pipelines access to Git once we create a pull request in GitHub. 

In simple terms, whenever we push or pull in Git, the pipelines will run tests in parallel jobs to verify the code structure and provide details regarding whether the tests passed or failed, including information about which stage failed and the reasons why.

### Yamal Setup for the Pipeline

Pipelines can operate in various ways, but in our case, we prefer a YAML format. It's simple, and we use YAML in other areas of computing, such as CloudFormation in AWS.

Let’s break down the YAML into its components:

- **Trigger**: Whenever a push occurs on the branches, it will automatically start the pipeline. Under the trigger, we specify the branches. In our case, whenever a push happens in any of the three branches, it triggers the process in the pipeline.
- **Pull Request (PR)**: Whenever we update the `main` or `dev` branch, the pipeline will run and merge the XML files into each branch. Note: This approach is not ideal, but we try to run the tests separately to prevent the entire pipeline from crashing during execution.
- **Pool**: This defines the environment where the pipeline will run. In our case, we are using the latest version of Ubuntu.
- **Variables**: We create a variable to hold the Python version, so that every time we need to specify the version of Python, we can reference it via the `$` symbol.
- **Script**: This section executes the installation of the necessary dependencies to run the pipeline:
   1. `python -m pip install --upgrade pip`: This command updates Python dependencies.
   2. `pip install -r requirements.txt`: This installs the dependencies we specified during local testing, such as `pytest` and `pylint`.
   3. `pytest --cov=calculator --cov-report=xml --cov-fail-under=80`: 
      - `pytest` runs all test files (e.g., `test_calculator.py`).
      - `--cov=calculator`: This option measures how much of the calculator module is executed during the tests.
      - `--cov-fail-under=80`: If the total coverage is below 80%, `pytest` will return a non-zero exit code.
- `pylint calculator.py`: This runs static testing to examine the code.

Next, we have:

- **Task: PublishTestResults@2**: In this task, we're specifying that the results will be formatted in an XML file using the JUnit format. If the task fails, we input the command `failTaskOnFailedTests: true`, which ensures that if tests fail, the job is marked as failed.
- From this yml we achieve that whenever a push happens the the trigger of pipeline will start the CI processes and we explain the YML structure

## Branch and Pipeline Protection

In Azure, we protect the pipelines using teams. We create teams and add policies that define the privileges available to them. The three major roles that can be set are:
- Admin
- Read

**Action Settings:**
- Allow
- Deny

These settings can be accessed in the security settings of each team and provide the necessary safeguards to ensure that only authorized people or groups can execute the pipeline.

Regarding branch protection in Git, this is managed through the settings. The reason branch protection is not implemented in our Git repository is that it requires organizational settings, and since the requirements in CA2 dictate that the repository must be private, the protection has not been set up. However, we can still go through the settings:

To apply branch protection, go to the settings, click on "Branches," and add a branch rule set where we specify the required protection. We will need to pass a security setting (depending on the user account, but I have registered a passkey on my personal PC), and then branch protection will be in place.
# Conclusion
In conclusion, this report showcases the continuous integration (CI) practice of code implementation into Azure Pipelines. We present the setup, practices, code, and the strategy behind separating source code from the testing environment. We conduct local tests before implementation into the pipelines as a strategy to preserve the allocation of resources provided by Azure. 
Additionally, we highlight the structure and capabilities of Pylint. Within Azure, we detail the connection and YAML structure that defines the pipeline and the creation of CI processes. We also briefly mention security settings (images will be included in screenshots) and how we can secure both Git and Azure environments.
One issue that the author of this report did not manage effectively was running multiple jobs simultaneously across all branches. This would require a redesign of the Azure YAML configuration. Currently, our approach involves testing each branch individually to ensure we achieve a CI coverage of over 80%.

