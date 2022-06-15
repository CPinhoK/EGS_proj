from typing import Optional, List
from enum import Enum
import uuid

from fastapi import FastAPI, File, UploadFile, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

import databases
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os


## Database configuration
# DATABASE_URL = "sqlite:///./stock.db"
DATABASE_URL = f"mysql+pymysql://test:test@stockapi-db:3306/stockapi_db"
# DATABASE_URL = "postgresql://test:test@127.0.0.1:5432/stock"

sql_database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

products = sqlalchemy.Table(
    "products",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, unique=True),
    sqlalchemy.Column("name", sqlalchemy.String(100)),
    sqlalchemy.Column("price", sqlalchemy.FLOAT),
    sqlalchemy.Column("image", sqlalchemy.String(100)),
    sqlalchemy.Column("category_id", sqlalchemy.Integer),
    sqlalchemy.Column("status", sqlalchemy.String(100))
)

articles = sqlalchemy.Table(
    "articles",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, unique=True),
    sqlalchemy.Column("product_id", sqlalchemy.Integer),
    sqlalchemy.Column("key", sqlalchemy.String(100), unique=True)
)

categories = sqlalchemy.Table(
    "categories",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, unique=True),
    sqlalchemy.Column("name", sqlalchemy.String(100))
)

engine = sqlalchemy.create_engine(
    DATABASE_URL    # connect_args={"check_same_thread": False}
)

metadata.create_all(engine)

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

## Models:
class Status(Enum):
    in_stock = "In_Stock"
    out_stock = "Out_of_Stock"


class Category(BaseModel):
    id: int
    name: str


class Product(BaseModel):
    id: int
    name: str
    price: float
    image: Optional[str]
    category: int
    status: Status


class Article(BaseModel):
    id: int
    product_id: int
    key: str


# Create Database
database = [
    Product(id=1, name="product_test1", price=1.99, image=None, category=1, status=Status.in_stock),
    Product(id=2, name="product_test2", price=2.99, image=None, category=2, status=Status.out_stock),
    Article(id=1, product_id=1, key="A1B2C3"),
    Article(id=2, product_id=2, key="Z0X9Y8"),
    Article(id=3, product_id=2, key="Z0X9Y8")
]

## Methods:
@app.on_event("startup")
async def startup() -> None:
    database_ = sql_database
    if not database_.is_connected:
        await database_.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    database_ = sql_database
    if database_.is_connected:
        await database_.disconnect()


@app.get("/")
def read_root():
    return {"This is an api for products stock management"}


@app.get("/products")
async def get_all_products(response: Response):
    # await sql_database.connect()
    query = products.select()

    try:
        products_list = await sql_database.fetch_all(query)
    except Exception as e: 
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"Status": 404, "Message": str(e)}

    response.status_code = status.HTTP_200_OK
    return products_list

    # to_send = []
    # for item in database:
    #     if (type(item) is Product):
    #         to_send.append(item)

    # if (len(to_send) == 0):
    #     response.status_code = status.HTTP_404_NOT_FOUND
    #     return {"Status": 404, "Message": "No products in database!"}
    # else:
    #     response.status_code = status.HTTP_200_OK
    #     return to_send


@app.post("/products")
async def insert_product(product: Product, response: Response):
    test_query = categories.select().where(categories.c.id == product.category)
    test_list = await sql_database.fetch_all(test_query)

    if (test_list == []):
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"Status": 404, "Message": "There are no categories with id: " + str(product.category)}
    else:
        query = products.insert().values(id = product.id, name = product.name, price = product.price, \
        image = None, category_id = product.category, status = str(product.status))

        try:
            await sql_database.execute(query)
        except Exception as e: 
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"Status": 400, "Message": str(e)}

        response.status_code = status.HTTP_201_CREATED
        return product

    # for item in database:
    #     if (type(item) is Product):
    #         if (item.id == product.id):
    #             response.status_code = status.HTTP_400_BAD_REQUEST
    #             return {"Status": 400, "Message": "This product is already in the database"}
    # database.append(product)
    # response.status_code = status.HTTP_201_CREATED
    # return product


