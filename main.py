"""
Simple Shop Stock and Accounts Management System
FastAPI Application Entry Point
"""

from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from database import init_db
from routers import stock, purchases, sales, expenses, dashboard, history

BASE_DIR = Path(__file__).resolve().parent


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database, tables, and seed default products on startup
    print("=" * 60)
    print("Initializing Shop Stock & Accounts Database in MySQL...")
    try:
        init_db()
        print("Database initialized successfully!")
    except Exception as e:
        print(f"Error during database initialization: {e}")
    print("=" * 60)
    yield
    print("Shop Management Server shutting down...")


app = FastAPI(
    title="Shop Stock & Accounts Management System",
    description="Simple, bilingual (Urdu/English) stock and profit management for home appliance shops",
    version="1.0.0",
    lifespan=lifespan
)

# Mount static files (CSS, JS, Icons)
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# Templates
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Register API Routers
app.include_router(stock.router)
app.include_router(purchases.router)
app.include_router(sales.router)
app.include_router(expenses.router)
app.include_router(dashboard.router)
app.include_router(history.router)


@app.get("/", response_class=HTMLResponse)
async def serve_shopkeeper_interface(request: Request):
    """Serve the single-page bilingual Shopkeeper web interface"""
    return templates.TemplateResponse(request=request, name="index.html", context={})


@app.get("/api/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "online",
        "system": "Home Appliances Stock & Accounts Management",
        "supported_products": [
            "Refrigerator",
            "Air Cooler",
            "Air Conditioner (AC)",
            "Washing Machine"
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
