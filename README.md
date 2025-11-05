## Docker-ECS-Github-Actions
This repository demonstrates a fully automated CI/CD pipeline <br>
Git push → Build Docker image → Push to Docker Hub → Deploy to AWS ECS (Fargate) <br>



## File Structure
 ```bash
.
├─ app.py
├─ requirements.txt
├─ Dockerfile
├─ .dockerignore
└─ .github/
   └─ workflows/
      └─ build-and-deploy.yml
```

File descriptions

app.py – Simple Flask app entrypoint.

requirements.txt – Lists Python dependencies.

Dockerfile – Builds the Docker image.

.dockerignore – Excludes unnecessary files from image builds.

.github/workflows/build-and-deploy.yml – GitHub Actions workflow that handles CI/CD.

🧰 Prerequisites

Before using this automation, make sure you have:

Docker Hub account – to store built images.

AWS account – with permissions for ECS, IAM, and CloudWatch Logs.

GitHub repository – containing this project.

ECS Cluster and Service (Fargate) – already set up.

IAM Execution Role – usually named ecsTaskExecutionRole.

🧱 Step 1: Set Up Docker Hub

Log in to Docker Hub.

Create a public repository (e.g., yourname/flask-welcome).

Go to Account Settings → Security → New Access Token.

Save your username and the access token — they’ll be used in GitHub secrets.

🔑 Step 2: Configure GitHub Environment & Secrets

Go to your repository’s Settings → Environments.

Create a new Environment named Docker-ECS-Github-Actions.

Inside that environment, add these secrets:

Secret Name	Example Value	Description
DOCKERHUB_USERNAME	elvis32	Docker Hub username
DOCKERHUB_TOKEN	dckr_pat_XXXXX	Docker Hub access token
DOCKERHUB_REPO	elvis32/flask-welcome	Repository name in Docker Hub
AWS_ACCESS_KEY_ID	your AWS key	AWS access key
AWS_SECRET_ACCESS_KEY	your AWS secret	AWS secret
AWS_REGION	eu-west-1	AWS region
ECS_CLUSTER	FlaskCluster	ECS cluster name
ECS_SERVICE	FlaskService	ECS service name
ECS_TASK_FAMILY	flask-welcome-task	ECS task definition family
CONTAINER_NAME	flask-welcome	ECS container name

⚠️ All workflow jobs reference this environment.
Without the environment link, secrets will not load correctly.

☁️ Step 3: Prepare AWS ECS (One-time Setup)

Create or reuse an ECS Fargate cluster.

Create a Service under the cluster (desired count ≥ 1).

Ensure the execution role ecsTaskExecutionRole has these policies:

AmazonECSTaskExecutionRolePolicy

AmazonEC2ContainerRegistryReadOnly

Verify:

The container port (5000) matches your Flask app.

Security groups allow inbound traffic (via ALB or public IP).

CloudWatch Logs group exists (named /ecs/<task-family>).

⚙️ Step 4: Workflow Overview

Once set up, the workflow runs automatically whenever you push to main, tag a version, or trigger it manually.

🔹 Build Job

Checks out your code.

Logs in to Docker Hub using secrets.

Builds and pushes the image to Docker Hub.

Tags the image as:

latest

Short SHA (7-character commit hash)

Exposes the short tag as an output for the deploy job.

🔹 Deploy Job

Configures AWS credentials.

Fetches your AWS account ID dynamically.

Generates and patches an ECS task definition (no static JSON file required).

Substitutes your environment values:

Task family, region, execution role, container name, log group.

Updates the image tag with the short SHA.

Registers the new task definition.

Deploys it to your ECS service.

Waits for service stability before finishing.

🚀 Step 5: Deployment Flow

Push code → triggers the GitHub Actions workflow.

Build job runs → image is built and uploaded to Docker Hub.

Deploy job runs → ECS service pulls the new image.

Fargate replaces old tasks with the new container.

Visit your ECS Service URL / ALB DNS →
you’ll see “Welcome to Python 🎉”.