@app.put("/products/{id}")
async def update_product(id: int, product: Product, response: Response):
    query = products.update().where(products.c.id == id).values(id = product.id, name = product.name, \
    price = product.price, image = None, category_id = product.category, status = str(product.status))

    try:
        await sql_database.execute(query)
    except Exception as e: 
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"Status": 404, "Message": str(e)}

    response.status_code = status.HTTP_200_OK
    return product

    # for item in database:
    #     if (type(item) is Product):
    #         if (item.id == id):
    #             item.id = product.id
    #             item.name = product.name
    #             item.category = product.category
    #             item.status = product.status
    #             response.status_code = status.HTTP_200_OK
    #             return item
    
    # response.status_code = status.HTTP_404_NOT_FOUND
    # return {"Status": 404, "Message": "Product not found!"}


@app.delete("/products/{id}")
async def delete_product(id: int, response: Response):
    test_query = products.select().where(products.c.id == id)
    test_list = await sql_database.fetch_all(test_query)

    if (test_list == []):
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"Status": 404, "Message": "There are no products with id: " + str(id)}
    else:
        query = products.delete().where(products.c.id == id)

        try:
            await sql_database.execute(query)
        except Exception as e:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"Status": 400, "Message": str(e)}

        response.status_code = status.HTTP_200_OK
        return {"Status": 200, "Message": "Product with id: " + str(id) + " was deleted!"}

    # for item in database:
    #     if (type(item) is Product):
    #         if (item.id == id):
    #             database.remove(item)
    #             response.status_code = status.HTTP_200_OK
    #             return {"Status": 200, "Message": "Product deleted!"}
    # response.status_code = status.HTTP_404_NOT_FOUND
    # return {"Status": 404, "Message": "Product not found!"}


@app.get("/products/")
async def read_product_query(id: int | None = None, name: str | None = None, category: int | None = None, status: Status | None = None):
    if (id):
        query = products.select().where(products.c.id == id)
    else:
        if (name and category and status):
            query = products.select().where(products.c.name == name and products.c.category_id == category \
            and products.c.status == str(status))
        elif (name and category):
            query = products.select().where(products.c.name == name and products.c.category_id == category)
        elif (name and status):
            query = products.select().where(products.c.name == name and products.c.status == str(status))
        elif (category and status):
            query = products.select().where(products.c.category_id == category and products.c.status == str(status))
        elif (name):
            query = products.select().where(products.c.name == name)
        elif (category):
            query = products.select().where(products.c.category_id == category)
        elif (status):
            query = products.select().where(products.c.status == str(status))
         
    try:
        products_list = await sql_database.fetch_all(query)
    except Exception as e:
        return {"Status": 404, "Message": str(e)}

    return products_list

    # to_send = []
    # print (name)
    # for item in database:
    #     if (type(item) is Product):
    #         if (id):
    #             if (item.id == id):
    #                 return item
    #         else:
    #             if (name and category and status):
    #                 if (item.name == name and item.category.id == category and item.status == status):
    #                     to_send.append(item)
    #             elif (name and category):
    #                 if (item.name == name and item.category.id == category):
    #                     to_send.append(item)
    #             elif (name and status):
    #                 if (item.name == name and item.status == status):
    #                     to_send.append(item)
    #             elif (category and status):
    #                 if (item.category.id == category and item.status == status):
    #                     to_send.append(item)
    #             elif (name):
    #                 if (item.name == name):
    #                     to_send.append(item)
    #             elif (category):
    #                 if (item.category.id == category):
    #                     to_send.append(item)
    #             elif (status):
    #                 if (item.status == status):
    #                     to_send.append(item)

    # if (len(to_send) == 0):
    #     return {"Status": 404, "Message": "No Products found!"}
    # else:
    #     return to_send


@app.get("/articles/{id_product}")
async def get_product_article(id_product: int, response: Response):
    query = articles.select().where(articles.c.product_id == id_product)

    try:
        articles_list = await sql_database.fetch_all(query)
    except Exception as e: 
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"Status": 404, "Message": str(e)}

    response.status_code = status.HTTP_202_ACCEPTED
    return articles_list

    # to_send = []
    # for item in database:
    #     if (type(item) is Article and item.product_id == id_product):
    #         to_send.append(item)

    # if (len(to_send) == 0):
    #     response.status_code = status.HTTP_404_NOT_FOUND
    #     return {"Status": 404, "Message": "No articles for this product id!"}
    # else:
    #     response.status_code = status.HTTP_202_ACCEPTED
    #     return to_send


