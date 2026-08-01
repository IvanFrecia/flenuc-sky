.PHONY: help local docker health deploy ci brand-guard icons

PORT ?= 8080
PROJECT_ID ?= skylabs-devops
SERVICE ?= sky-portfolio
REGION ?= us-central1

help:
	@echo "Ivan Frecia portfolio (flenuc-sky)"
	@echo "  make local         Run uvicorn locally (reload)"
	@echo "  make docker        Build + run container on :$(PORT)"
	@echo "  make health        curl /api/health (local)"
	@echo "  make brand-guard   Assert no org marketing brand in app copy"
	@echo "  make deploy        Deploy to Cloud Run ($(PROJECT_ID)/$(SERVICE))"
	@echo "  make ci            Local CI-ish smoke (import + health via TestClient)"

local:
	chmod +x infra/scripts/run-local.sh
	./infra/scripts/run-local.sh

docker:
	docker build -t flenuc-sky .
	docker run --rm -p $(PORT):8080 -e PORT=8080 -e ENV=production flenuc-sky

health:
	curl -sfS "http://127.0.0.1:$(PORT)/api/health" | head -c 500; echo

brand-guard:
	python3 scripts/assert_no_org_brand.py

deploy:
	chmod +x infra/scripts/deploy-stg.sh
	PROJECT_ID=$(PROJECT_ID) SERVICE=$(SERVICE) REGION=$(REGION) ./infra/scripts/deploy-stg.sh

ci:
	cd apps/portfolio && \
	  python3 -m pip install -q -r requirements.txt && \
	  PYTHONPATH=. ENV=test LEDGER_PATH=/tmp/flenuc-sky-ci-ledger.json \
	  python3 -c "from fastapi.testclient import TestClient; from app.main import app; c=TestClient(app); r=c.get('/api/health'); assert r.status_code==200 and r.json().get('status')=='ok', r.text; print('ok', r.json())"
