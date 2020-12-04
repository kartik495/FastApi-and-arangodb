from fastapi import FastAPI,Request
from fastapi.responses import HTMLResponse
import requests as req
import json
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from arango.client import ArangoClient

db=0
app=FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get('/')
def d():
    return 'go to home page'

@app.get('/home',response_class=HTMLResponse)
def home(request:Request):
    return templates.TemplateResponse('home.html',{'request':request})

@app.get('/database/{password}')
def createdatabase(password):
    client = ArangoClient(hosts='http://localhost:8529')
    sys_db = client.db('_system', username='root', password=password)
    
    if   sys_db.has_database('Capstone'):
        sys_db.delete_database('Capstone')

    sys_db.create_database('Capstone')
    global db
    db = client.db('Capstone', username='root', password=password)                
    languagesCollection=db.create_collection('languages')
    programmingLang=['Python','Java','Dart','C++']
    for lang in programmingLang:
        data={'name':lang }
        languagesCollection.insert(data)
        
    coursesCollection=db.create_collection('courses')
    coursesName=['Beginner','Intermediate','Advance']
    for lang in programmingLang:
        for course in coursesName:
            data={'name':course+' '+lang,'language':lang,'vedio quality':0,'qalified instructor':0,'content quality':0,'course pace':0,'course depth and quality':0,'rating':0}
            coursesCollection.insert(data)
    return 'database created'

@app.get('/languages',response_class=HTMLResponse)
def home(request:Request):
    global db
    languagesCollection=db.collection('languages')
    lang=[]
    for doc in languagesCollection:
        lang.append(doc['name'])
 
    return templates.TemplateResponse('language.html',{'request':request,'languages':lang})
@app.get('/languages/{language}',response_class=HTMLResponse)
def home(request:Request,language):
    global db
    coursesCollection=db.collection('courses')
    courses=[]
    for doc in coursesCollection:
        if doc['language']==language:
            courses.append(doc)
 
    return templates.TemplateResponse('course.html',{'request':request,'courses':courses})


@app.get('/{key}/{x}/{no}')
def home(request:Request,key,x,no):
    
    global db
    coursesCollection=db.collection('courses')
    
    doc=coursesCollection.get( key)
    print(doc)
    if no=='1':
        doc[x]+=1
    else:
        doc[x]-=1
    coursesCollection.update(doc)

 
    return 'updated successfully'
