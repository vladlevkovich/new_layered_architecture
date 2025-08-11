# from sqlalchemy import create_engine
# from sqlalchemy.orm import Session
#
# from app.src.models.menu_models import Dish
#
# engine = create_engine("sqlite:///project.db", echo=True)
#
# # Base.metadata.create_all(engine)
#
# sample_dishes = [
#     Dish(name="Борщ український", description="Традиційний борщ з м’ясом та сметаною", price=95.00, photo=None),
#     Dish(name="Вареники з картоплею", description="Домашні вареники з картоплею та смаженою цибулею", price=75.50, photo=None),
#     Dish(name="Салат Цезар", description="Салат з куркою, грінками, пармезаном і соусом Цезар", price=110.00, photo=None),
#     Dish(name="Піцца Маргарита", description="Класична піцца з томатами та моцарелою", price=125.00, photo=None),
#     Dish(name="Капучино", description="Ароматна кава з молочною пінкою", price=45.00, photo=None),
# ]
#
# with Session(engine) as session:
#     session.add_all(sample_dishes)
#     session.commit()
#
# print("Тестові страви успішно додані.")
