from typing import Optional
from enum import Enum
import uuid

from fastapi import FastAPI, File, UploadFile, Response, status
from fastapi.responses import FileResponse
from pydantic import BaseModel


class Status(Enum):
    in_stock = "In_Stock"
    out_stock = "Out_of_Stock"

app = FastAPI()

##Models:
class Category(BaseModel):
    id: int
    name: str


class Product(BaseModel):
    id: int
    name: str
    price: float
    image: Optional[str]
    category: Category
    status: Status


class Article(BaseModel):
    id: int
    product_id: int
    key: str


#Create Database
database = [
    Product(id=1, name="product_test1", price=1.99, image=None, category=Category(id=1, 
    name="category_test1"), status=Status.in_stock),
    Product(id=2, name="product_test2", price=2.99, image=None, category=Category(id=2, 
    name="category_test2"), status=Status.out_stock),
    Article(id=1, product_id=1, key="A1B2C3"),
    Article(id=2, product_id=2, key="Z0X9Y8"),
    Article(id=3, product_id=2, key="Z0X9Y8")
]


##Methods:
@app.get("/")
def read_root():
    return {"This is an api for products stock management"}


@app.get("/products")
async def get_all_products(response: Response):
    to_send = []
    for item in database:
        if (type(item) is Product):
            to_send.append(item)

    if (len(to_send) == 0):
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"Status": 404, "Message": "No products in database!"}
    else:
        response.status_code = status.HTTP_200_OK
        return to_send


@app.post("/products")
async def insert_product(product: Product, response: Response):
    for item in database:
        if (type(item) is Product):
            if (item.id == product.id):
                response.status_code = status.HTTP_400_BAD_REQUEST
                return {"Status": 400, "Message": "This product is already in the database"}
    database.append(product)
    response.status_code = status.HTTP_201_CREATED
    return product


@app.put("/products/{id}")
async def update_product(id: int, product: Product, response: Response):
    for item in database:
        if (type(item) is Product):
            if (item.id == id):
                item.id = product.id
                item.name = product.name
                item.category = product.category
                item.status = product.status
                response.status_code = status.HTTP_200_OK
                return item
    
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"Status": 404, "Message": "Product not found!"}


@app.delete("/products/{id}")
async def delete_product(id: int, response: Response):
    for item in database:
        if (type(item) is Product):
            if (item.id == id):
                database.remove(item)
                response.status_code = status.HTTP_200_OK
                return {"Status": 200, "Message": "Product deleted!"}
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"Status": 404, "Message": "Product not found!"}


@app.get("/products/")
async def read_product_query(id: int | None = None, name: str | None = None, category: int | None = None, status: Status | None = None):
    to_send = []
    print (name)
    for item in database:
        if (type(item) is Product):
            if (id):
                if (item.id == id):
                    return item
            else:
                if (name and category and status):
                    if (item.name == name and item.category.id == category and item.status == status):
                        to_send.append(item)
                elif (name and category):
                    if (item.name == name and item.category.id == category):
                        to_send.append(item)
                elif (name and status):
                    if (item.name == name and item.status == status):
                        to_send.append(item)
                elif (category and status):
                    if (item.category.id == category and item.status == status):
                        to_send.append(item)
                elif (name):
                    if (item.name == name):
                        to_send.append(item)
                elif (category):
                    if (item.category.id == category):
                        to_send.append(item)
                elif (status):
                    if (item.status == status):
                        to_send.append(item)

    if (len(to_send) == 0):
        return {"Status": 404, "Message": "No Products found!"}
    else:
        return to_send


@app.get("/articles/{id_product}")
async def get_product_article(id_product: int, response: Response):
    to_send = []
    for item in database:
        if (type(item) is Article and item.product_id == id_product):
            to_send.append(item)

    if (len(to_send) == 0):
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"Status": 404, "Message": "No articles for this product id!"}
    else:
        response.status_code = status.HTTP_202_ACCEPTED
        return to_send


@app.post("/articles")
async def insert_article(article : Article, response: Response):
    for item in database:
        if (type(item) is Article):
            if (item.id == article.id):
                response.status_code = status.HTTP_400_BAD_REQUEST
                return {"Status": 400, "Message": "This article is already in the database"}
            elif (item.product_id == article.product_id):
                response.status_code = status.HTTP_404_NOT_FOUND
                return {"Status": 404, "Message": "Product id provided not found!"}
    database.append(article)
    response.status_code = status.HTTP_201_CREATED
    return article


@app.put("/articles/{id}")
async def update_article(id: int, article: Article, response: Response):
    for item in database:
        if (type(item) is Article):
            if (item.id == id):
                item.id = article.id
                item.product_id = article.product_id
                item.key = article.key
                response.status_code = status.HTTP_200_OK
                return item
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"Status": 404, "Message": "Article not found!"}


@app.delete("/articles/{id}")
async def delete_article(id : int, response: Response):
    for item in database:
        if (type(item) is Article):
            if (item.id == id):
                database.remove(item)
                response.status_code = status.HTTP_200_OK
                return {"Status": 200, "Message": "Article deleted!"}
            else:
                response.status_code = status.HTTP_404_NOT_FOUND
                return {"Status": 404, "Message": "Article not found!"}


# Requires pip install python-multipart
@app.post("/Image/{id}")
async def upload_image(id: int, response: Response, file: bytes = File(...)):
    name = str(uuid.uuid4())
    url = 'images/' + name + ".png"

    for item in database:
        if (type(item) is Product):
            if (item.id == id):
                if (item.image == None):
                    with open(url,'wb') as image:
                        image.write(file)
                        image.close()
                    item.image = name
                    response.status_code = status.HTTP_200_OK
                    return "Image " + name + " was added to product with id " + str(id)
                else:
                    response.status_code = status.HTTP_400_BAD_REQUEST
                    return {"Status": 400, "Message": "This Product already was an image"}
    
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"Status": 404, "Message": "This Product was not found!"}


@app.put("/Image/{id}")
async def update_image(id: int, response: Response, file: bytes = File(...)):
    name = str(uuid.uuid4())
    url = 'images/' + name + ".png"

    for item in database:
        if (type(item) is Product):
            if (item.id == id):
                if (item.image != None):
                    with open(url,'wb') as image:
                        image.write(file)
                        image.close()
                    item.image = name
                    response.status_code = status.HTTP_200_OK
                    return "Image " + name + " was updated to product with id " + str(id)
                else:
                    response.status_code = status.HTTP_400_BAD_REQUEST
                    return {"Status": 400, "Message": "This Product doesn't have an image"}
    
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"Status": 404, "Message": "This Product was not found!"}


@app.get("/Image/{id}")
async def get_image(id: int, response: Response):
    for item in database:
        if (type(item) is Product):
            if (item.id == id):
                if (item.image != None):
                    image_name = item.image
                    image_url = 'images/' + image_name + '.png'
                    response.status_code = status.HTTP_200_OK
                    return FileResponse(path=image_url, filename=image_name, media_type='image/png')
                else:
                    response.status_code = status.HTTP_404_NOT_FOUND
                    return {"Status": 404, "Message": "No image found for this product"}    

    response.status_code = status.HTTP_404_NOT_FOUND
    return {"Status": 404, "Message": "Product not found!"}