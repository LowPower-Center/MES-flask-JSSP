# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
#
from apps.data import blueprint,models
from apps.data.forms import CreateMaterialForm
from apps.data.models import *
import requests
from flask import render_template, request,jsonify
from flask_login import login_required
from jinja2 import TemplateNotFound
import random
import matplotlib.pyplot as plt

@blueprint.route('/order_chart_thisweek',methods=["GET","POST"])
@login_required
def data1():
    data=[]
    for i in range(7):
        data.append(random.randint(100,200))
    return jsonify(data)


@blueprint.route('/order_chart_lastweek',methods=["GET","POST"])
@login_required
def data2():
    data=[]
    for i in range(7):
        data.append(random.randint(50,100))
    return jsonify(data)

@blueprint.route('/material',methods=["GET","POST","PUT","DELETE"])
@login_required
def material():
    if "POST" in request.method:
        item=request.values
        material=RawMaterial()
        material.name=item["name"]
        material.number=item["number"]
        material.description=item["description"]
        db.session.add(material)
        db.session.commit()
        return material.test_schema()
    elif "PUT" in request.method:
        print("HERE")
        item_new=request.values
        item=RawMaterial.query.get(item_new["number"])
        item.name=item_new["name"]
        item.description=item_new["description"]
        db.session.commit()
        return item.test_schema()
    elif "DELETE" in request.method:
        item_new = request.values
        item = RawMaterial.query.get(item_new["number"])
        db.session.delete(item)
        db.session.commit()
        return "Success"
    data=RawMaterial.query.all()
    data=list(map(lambda x:x.test_schema(),data))
    return jsonify(data)


@blueprint.route('/product',methods=["GET","POST","PUT","DELETE"])
@login_required
def product():
    if "POST" in request.method:
        item=request.values
        product=Product()
        product.name=item["name"]
        product.number=item["number"]
        product.description=item["description"]
        product.technology=item["technology"]
        db.session.add(product)
        db.session.commit()
        return product.test_schema()
    elif "PUT" in request.method:
        print("HERE")
        item_new=request.values
        item=Product.query.get(item_new["number"])
        item.name=item_new["name"]
        item.description=item_new["description"]
        item.technology=item_new["technology"]
        db.session.commit()
        return item.test_schema()
    elif "DELETE" in request.method:
        item_new = request.values
        item = Product.query.get(item_new["number"])
        db.session.delete(item)
        db.session.commit()
        return "Success"
    data=Product.query.all()
    data=list(map(lambda x:x.test_schema(),data))
    return jsonify(data)

