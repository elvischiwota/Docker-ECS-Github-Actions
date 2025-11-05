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

## File descriptions
🔹 app.py – Simple Flask app entrypoint. <br>
🔹 requirements.txt – Lists Python dependencies. <br>
🔹 Dockerfile – Builds the Docker image. <br>
🔹 .dockerignore – Excludes unnecessary files from image builds. <br>
🔹 .github/workflows/build-and-deploy.yml – GitHub Actions workflow that handles CI/CD. <br>

## Prerequisites
Before using this automation, make sure you have: <br>
a. Docker Hub account – to store built images. <br>
b. AWS account – with permissions for ECS, IAM, and CloudWatch Logs. <br>
c. GitHub repository – containing this project. <br>
d. ECS Cluster and Service (Fargate) – already set up. <br>
e. IAM Execution Role – usually named ecsTaskExecutionRole. <br>

## Step 1: Set Up Docker Hub
a. Log in to Docker Hub. <br>
b. Create a public repository (e.g., yourname/flask-welcome). <br>
c. Go to Account Settings → Security → New Access Token. <br>
d. Save your username and the access token — they’ll be used in GitHub secrets. <br>

## Step 2: Configure GitHub Environment & Secrets
a. Go to your repository’s Settings → Environments. <br>
b. Create a new Environment named Docker-ECS-Github-Actions. <br>
c. Inside that environment, add these secrets: <br>

| Secret Name             | Example Value            | Description                   |
| :----------------------- | :----------------------- | :----------------------------- |
| `DOCKERHUB_USERNAME`    | `elvis32`               | Docker Hub username            |
| `DOCKERHUB_TOKEN`       | `dckr_pat_XXXXX`        | Docker Hub access token        |
| `DOCKERHUB_REPO`        | `elvis32/flask-welcome` | Repository name in Docker Hub  |
| `AWS_ACCESS_KEY_ID`     | *your AWS key*          | AWS access key                 |
| `AWS_SECRET_ACCESS_KEY` | *your AWS secret*       | AWS secret                     |
| `AWS_REGION`            | `eu-west-1`             | AWS region                     |
| `ECS_CLUSTER`           | `FlaskCluster`          | ECS cluster name               |
| `ECS_SERVICE`           | `FlaskService`          | ECS service name               |
| `ECS_TASK_FAMILY`       | `flask-welcome-task`    | ECS task definition family     |
| `CONTAINER_NAME`        | `flask-welcome`         | ECS container name             |

All workflow jobs reference this environment. <br>
Without the environment link, secrets will not load correctly. <br>

## Step 3: Prepare AWS ECS (One-time Setup)
a. Create or reuse an ECS Fargate cluster. <br>
b. Create a Service under the cluster (desired count ≥ 1). <br>
c. Ensure the execution role ecsTaskExecutionRole has these policies: <br>
 🔹 AmazonECSTaskExecutionRolePolicy <br>
 🔹 AmazonEC2ContainerRegistryReadOnly <br>

d. Verify: <br>
 🔹 The container port (5000) matches your Flask app. <br>
 🔹 Security groups allow inbound traffic (via ALB or public IP). <br>
 🔹 CloudWatch Logs group exists (named /ecs/<task-family>). <br>

## Step 4: Workflow Overview
Once set up, the workflow runs automatically whenever you push to main, tag a version, or trigger it manually.  <br>
a. Build Job  <br>
🔹 Checks out your code.<br>
🔹 Logs in to Docker Hub using secrets.<br>
🔹 Builds and pushes the image to Docker Hub.<br>
🔹 Tags the image as:<br>
  🔹 latest<br>
  🔹 Short SHA (7-character commit hash)<br>
🔹 Exposes the short tag as an output for the deploy job.<br>

b. Deploy Job
🔹 Configures AWS credentials.<br>
🔹 Fetches your AWS account ID dynamically.<br>
🔹 Generates and patches an ECS task definition (no static JSON file required).<br>
🔹 Substitutes your environment values:<br>
  🔹 Task family, region, execution role, container name, log group.<br>
🔹 Updates the image tag with the short SHA.<br>
🔹 Registers the new task definition.<br>
🔹 Deploys it to your ECS service.<br>
🔹 Waits for service stability before finishing.<br>

## Step 5: Deployment Flow
a. Push code → triggers the GitHub Actions workflow.<br>
b. Build job runs → image is built and uploaded to Docker Hub.<br>
c. Deploy job runs → ECS service pulls the new image.<br>
d. Fargate replaces old tasks with the new container.<br>

Visit your ECS Service URL / ALB DNS → <br>
you’ll see “Welcome to Python”. <br>