@app.post("/articles")
async def insert_article(article : Article, response: Response):
    test_query = products.select().where(products.c.id == article.product_id)
    test_list = await sql_database.fetch_all(test_query)

    if (test_list == []):
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"Status": 404, "Message": "There are no products with id: " + str(article.product_id)}
    else: 
        query = articles.insert().values(id = article.id, product_id = article.product_id, key = article.key)

        try:
            await sql_database.execute(query)
        except Exception as e: 
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"Status": 400, "Message": str(e)}

        print (article)
        response.status_code = status.HTTP_201_CREATED
        return article

    # for item in database:
    #     if (type(item) is Article):
    #         if (item.id == article.id):
    #             response.status_code = status.HTTP_400_BAD_REQUEST
    #             return {"Status": 400, "Message": "This article is already in the database"}
    #         elif (item.product_id == article.product_id):
    #             response.status_code = status.HTTP_404_NOT_FOUND
    #             return {"Status": 404, "Message": "Product id provided not found!"}
    # database.append(article)
    # response.status_code = status.HTTP_201_CREATED
    # return article


@app.put("/articles/{id}")
async def update_article(id: int, article: Article, response: Response):
    query = articles.update().where(articles.c.id == id).values(id = article.id, product_id = article.product_id, key = article.key)

    try:
        await sql_database.execute(query)
    except Exception as e: 
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"Status": 404, "Message": str(e)}

    response.status_code = status.HTTP_200_OK
    return article

    # for item in database:
    #     if (type(item) is Article):
    #         if (item.id == id):
    #             item.id = article.id
    #             item.product_id = article.product_id
    #             item.key = article.key
    #             response.status_code = status.HTTP_200_OK
    #             return item
    # response.status_code = status.HTTP_404_NOT_FOUND
    # return {"Status": 404, "Message": "Article not found!"}


@app.delete("/articles/{id}")
async def delete_article(id : int, response: Response):
    test_query = articles.select().where(articles.c.id == id)
    test_list = await sql_database.fetch_all(test_query)

    if (test_list == []):
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"Status": 404, "Message": "There are no articles with id: " + str(id)}
    else:
        query = articles.delete().where(articles.c.id == id)

        try:
            await sql_database.execute(query)
        except Exception as e:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"Status": 400, "Message": str(e)}

        response.status_code = status.HTTP_200_OK
        return {"Status": 200, "Message": "Article with id: " + str(id) + " was deleted!"}

    # for item in database:
    #     if (type(item) is Article):
    #         if (item.id == id):
    #             database.remove(item)
    #             response.status_code = status.HTTP_200_OK
    #             return {"Status": 200, "Message": "Article deleted!"}
    #         else:
    #             response.status_code = status.HTTP_404_NOT_FOUND
    #             return {"Status": 404, "Message": "Article not found!"}

@app.post("/category")
async def insert_category(category : Category, response: Response):
    query = categories.insert().values(id = category.id, name = category.name)

    try:
        await sql_database.execute(query)
    except Exception as e: 
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"Status": 400, "Message": str(e)}

    response.status_code = status.HTTP_201_CREATED
    return category


@app.get("/category")
async def get_all_categories(response: Response):
    query = categories.select()

    try:
        category_list = await sql_database.fetch_all(query)
    except Exception as e: 
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"Status": 400, "Message": str(e)}

    response.status_code = status.HTTP_201_CREATED
    return category_list


@app.put("/category/{id}")
async def update_category(id: int, category: Category, response: Response):
    query = categories.update().where(categories.c.id == id).values(id = category.id, name = category.name)

    try:
        await sql_database.execute(query)
    except Exception as e: 
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"Status": 404, "Message": str(e)}

    response.status_code = status.HTTP_200_OK
    return category


@app.delete("/category/{id}")
async def delete_category(id: int, response: Response):
    test_query = categories.select().where(categories.c.id == id)
    test_list = await sql_database.fetch_all(test_query)

    if (test_list == []):
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"Status": 404, "Message": "There are no categories with id: " + str(id)}
    else:
        query = categories.delete().where(categories.c.id == id)

        try:
            await sql_database.execute(query)
        except Exception as e:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"Status": 400, "Message": str(e)}

        response.status_code = status.HTTP_200_OK
        return {"Status": 200, "Message": "Category with id: " + str(id) + " was deleted!"}

