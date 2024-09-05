ps: ## Container status
	docker ps

install_dependencies: ## Install dependencies 
	@make create_env
	@make 

create_shared_network:
	docker network create shared_network
 
create_env:  
	python3 -m venv .venv
 
pip_install:  
	. ./.venv/bin/activate
	.venv/bin/pip install -r requirements.txt

start: ## Start Services
	docker build . --tag extending_airflow:latest -f Dockerfile && \
	cd airflow && \
	mkdir -p ./dags ./logs ./plugins ./config && \
	docker compose up airflow-init -d && \
	docker compose up -d

stop: ## Stop services
	docker compose -f airflow/docker-compose.yaml down

analytics: ## Start analytics
	cd src/analytics && \
	msgfmt -o locales/en/LC_MESSAGES/messages.mo locales/en/LC_MESSAGES/messages && \
	msgfmt -o locales/pt/LC_MESSAGES/messages.mo locales/pt/LC_MESSAGES/messages && \
	streamlit run main.py
	

clean: ## Clean venv and generated folders
	rm -rf .venv target
 
#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

help:
	@echo Available Commands
	@echo '   '
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
