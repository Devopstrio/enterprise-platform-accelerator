import logging
import time
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app
from pythonjsonlogger import jsonlogger

# Logger setup
logger = logging.getLogger("enterprise-platform-api")
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

app = FastAPI(title="Enterprise Platform API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Metrics
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    logger.info(f"Path: {request.url.path} Duration: {duration:.4f}s Status: {response.status_code}")
    return response

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/platform/provision")
def provision_service(template_id: str, team_id: str, environment: str = "dev"):
    logger.info(f"Provisioning golden path {template_id} for team {team_id} in {environment}")
    return {"status": "PROVISIONING", "operation_id": f"svc_{int(time.time())}", "estimated_duration": "8m"}

@app.get("/catalog/services")
def get_catalog_services():
    return [
        {"id": "go-micro-v1", "name": "Standard Go Microservice", "language": "Go", "maturity": "GOLDEN"},
        {"id": "py-api-v2", "name": "FastAPI Service", "language": "Python", "maturity": "GOLDEN"},
        {"id": "react-spa-v1", "name": "Vite React SPA", "language": "TypeScript", "maturity": "SILVER"}
    ]

@app.post("/deployments/run")
def run_deployment(service_id: str, target: str = "aks-prod-01"):
    logger.info(f"Triggering GitOps sync for {service_id} to {target}")
    return {"status": "SYNCING", "sync_id": f"sync_{int(time.time())}"}

@app.get("/costs/summary")
def get_costs_summary():
    return {
        "monthly_platform_spend": 450000,
        "compute_spend": 280000,
        "storage_spend": 120000,
        "managed_services_spend": 50000,
        "idle_resource_waste": 12400,
        "budget_variance": "-0.8%"
    }

@app.get("/governance/status")
def get_governance_status():
    return {
        "golden_path_adoption": "84%",
        "policy_compliance": "98%",
        "vulnerability_remediation_rate": "92%",
        "platform_drift_detected": False
    }

@app.get("/scores/summary")
def get_scores_summary():
    return {
        "platform_maturity": 0.94,
        "developer_experience_index": 0.88,
        "operational_efficiency": 0.96,
        "reliability_score": 0.99
    }

@app.get("/dashboard/summary")
def get_dashboard_summary():
    return {
        "active_services": 1240,
        "total_deployments_24h": 450,
        "onboarded_teams": 82,
        "platform_status": "READY"
    }
