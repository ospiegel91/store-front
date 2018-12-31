from bottle import route, run, template, static_file, get, post, delete, request
from sys import argv
import sys
import os
import json
import pymysql


connection = pymysql.connect(host='localhost',
                             user='root',
                             password='hard2figureout',
                             db='store_front',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)


@get("/admin")
def admin_portal():
    return template("pages/admin.html")


@get("/")
def index():
    return template("index.html")


@get('/js/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root='js')


@get('/css/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='css')


@get('/images/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root='images')


@post("/category")
def create_category():
    try:
        with connection.cursor() as cursor:
            newcatname = request.forms.get("name");
            sql2 = "SELECT name FROM categories"
            cursor.execute(sql2)
            results = cursor.fetchall()
            if(newcatname==""):
                object = {
                    'STATUS': 'ERROR',
                    'MSG': "Name parameter is missing",
                    "CAT_ID": "",
                    'CODE': "400"
                }
                return json.dumps(object)
            if newcatname in [d['name'].lower() for d in results]:
                object = {
                    'STATUS': 'ERROR',
                    'MSG': "Category already exists ",
                    "CAT_ID": "",
                    'CODE': "200"
                }
                return json.dumps(object)
            else:
                sql = "INSERT INTO categories VALUES({},'{}')".format("NULL", newcatname)
                cursor.execute(sql)
                object = {
                    'STATUS': 'SUCCESS',
                    'MSG': "category created successfully",
                    'CAT_ID': cursor.lastrowid,
                    'CODE': "201"
                }
                return json.dumps(object)
    except:
        object = {
            'STATUS': 'ERROR',
            'MSG': "internal error",
            "CATEGORIES": "",
            'CODE': "500"
        }
        return json.dumps(object)


@delete('/category/<id>')
def delete_category(id):
    try:
        with connection.cursor() as cursor:
            sql2 = "SELECT id FROM categories"
            cursor.execute(sql2)
            results = cursor.fetchall()
            if int(id) in [d['id'] for d in results]:
                sql = "DELETE FROM categories WHERE id={}".format(int(id))
                print(sql)
                cursor.execute(sql)
                sql2 = "SELECT * FROM categories"
                cursor.execute(sql2)
                table_1_mock = cursor.fetchall()
                print(table_1_mock)
                object = {
                    'STATUS': 'SUCCESS',
                    'MSG': "category deleted successfully",
                    'CODE': "201"
                }
                return json.dumps(object)
            else:
                object = {
                    'STATUS': 'ERROR',
                    'MSG': "category not found",
                    'CODE': "404"
                }
                return json.dumps(object)
    except:
        object = {
            'STATUS': 'ERROR',
            'MSG': "internal error",
            "CATEGORIES": "",
            'CODE': "500"
        }
        return json.dumps(object)


@get('/category/<id>/products')
def get_products_by_category(id):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM products WHERE category={}".format(id)
            cursor.execute(sql)
            results = cursor.fetchall()
            if int(id) in [d['category'] for d in results]:
                object = {
                    'STATUS': 'SUCCESS',
                    'MSG': "",
                    'PRODUCTS': results,
                    'CODE': "201"
                }
                return json.dumps(object)
            else:
                object = {
                    'STATUS': 'ERROR',
                    'MSG': "category not found",
                    'CODE': "404"
                }
                return json.dumps(object)
    except:
        object = {
            'STATUS': 'ERROR',
            'MSG': "internal error",
            "CATEGORIES": "",
            'CODE': "500"
        }
        return json.dumps(object)


@get('/categories')
def get_categories():
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM categories"
            cursor.execute(sql)
            results = cursor.fetchall()
            object = {
                'STATUS': 'SUCCESS',
                'MSG': "",
                'CATEGORIES': results,
                'CODE': "200"
            }
            return json.dumps(object)
    except:
        object = {
            'STATUS': 'ERROR',
            'MSG': "internal error",
            "CATEGORIES": "",
            'CODE': "500"
        }
        return json.dumps(object)


def get_category_name_by_id(id):
    try:
        with connection.cursor() as cursor:
            sql_categories = "SELECT * FROM categories"
            cursor.execute(sql_categories)
            categories = cursor.fetchall()
            for category in categories:
                if category['id'] == int(id):
                    return category['name']
                else:
                    return None
    except:
        return None


def edit_product(form, product_id):
    update_desc(form, product_id)
    update_px(form, product_id)
    update_img(form, product_id)
    update_fav(form, product_id)


def update_desc(form, product_id):
    try:
        with connection.cursor() as cursor:
            sql_desc = "UPDATE products SET description = '{}' WHERE id = {}".format(form['product_desc'], int(product_id))
            cursor.execute(sql_desc)
            connection.commit()
    except TypeError as e:
        print("error happened")
        print(e)
        return 'error'


def update_px(form, product_id):
    try:
        with connection.cursor() as cursor:
            sql_price = "UPDATE products SET price = {} WHERE id = {}".format(int(form['product_price']),int(product_id))
            cursor.execute(sql_price)
            connection.commit()
    except TypeError as e:
        print("error happened")
        print(e)
        return 'error'


def update_img(form, product_id):
    try:
        with connection.cursor() as cursor:
            sql_img = "UPDATE products SET img_url = '{}' WHERE id = {}".format(form['product_img'], int(product_id))
            cursor.execute(sql_img)
            connection.commit()
    except TypeError as e:
        print("error happened")
        print(e)
        return 'error'


def update_fav(form, product_id):
    try:
        with connection.cursor() as cursor:
            if form['product_isFav'] == 'on':
                sql_favorite = "UPDATE products SET favorite = '{}' WHERE id = {}".format('1', int(product_id))
            else:
                sql_favorite = "UPDATE products SET favorite = '{}' WHERE id = {}".format('0', int(product_id))
            cursor.execute(sql_favorite)
            connection.commit()
    except TypeError as e:
        print("error happened")
        print(e)
        return 'error'


def create_product(form):
    try:
        with connection.cursor() as cursor:
            if form['product_isFav'] == 'on':
                x_favorite = 1
            else:
                x_favorite = 0
            sql_create = 'INSERT INTO products VALUES(Null,"{}","{}",{},"{}",{},{})'\
                .format(form['product_title'],form['product_desc'],form['product_price'], form['product_img'],
                        form['product_category_id'], x_favorite)
            print(sql_create)
            cursor.execute(sql_create)
            connection.commit()
            return cursor.lastrowid
    except TypeError as e:
        print("error happened")
        print(e)
        return 'error'


@get('/product/<id>')
def get_product(id):
    try:
        with connection.cursor() as cursor:
            sql2 = "SELECT id FROM products"
            cursor.execute(sql2)
            results = cursor.fetchall()
            if int(id) in [d['id'] for d in results]:
                get_produt_sql = "SELECT id FROM products WHERE id={}".format(id)
                cursor.execute(get_produt_sql)
                result = cursor.fetchone()
                print(result)
                object = {
                    'STATUS': 'SUCCESS',
                    'MSG': "product fetched successfully",
                    'PRODUCT': result,
                    'CODE': "201"
                }
                return json.dumps(object)
            else:
                object = {
                    'STATUS': 'ERROR',
                    'MSG': "product not found",
                    'PRODUCT':"",
                    'CODE': "404"
                }
                return json.dumps(object)
    except:
        object = {
            'STATUS': 'ERROR',
            'MSG': "internal error",
            "PRODUCT": "",
            'CODE': "500"
        }
        return json.dumps(object)


@delete('/product/<id>')
def delete_product(id):
    try:
        with connection.cursor() as cursor:
            sql2 = "SELECT id FROM products"
            cursor.execute(sql2)
            results = cursor.fetchall()
            if int(id) in [d['id'] for d in results]:
                sql = "DELETE FROM products WHERE id={}".format(int(id))
                print(sql)
                cursor.execute(sql)
                sql2 = "SELECT * FROM products"
                cursor.execute(sql2)
                table_1_mock = cursor.fetchall()
                print(table_1_mock)
                object = {
                    'STATUS': 'SUCCESS',
                    'MSG': "product deleted successfully",
                    'CODE': "201"
                }
                return json.dumps(object)
            else:
                object = {
                    'STATUS': 'ERROR',
                    'MSG': "product not found",
                    'CODE': "404"
                }
                return json.dumps(object)
    except:
        object = {
            'STATUS': 'ERROR',
            'MSG': "internal error",
            "CATEGORIES": "",
            'CODE': "500"
        }
        return json.dumps(object)


@get('/products')
def get_products():
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM products"
            cursor.execute(sql)
            results = cursor.fetchall()
            object = {
                'STATUS': 'SUCCESS',
                'MSG': "",
                'PRODUCTS': results,
                'CODE': "200"
            }
            return json.dumps(object)
    except:
        object = {
            'STATUS': 'ERROR',
            'MSG': "internal error",
            "PRODUCTS": "",
            'CODE': "500"
        }
        return json.dumps(object)


@post('/product')
def add_edit_product():
    try:
        with connection.cursor() as cursor:
            product_form_obj = {
                'product_title': request.forms.get("title"),
                'product_desc': request.forms.get("desc"),
                'product_price': request.forms.get("price"),
                'product_img': request.forms.get("img_url"),
                'product_category_id': request.forms.get("category"),
                'product_isFav': request.forms.get("favorite")
            }
            sql_products = "SELECT * FROM products"
            cursor.execute(sql_products)
            products = cursor.fetchall()
            if product_form_obj['product_category_id'] is None:
                object = {
                    'STATUS': 'ERROR',
                    'MSG': "category not found",
                    'PRODUCT_ID': "",
                    'CODE': "404"
                }
                return json.dumps(object)
            is_in_list = False
            for product in products:
                if product['title'].lower() == product_form_obj['product_title'].lower() \
                        and int(product['category']) == int(product_form_obj['product_category_id']):
                    product_id = product['id']
                    is_in_list = True
            if is_in_list:
                edit_product(product_form_obj,product_id)
                object = {
                    'STATUS': 'SUCCESS',
                    'MSG': "product created/updated successfully",
                    "PRODUCT_ID": product_id,
                    'CODE': "201"
                }
                return json.dumps(object)
            else:
                newproduct_id = create_product(product_form_obj)
                object = {
                    'STATUS': 'SUCCESS',
                    'MSG': "product created/updated successfully",
                    "PRODUCT_ID": newproduct_id,
                    'CODE': "201"
                }
                return json.dumps(object)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        object = {
            'STATUS': 'ERROR',
            'MSG': "internal error",
            "PRODUCT_ID": "",
            'CODE': "500"
        }
        return json.dumps(object)


run(host='0.0.0.0', port=7000)
