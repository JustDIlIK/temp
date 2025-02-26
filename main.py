import os
from http.client import HTTPException
from pathlib import Path
from uuid import uuid4

import uvicorn
from fastapi import FastAPI, UploadFile, File, Form
from sqladmin import Admin
from sqladmin.templating import Jinja2Templates
from starlette.responses import JSONResponse
from starlette.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from api.endpoints.product import router as product_router
from api.endpoints.social import router as social_router
from api.endpoints.category import router as category_router
from api.endpoints.discount import router as discount_router
from api.endpoints.shop import router as shop_router
from api.endpoints.vacancy import router as vacancy_router
from api.endpoints.condition import router as condition_router
from api.endpoints.news import router as news_router
from api.endpoints.promotion import router as promotion_router
from api.endpoints.newsletter import router as newsletter_router
from api.endpoints.users import router as user_router
from api.services.admin import (
    UserAdmin,
#    CategoryAdmin,
    ConditionAdmin,
#    DiscountAdmin,
    NewsAdmin,
    NewsletterAdmin,
    ProductAdmin,
    PromotionAdmin,
    ShopAdmin,
    SocialAdmin,
    VacancyAdmin,
)

from api.services.adminAuth import authentication_backend

from db.connection import engine

app = FastAPI()

app.include_router(product_router)
app.include_router(social_router)
#app.include_router(category_router)
#app.include_router(discount_router)
app.include_router(shop_router)
app.include_router(vacancy_router)
app.include_router(condition_router)
app.include_router(news_router)
app.include_router(promotion_router)
app.include_router(newsletter_router)
app.include_router(user_router)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

admin = Admin(
    app,
    engine,
    authentication_backend=authentication_backend,
    base_url="/admin/",
    title="Baraka Market",
    logo_url="https://api-baraka.ai-softdev.com/uploads/source/logo.svg",
    favicon_url="https://api-baraka.ai-softdev.com/uploads/source/favicon.ico",
)


admin.add_model_view(UserAdmin)
#admin.add_model_view(CategoryAdmin)
admin.add_model_view(ConditionAdmin)
#admin.add_model_view(DiscountAdmin)
admin.add_model_view(NewsAdmin)
admin.add_model_view(NewsletterAdmin)
admin.add_model_view(ProductAdmin)
admin.add_model_view(PromotionAdmin)
admin.add_model_view(ShopAdmin)
admin.add_model_view(SocialAdmin)
admin.add_model_view(VacancyAdmin)

if __name__ == "__main__":
    uvicorn.run(app)
