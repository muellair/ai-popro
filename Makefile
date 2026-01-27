all:
	docker volume create ai_system
	docker build -f images/knowledgeBase_aipopro/Dockerfile -t knowledgebase_aipopro .
	docker build -t activationbase_aipopro -f images/activationBase_aipopro/Dockerfile .
	docker build -t codebase_aipopro -f images/codeBase_aipopro/Dockerfile .
	docker compose -f scenarios/docker-compose-ai.yaml up
	docker compose -f scenarios/docker-compose-ols.yaml up