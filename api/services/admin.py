from sqladmin import ModelView

from db.models.category import Category
from db.models.conditions import Condition
from db.models.discount import Discount
from db.models.news import News
from db.models.newsletter import Newsletter
from db.models.product import Product
from db.models.promotion import Promotion
from db.models.shop import Shop
from db.models.socials import Social
from db.models.users import User
from db.models.vacancy import Vacancy


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email]
    column_details_exclude_list = [User.password]
    can_delete = False
    can_edit = False
    can_create = False
    icon = "fa-solid fa-user"
    name = "Пользователь"
    name_plural = "Пользователи"


#class CategoryAdmin(ModelView, model=Category):
#    column_list = [c.name for c in Category.__table__.c]
#    icon = "fa-solid fa-table-cells"
#    name = "Категория"
#    name_plural = "Категории"


class ConditionAdmin(ModelView, model=Condition):
    column_list = [c.name for c in Condition.__table__.c]
    icon = "fa-solid fa-briefcase"
    name = "Условие работы"
    name_plural = "Условия работы"


#class DiscountAdmin(ModelView, model=Discount):
#    column_list = [c.name for c in Discount.__table__.c]
#    icon = "fa-solid fa-tags"
#    name = "Скидка"
#    name_plural = "Скидки"


class NewsAdmin(ModelView, model=News):
    form_widget_args = {"image_url": {"readonly": True}}
    column_exclude_list = [News.image]
    icon = "fa-solid fa-newspaper"
    edit_template = "news_edit.html"
    create_template = "news_create.html"
    name = "Новость"
    name_plural = "Новости"


class NewsletterAdmin(ModelView, model=Newsletter):
    column_list = [c.name for c in Newsletter.__table__.c]
    icon = "fa-solid fa-envelopes-bulk"
    name = "Рассылка"
    name_plural = "Рассылка"


class ProductAdmin(ModelView, model=Product):
    icon = "fa-solid fa-cart-shopping"
    column_exclude_list = [Product.image]
    form_widget_args = {"image_url": {"readonly": True}}
    name = "Продукт"
    name_plural = "Продукты"


class PromotionAdmin(ModelView, model=Promotion):
    form_widget_args = {
        "image_url": {"readonly": True},
        "poster_url": {"readonly": True},
    }
    icon = "fa-solid fa-percent"
    column_exclude_list = [Promotion.image, Promotion.poster]
    edit_template = "promotion_edit.html"
    create_template = "promotion_create.html"
    name = "Акция"
    name_plural = "Акции"


class ShopAdmin(ModelView, model=Shop):
    column_list = [c.name for c in Shop.__table__.c]
    icon = "fa-solid fa-shop"
    name = "Магазин"
    name_plural = "Магазины"


class SocialAdmin(ModelView, model=Social):
    icon = "fa-solid fa-share-nodes"
    form_widget_args = {"image_url": {"readonly": True}}
    column_exclude_list = [News.image]
    name = "Соц. сеть"
    name_plural = "Соц. сети"


class VacancyAdmin(ModelView, model=Vacancy):
    column_list = [c.name for c in Vacancy.__table__.c]
    icon = "fa-solid fa-user-plus"
    name = "Вакансия"
    name_plural = "Вакансии"