@blueprint.route('/plan',methods=["GET"])
@login_required
def get_plan():
    data1=Order.query.all()
    data1=list(map(lambda x:x.test_schema(),data1))
    data2=PathDetail.query.all()
    data2=list(map(lambda x:x.test_schema(),data2))
    res=requests.post("http://localhost:1880/jssp",json=(data1,data2),)
    str1=str(res.content.decode())

    s=str1.split("-")
    ret=s[0].replace("."," ").split("][")
    PT=(ret[0]+"]").replace(" ",",").replace("[",",").replace("]",",").replace("\n",",").split(",")
    MT=("["+ret[1]).replace(" ",",").replace("[",",").replace("]",",").replace("\n",",").split(",")
    ST=(s[4]).replace(" ",",").replace("[",",").replace("]",",").replace("\n",",").split(",")
    MT_item=[]
    PT_item=[]
    ST_item=[]
    for i in MT:
        if i:
            MT_item.append(i)
    for i in PT:
        if i:
            PT_item.append(i)
    for i in ST:
        if i :
            ST_item.append(i)
    # print(eval(PT))
    print(MT_item,PT_item,ST_item)
    markspan=eval(s[1])
    n=eval(s[2])
    m=eval(s[3])

    print(markspan,n,m)
    PT=[]
    MT=[]
    ST=[]
    for i in range(m):
        PT_tmp = []
        MT_tmp = []
        ST_tmp=[]
        for j in range(n):
            MT_tmp.append((eval(MT_item[i*n+j])//m,eval(MT_item[i*n+j])%m))
            ST_tmp.append(eval(ST_item[i * n + j]))
            PT_tmp.append(eval(PT_item[(eval(MT_item[i*n+j])//m)*m+(eval(MT_item[i*n+j])%m)]))
        PT.append(PT_tmp)
        MT.append(MT_tmp)
        ST.append(ST_tmp)
    print(MT,PT,ST)

    plt.rcParams['font.sans-serif'] = ['Times New Roman']  # 如果要显示中文字体,则在此处设为：SimHei
    plt.rcParams['axes.unicode_minus'] = False  # 显示负号
    M = ['red', 'blue', 'yellow', 'orange', 'green', 'palegoldenrod', 'purple', 'pink', 'Thistle', 'Magenta',
         'SlateBlue', 'RoyalBlue', 'Cyan', 'Aqua', 'floralwhite', 'ghostwhite', 'goldenrod', 'mediumslateblue',
         'navajowhite', 'navy', 'sandybrown', 'moccasin']
    Job_text = ['J' + str(i + 1) for i in range(100)]
    Machine_text = ['M' + str(i + 1) for i in range(50)]

    print(Job_text)
    for i in range(m):
        for j in range(len(ST[i])):
            if PT[i][j] - ST[i][j] != 0:
                plt.barh(i, width=PT[i][j] - ST[i][j],
                         height=0.8, left=ST[i][j],
                         color=M[MT[i][j][0]],
                         edgecolor='black')
                plt.text(x=ST[i][j] + (PT[i][j] - ST[i][j]) / 2 - 0.1,
                         y=i,
                         s=Job_text[MT[i][j][0]],
                         fontsize=12)
    plt.savefig("apps/static/gantti.png")
    plt.show()
    return "sucess"

@blueprint.route('/order',methods=["GET","POST","PUT","DELETE"])
@login_required
def order_list():
    if "POST" in request.method:
        item=request.values
        order=Order()
        order.name=item["name"]
        order.number=item["number"]
        order.description=item["description"]
        order.ordered=item["ordered"]
        db.session.add(order)
        db.session.commit()
        return order.test_schema()
    elif "PUT" in request.method:
        print("HERE")
        item_new=request.values
        item=Order.query.get(item_new["name"])
        item.name=item_new["number"]
        item.description=item_new["description"]
        item.ordered=item_new["ordered"]
        db.session.commit()
        return item.test_schema()
    elif "DELETE" in request.method:
        item_new = request.values
        item = Order.query.get(item_new["name"])
        db.session.delete(item)
        db.session.commit()
        return "Success"
    data=Order.query.all()
    data=list(map(lambda x:x.test_schema(),data))
    return jsonify(data)


@blueprint.route('/technology',methods=["GET","POST","PUT","DELETE"])
@login_required
def technology():
    if "POST" in request.method:
        item=request.values
        technology=PathDetail()
        technology.path=item["path"]
        technology.bom=item["bom"]
        db.session.add(technology)
        db.session.commit()
        return technology.test_schema()
    elif "PUT" in request.method:
        print("HERE")
        item_new=request.values
        item=PathDetail.query.get(item_new["path"])
        item.path=item_new["path"]
        item.bom=item_new["bom"]
        db.session.commit()
        return item.test_schema()
    elif "DELETE" in request.method:
        item_new = request.values
        item = PathDetail.query.get(item_new["path"])
        db.session.delete(item)
        db.session.commit()
        return "Success"
    data=PathDetail.query.all()
    data=list(map(lambda x:x.test_schema(),data))
    return jsonify(data)



# @blueprint.route('/technology/<id>',methods=["GET"])
# @login_required
# def tenology_get(id):
#     print("return a message")
#     data="This problem can't be solved now!"
#     return jsonify(data)









# @blueprint.route('/material/add',methods=["GET","POST"])
# @login_required
# def material_add():
#     data=RawMaterial()
#     data.number=random.randint(0,100000000)
#     data.img="None"
#     data.name="test"
#     db.session.add(data)
#     db.session.commit()
#     return "sucess"

#
#
# @blueprint.route("/test",methods=["GET","POST"])
# def test():
#     print (request.data)
#     content = request.get_json()
#     print (content)
#     return 'JSON posted'
#
#
# @blueprint.route('/test_data',methods=["GET","POST"])
# def data3():
#     data3=[10,20,30,40,50,60,70]
#     return jsonify(data3)
#
# @blueprint.route('/add_raw_material',methods=["GET","POST"])
# def add_raw_material():
#     create_raw_material_form = CreateMaterialForm(request.form)
#     if 'submit' in request.form:
#         name = request.form['name']
#         number = request.form['number']
#         img=request.form['img']
#
#         # Check usename exists
#         material = RawMaterial.query.filter_by(name=name).first()
#         if material:
#             return render_template('#',
#                                    msg='name already registered',
#                                    success=False,
#                                    form=create_raw_material_form)
#
#         # Check number exists
#         material = RawMaterial.query.filter_by(number=number).first()
#         if material:
#             return render_template('#',
#                                    msg='number already registered',
#                                    success=False,
#                                    form=create_raw_material_form)
#
#         # else we can create the material
#         material = RawMaterial(**request.form)
#         db.session.add(material)
#         db.session.commit()
#
#         return render_template('#',
#                                msg='material created please <a href="/login">login</a>',
#                                success=True,
#                                form=create_raw_material_form)
#
#     else:
#         return render_template('accounts/register.html', form=create_raw_material_form)