# Requires pip install python-multipart
@app.post("/Image/{id}")
async def upload_image(id: int, response: Response, file: bytes = File(...)):
    name = str(uuid.uuid4())
    url = 'www/images/' + name + ".png"

    test_query = products.select().where(products.c.id == id)
    test_list = await sql_database.fetch_all(test_query)

    if (test_list == []):
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"Status": 404, "Message": "There are no products with id: " + str(id)}
    elif (test_list[0][3] != None):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"Status": 400, "Message": "Product with id: " + str(id) + " already has an image!"}
    else:
        query = products.update().where(products.c.id == id).values(image = url)

        try:
            with open(url,'wb') as image:
                image.write(file)
                image.close()
            await sql_database.execute(query)
        except Exception as e:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"Status": 400, "Message": str(e)}

        response.status_code = status.HTTP_200_OK
        return {"Status": 200, "Message": "Image for product with id: " + str(id) + " uploaded!"}

    # name = str(uuid.uuid4())
    # url = 'images/' + name + ".png"

    # for item in database:
    #     if (type(item) is Product):
    #         if (item.id == id):
    #             if (item.image == None):
    #                 with open(url,'wb') as image:
    #                     image.write(file)
    #                     image.close()
    #                 item.image = name
    #                 response.status_code = status.HTTP_200_OK
    #                 return "Image " + name + " was added to product with id " + str(id)
    #             else:
    #                 response.status_code = status.HTTP_400_BAD_REQUEST
    #                 return {"Status": 400, "Message": "This Product already was an image"}
    
    # response.status_code = status.HTTP_404_NOT_FOUND
    # return {"Status": 404, "Message": "This Product was not found!"}


@app.put("/Image/{id}")
async def update_image(id: int, response: Response, file: bytes = File(...)):
    name = str(uuid.uuid4())
    url = 'www/images/' + name + ".png"

    test_query = products.select().where(products.c.id == id)
    test_list = await sql_database.fetch_all(test_query)

    if (test_list == []):
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"Status": 404, "Message": "There are no products with id: " + str(id)}
    else:
        query = products.update().where(products.c.id == id).values(image = url)

        try:
            with open(url,'wb') as image:
                image.write(file)
                image.close()
            await sql_database.execute(query)
        except Exception as e:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"Status": 400, "Message": str(e)}

        os.remove(test_list[0][3])
        response.status_code = status.HTTP_200_OK
        return {"Status": 200, "Message": "Image for product with id: " + str(id) + " updated!"}

    # name = str(uuid.uuid4())
    # url = 'images/' + name + ".png"

    # for item in database:
    #     if (type(item) is Product):
    #         if (item.id == id):
    #             if (item.image != None):
    #                 with open(url,'wb') as image:
    #                     image.write(file)
    #                     image.close()
    #                 item.image = name
    #                 response.status_code = status.HTTP_200_OK
    #                 return "Image " + name + " was updated to product with id " + str(id)
    #             else:
    #                 response.status_code = status.HTTP_400_BAD_REQUEST
    #                 return {"Status": 400, "Message": "This Product doesn't have an image"}
    
    # response.status_code = status.HTTP_404_NOT_FOUND
    # return {"Status": 404, "Message": "This Product was not found!"}


@app.delete("/Image/{id}")
async def delete_image(id: int, response: Response):
    test_query = products.select().where(products.c.id == id)
    test_list = await sql_database.fetch_all(test_query)

    if (test_list == []):
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"Status": 404, "Message": "There are no products with id: " + str(id)}
    elif (test_list[0][3] == None):
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"Status": 404, "Message": "Product with id: " + str(id) + " has no image"}
    else:
        query = products.update().where(products.c.id == id).values(image = None)

        os.remove(test_list[0][3])

        try:
            await sql_database.execute(query)
        except Exception as e:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"Status": 400, "Message": str(e)}

        response.status_code = status.HTTP_200_OK
        return {"Status": 200, "Message": "Image for product with id: " + str(id) + " was deleted!"}


@app.get("/Image/{id}")
async def get_image(id: int, response: Response):
    test_query = products.select().where(products.c.id == id)
    test_list = await sql_database.fetch_all(test_query)

    if (test_list == []):
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"Status": 404, "Message": "There are no products with id: " + str(id)}
    else:
        response.status_code = status.HTTP_200_OK
        return test_list[0][3]

    # for item in database:
    #     if (type(item) is Product):
    #         if (item.id == id):
    #             if (item.image != None):
    #                 image_name = item.image
    #                 image_url = 'images/' + image_name + '.png'
    #                 response.status_code = status.HTTP_200_OK
    #                 return FileResponse(path=image_url, filename=image_name, media_type='image/png')
    #             else:
    #                 response.status_code = status.HTTP_404_NOT_FOUND
    #                 return {"Status": 404, "Message": "No image found for this product"}    

    # response.status_code = status.HTTP_404_NOT_FOUND
    # return {"Status": 404, "Message": "Product not found!"}