status: ## Status dos containers
	docker ps
ps: ## Status dos containers
	docker ps

install_dependencies: ## Instala dependências para o projeto 
	@make create_env
	@make 

create_shared_network:
	docker network create shared_network
 
create_env:  
	python3 -m venv .venv
 
pip_install:  
	. ./.venv/bin/activate
	.venv/bin/pip install -r requirements.txt

start: ## Inicia Serviços
	docker build . --tag extending_airflow:latest -f airflow/Dockerfile && \
	cd airflow && \
	mkdir -p ./dags ./logs ./plugins ./config && \
	echo -e "AIRFLOW_UID=$(id -u)" > .env && \
	docker compose up airflow-init -d && \
	docker compose up -d

run: # Roda os models do DBT localmente
	cd dbt/brazil_football && dbt run

stop: ## Desliga Serviços
	docker compose -f devops/docker-compose.yaml down  
clean:
	rm -rf .venv target
 
#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

help:
	@echo Comandos disponíveis
	@echo '   '
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
