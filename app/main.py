from fastapi import FastAPI
from app.routers import (
    phones_router, 
    organizations_router, 
    buildings_router, 
    activities_router,
    act_org_router,
    main_logic_router
)

app = FastAPI()

app.include_router(main_logic_router.router, prefix="/api")
app.include_router(phones_router.router, prefix="/api")
app.include_router(organizations_router.router, prefix="/api")
app.include_router(buildings_router.router, prefix="/api")
app.include_router(activities_router.router, prefix="/api")
app.include_router(act_org_router.router, prefix="/api")
