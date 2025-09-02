# Path to FastAPI Dockerfile and context
SRC_DIR        = ./fastapi
DOCKER_IMAGE   = fastapi-app
DOCKERFILE     = $(SRC_DIR)/fastAPI.dockerfile
CONTAINER_NAME = fastapi-app-container
PORT           = 8000

# Path to Wazuh Docker Compose setup
WAZUH_DIR      = ./wazuh-docker/single-node

.PHONY: build run stop remove clean ps logs prune test deploy destroy \
        wazuh-up wazuh-down all-up all-down help

# ---------- FastAPI Local Workflow ----------
build:
	docker build -t $(DOCKER_IMAGE) -f $(DOCKERFILE) $(SRC_DIR)

run:
	docker rm -f $(CONTAINER_NAME) 2>/dev/null || true
	docker run -d -p $(PORT):8000 --name $(CONTAINER_NAME) $(DOCKER_IMAGE)

# ---------- Wazuh Docker Compose Workflow ----------
wazuh-up:
	cd $(WAZUH_DIR) && docker compose up -d

wazuh-down:
	cd $(WAZUH_DIR) && docker compose down

# ---------- Kickstart Everything ----------

# all-up: build run 
all-up: build run wazuh-up
	@echo "FastAPI container and Wazuh stack started!"


# all-down: stop remove
all-down: stop remove wazuh-down
	@echo "FastAPI container and Wazuh stack stopped and removed!"

# (Other targets like stop, remove, clean, ps, logs, prune, test, deploy, destroy, help unchanged)
deploy:
	terraform init
	terraform plan
	terraform apply -auto-approve

destroy:
	terraform destroy -auto-approve