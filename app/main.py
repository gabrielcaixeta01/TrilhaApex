from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.routers import pet_crud, order_crud, user_crud

app = FastAPI(title="Petstore da Apex")

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

app.include_router(pet_crud.router)
app.include_router(order_crud.router)
app.include_router(user_crud.router)

def get_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = FastAPI.openapi(app)
    
    allowed_schemas = {"Category", "Order", "Pet", "User"}
    
    if "components" in openapi_schema and "schemas" in openapi_schema["components"]:
        schemas_to_remove = [key for key in openapi_schema["components"]["schemas"].keys() 
                            if key not in allowed_schemas]
        for schema in schemas_to_remove:
            del openapi_schema["components"]["schemas"][schema]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = get_openapi