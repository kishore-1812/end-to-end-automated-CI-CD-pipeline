# Project variables
DOCKER_IMAGE = fastapi-app
DOCKERFILE = fastAPI.dockerfile
CONTAINER_NAME = fastapi-app-container
PORT = 8000
# AWS_REGION = us-east-1
# AWS_ACCOUNT_ID = <your-aws-account-id>
# AWS_ECR_REPO = $(AWS_ACCOUNT_ID).dkr.ecr.$(AWS_REGION).amazonaws.com/$(DOCKER_IMAGE)
# SSH_KEY = MyKeyPair.pem
# EC2_PUBLIC_IP = <your-ec2-public-ip>

# Declare all targets as phony
.PHONY: build run stop remove clean ps logs prune test help

# Build Docker Image
build:
	docker build -t $(DOCKER_IMAGE) -f $(DOCKERFILE) .

# Run Container (Detached Mode)
run:
	docker rm -f fastapi-app-container 2>/dev/null || true
	docker run -d -p $(PORT):8000 --name $(CONTAINER_NAME) $(DOCKER_IMAGE)

# Stop Running Container
stop:
	docker stop $(CONTAINER_NAME) || true

# Remove Container
remove:
	docker rm $(CONTAINER_NAME) || true

# Remove Docker Image
clean:
	docker rmi $(DOCKER_IMAGE) || true

# Show Running Containers
ps:
	docker ps

# Show Docker Logs
logs:
	docker logs $(CONTAINER_NAME)

# Remove all unused Docker resources
prune:
	docker image prune -af

# Test the FastAPI application
test:
	curl http://localhost:$(PORT)

# Display help message
help:
	@echo "Available targets:"
	@echo "  build         - Build Docker image"
	@echo "  run           - Run Docker container"
	@echo "  stop          - Stop running container"
	@echo "  remove        - Remove container"
	@echo "  clean         - Remove Docker image"
	@echo "  ps            - Show running containers"
	@echo "  logs          - Show Docker logs"
	@echo "  prune         - Remove unused Docker resources"
	@echo "  test          - Test the FastAPI application"

# Uncomment the following targets when ready for AWS deployment
# # Create ECR Repository
# create-ecr-repo:
# 	aws ecr create-repository --repository-name $(DOCKER_IMAGE) --region $(AWS_REGION) || true

# # Push Image to AWS ECR (Ensure you're logged in first)
# push-to-ecr: create-ecr-repo
# 	aws ecr get-login-password --region $(AWS_REGION) | docker login --username AWS --password-stdin $(AWS_ECR_REPO)
# 	docker tag $(DOCKER_IMAGE) $(AWS_ECR_REPO)
# 	docker push $(AWS_ECR_REPO)

# # Deploy to AWS EC2 (SSH into instance & pull latest Docker image)
# deploy-ec2:
# 	ssh -i $(SSH_KEY) ubuntu@$(EC2_PUBLIC_IP) "docker pull $(AWS_ECR_REPO) && docker run -d -p $(PORT):8000 $(AWS_ECR_REPO)"