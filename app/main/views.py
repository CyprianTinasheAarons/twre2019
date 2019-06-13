from datetime import datetime,date
from flask import render_template, session, redirect, url_for,request,current_app,abort,flash 
from . import main
from flask_pymongo import pymongo ,MongoClient
from flask_login import login_required
from .forms import PostForm,PropertyForm,EditProfileForm,CommentForm,EditProfileAdminForm,SearchForm
from flask_login import current_user
from app import  images 
from werkzeug import secure_filename
from functools import wraps



client = pymongo.MongoClient("mongodb+srv://twre:qwertyuiop@cluster0-igeuf.mongodb.net/test?retryWrites=true&w=majority")
mongo= client.twredb

try:
    print("MongoDB version is %s" %
            client.server_info()['version'])
except pymongo.errors.OperationFailure as error:
    print(error)
    quit(1)


def admin_required(f):
    @wraps(f)
    def  wrap(*args, **kwargs):
        users = mongo.db.Users
        query= users.find({'email': session['email'] },{'role':'1'})
        for i in query:
            dbRole = i['role']
            if dbRole != 'admin':
                    return redirect(url_for('auth.login', next=request.url))
            else:
                return f(*args, **kwargs)
    return wrap

def getNextSequence(collection,name):
    return collection.find_and_modify(query= { '_id': name },update= { '$inc': {'seq': 1}}, new=True ).get('seq')

def search(collection,search_text):
    return collection.find({"$text": {"$search": search_text}}).limit(10)

def delete(collection,uniqueid):
    return collection.remove({'_id': uniqueid})

#Main pages of twre site
@main.route('/', methods=['GET','POST'])
@main.route('/home', methods=['GET','POST'])
def home():
    estates =[]
    
    query = mongo.db.Estates.find({}, {"_id":"1" ,"Title":"1", "Category":"1","Price":"1" ,"Address":"1" ,"Photos": "1"  }).limit(8).sort("_id" ,-1)
    
 
    for i in query:
        _id =i['_id']
        title = i['Title']
        category = i['Category'] 
        price = i['Price']
        address = i['Address']
        image = i['Photos']
        estates.append([ _id,title, category , price , address , image])

    return render_template('home.html', estates=estates )
 
@main.route('/properties',  methods=['GET','POST'])
def properties():
    estatesDB=mongo.db.Estates
    estates =[]
   

    query=estatesDB.find({},{"_id":"1" ,"Title":"1", "Category":"1","Price":"1" ,"Address":"1" ,"Photos": "1"  }).sort("_id" ,-1)

    for i in query:
        _id = i['_id']
        title = i['Title']
        category = i['Category'] 
        price = i['Price']
        address = i['Address']
        photos = i['Photos']
        estates.append([ _id,title, category , price , address , photos])

    form = SearchForm()
   

     
    return render_template('properties.html', estates=estates , form=form  )

@main.route('/properties/search',  methods=['GET','POST'])
def properties_search():
    estatesSearch=[]
    form = SearchForm()
    if form.validate_on_submit():
        searchQuery=search( mongo.db.Estates, search_text = request.form['search'])
        for i in searchQuery:
            _id =i['_id']
            title = i['Title']
            category = i['Category'] 
            price = i['Price']
            address = i['Address']
            image = i['Photos']
            estatesSearch.append([ _id,title, category , price , address , image])
   
    return render_template('properties.html', form=form , estatesSearch=estatesSearch )
    
@main.route('/blog',methods=['GET','POST'])
def blog():
    posts = []
    postsSearch=[]
    query = mongo.db.Posts.find({},{"_id": "1" , "Title": "1" ,"Summary": "1" , "Image_url" : "" }).sort('_id' , -1)
    for  i in query:
        _id = i['_id']
        title = i['Title']
        summary = i['Summary']
        image = i['Image_url']
        posts.append([_id ,title , summary ,image ])

    form = SearchForm()
  
    
    return render_template('blog.html' ,posts=posts  , form=form )


@main.route('/blog/search' ,methods=['GET','POST'])
def blog_search():
    postsSearch=[]
    form = SearchForm()
    if form.validate_on_submit():
        searchQuery=search( mongo.db.Posts, search_text = request.form['search'])
        for i in searchQuery:
            _id =i['_id']
            title = i['Title']
            summary = i['Summary'] 
            image = i['Image_url']
            postsSearch.append([ _id,title,summary, image]
            )

    return render_template('blog.html' ,postsSearch=postsSearch , form=form )

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/user')
def user():
    query = mongo.db.Users.find({'email' : session['email'] },{'username': '1', 'email': '1', 'name': '1','location': '1','about_me' : '1'})
    user ={}
    for i in query:
        user={
            'username' :  i['username'],
            'email' : i['email'],
            'name' : i['name'],
            'location' : i['location'],
        'about_me' : i['about_me']
        }
    if user is None:
        abort(404)
    return render_template('user.html' , user=user)

@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    query = mongo.db.Users.find({'email': session['email']},{'_id': '1' ,'password':'1', 'email': '1', 'username': '1', 'name': '1' , 'location': '1', 'about_me': '1' ,'role': '1', 'Date':'1'})
    for i in query:
        oldId = i['_id']
        oldPassword = i['password']
        oldEmail  = i['email']
        oldUsername = i['username']
        oldName = i['name']
        oldLocation = i['location']
        oldAboutme = i['about_me']
        oldRole = i['role']
        date = i['Date']
  
    form = EditProfileForm( )
    if form.validate_on_submit():
        mongo.db.Users.update( {'_id':oldId},{'_id': oldId, 'password': oldPassword, 'email' : oldEmail, 'username' : oldUsername,'name': request.form['name'], 'location' : request.form['location'],'about_me' : request.form['about_me'] ,'role':  oldRole, 'Date' : date , 'Edit-date': datetime.now()})
        flash('Your profile has been updated.')
        return redirect(url_for('.user'))
    
    form.name.data = oldName
    form.location.data = oldLocation
    form.about_me.data = oldAboutme
    
    return render_template('edit_profile.html', form=form)   

@main.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    query = mongo.db.Posts.find({"_id": id }, {"_id":"1", "Title":"1", "Body":"1"  ,"Image_url": "1" , "Date" : "1"   })
    post ={}

    for i in query:
        post={
        '_id' :i['_id'],
       'title' :i['Title'],
        'body_html':i['Body'],
        'image' :i['Image_url'],
        'date':i['Date']
        }
    form = CommentForm()
    return render_template('post.html', post=post , form=form)

@main.route('/property/<int:id>', methods=['GET', 'POST'])
def property(id):
    query = mongo.db.Estates.find({"_id": id }, {"_id":"1", "Title":"1", "Category":"1","Price":"1" ,"Address":"1", "Body" :"1" ,"Photos": "1"   })
    estate = {}

    for i in query:
        estate = {
            '_id': i['_id'],
            'title': i['Title'] ,
            'category': i['Category'], 
            'price': i['Price'], 
            'address': i['Address'],
            'body': i['Body'], 
            'image': i['Photos']
        }
    
    return render_template('property.html', estate=estate )
#Administration dashboard of the website
@main.route('/admin')
@login_required
@admin_required
def admin(): 
    count_posts = mongo.db.Posts.count()
    count_estates = mongo.db.Estates.count()
    count_users = mongo.db.Users.count()
    return render_template('admin.html' , count_posts=count_posts,count_estates=count_estates,count_users=count_users )

@main.route('/admin/properties/search' ,methods=['GET' , 'POST'])
@login_required
@admin_required
def admin_properties_search():
    propertyList =[]
    form1 =SearchForm()
    form2=PropertyForm()
    if form1.validate_on_submit():
        searchQuery=search( mongo.db.Estates, search_text= request.form['search'])
        for i in searchQuery:
            _id = i['_id']
            authorName=i['Author']
            title = i['Title']
            category = i['Category'] 
            address = i['Address']
            price = i['Price']
            date = i['Date']
            propertyList.append([_id,title, category ,address , price , date ,authorName])
        
    return render_template('admin-properties.html' ,form1=form1, form2=form2,propertyList=propertyList )

@main.route('/admin/properties' ,methods=['GET' , 'POST'])
@login_required
@admin_required
def admin_properties():
    propertyList =[]
    form1 =SearchForm()
    query = mongo.db.Estates.find({},{"_id":"1" ,"Title":"1", "Category":"1","Price":"1" ,"Address":"1","Date": "1","Author" : "1"})
    for i in query:
            _id = i['_id']
            authorName=i['Author']
            title = i['Title']
            category = i['Category'] 
            address = i['Address']
            price = i['Price']
            date = i['Date']
            propertyList.append([_id,title, category ,address , price , date,authorName])

    
    form2 = PropertyForm()
    if form2.validate_on_submit():
        photo_file = {}
        photo_filenames=[]
        photo = request.files['images']
        for photo in form2.images.data:
            photo_filename = images.save(photo)
            photo_url = images.url(photo_filename)
            photo_file = {
                'name': photo_filename,
                'photo': photo_url
            }
            photo_filenames.append(photo_file)
        query1 = mongo.db.Users.find({'email': session['email'] },{'username': '1'})
        for i in query1:
            author=i['username']
        mongo.db.Estates.insert({ '_id': getNextSequence(mongo.db.Counters,"estateId"),'Author':author , 'Title' : request.form['title'], 'Category' : request.form['category'] ,'Address': request.form['address'],'Price': int(request.form['price']),'Body': request.form['body'],'Photos': photo_filenames ,'Date' : datetime.now()})
        return redirect(url_for('.properties'))
    return render_template('admin-properties.html',form1=form1, form2=form2, propertyList=propertyList )



@main.route('/admin/posts/search' ,methods=['GET' , 'POST'])
@login_required
@admin_required
def admin_posts_search():
    postsList =[]
    form1=SearchForm()
    form2=PostForm()
    if form1.validate_on_submit():
        searchQuery=search( mongo.db.Posts, search_text= request.form['search'])
        for i in searchQuery:
            _id = i['_id']
            title = i['Title']
            date = i['Date']
            postsList.append([ _id, title ,date])
    return render_template('admin-posts.html',form1=form1,form2=form2, postsList=postsList  )

@main.route('/admin/posts' ,methods=['GET' , 'POST'])
@login_required
@admin_required
def admin_posts():

    postsList =[]
    form1=SearchForm()
    query = mongo.db.Posts.find({},{"_id": "1" , "Title": "1" , "Date" : "1"})
    for  i in query:
        _id = i['_id']
        title = i['Title']
    
        date = i['Date']
        postsList.append([_id ,title , date ])
    form2 = PostForm()
    if form2.validate_on_submit(): 

        photo_filename =images.save(request.files['image'])
        photo_url = images.url(photo_filename)
        mongo.db.Posts.insert({ '_id': getNextSequence(mongo.db.Counters,"postId"),'Title' : request.form['title'], 'Summary' : request.form['summary'] ,'Body': request.form['body'],'Image_url': photo_url,'Image_filename':photo_filename , 'Date': datetime.now()})
        return redirect(url_for('.blog'))
    return render_template('admin-posts.html',form1=form1,form2=form2, postsList=postsList  )



@main.route('/admin/users/search' , methods=['GET', 'POST'])
@login_required
@admin_required
def admin_users_s():
    usersList=[]
    form = SearchForm()
    
    if form.validate_on_submit():
        searchQuery=search( mongo.db.Users, search_text= request.form['search'])
        for i in searchQuery:
            _id = i["_id"]
            username = i["username"]
            email = i["email"]
            date = i["Date"]
    
            usersList.append([ _id ,username,email ,date])
    return render_template('admin-users.html' ,usersList=usersList ,form=form )

@main.route('/admin/users' , methods=['GET', 'POST'])
@login_required
@admin_required
def admin_users():
    usersList=[]
    form = SearchForm()
    query = mongo.db.Users.find({}).sort("_id" ,-1)
    for i in query:
            _id = i["_id"]
            username = i["username"]
            email = i["email"]
            date = i["Date"]
            usersList.append([ _id ,username,email ,date])

    return render_template('admin-users.html' ,usersList=usersList ,form=form )

@main.route('/admin/user_delete/<int:id>', methods=[ 'GET','POST'])
@login_required
@admin_required
def delete_user (id):
    query = mongo.db.Users.find({'_id': id},{'email': '1'})
    for i in query:
        delete_email = i['email']
    if session['email'] == delete_email:
        flash('Warning: You Can Not  Delete Current User!')
        return redirect(url_for('.admin_users'))
    else:
        delete_query=delete(mongo.db.Users, uniqueid=id)

    return redirect(url_for('.admin_users'))

@main.route('/admin/property_edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_property (id):
    query = mongo.db.Estates.find({'_id' : id }, {"Author" : "1", "Title":"1", "Category":"1","Price":"1" ,"Address":"1", "Body" :"1" ,"Date": "1"})

    for i in query:
        oldAuthor = i['Author']
        oldTitle = i['Title'] 
        oldCategory = i['Category'] 
        oldPrice = i['Price']
        oldAddress = i['Address']
        oldBody = i['Body']
        date = i['Date']

    form = PropertyForm()
    if form.validate_on_submit():
        photo_file = {}
        photo_filenames=[]
        photo = request.files['images']
        for photo in form.images.data:
            photo_filename = images.save(photo)
            photo_url = images.url(photo_filename)
            photo_file = {
                'name': photo_filename,
                'photo': photo_url
            }
            photo_filenames.append(photo_file)
        
        query1 = mongo.db.Users.find({'email': session['email'] },{'username': '1'})
        for i in query1:
            author=i['username']

        mongo.db.Estates.update({'_id': id},{'Author': author,'Title': request.form['title']  , 'Category' : request.form['category'], 'Address' : request.form['address'] ,'Price': request.form['price'], 'Body' : request.form['body'], 'Photos': photo_filenames ,'Date' : date, 'Edit-Date': datetime.now() })
        flash('The property has been updated.')
        return redirect(url_for('main.property' , id= id))
    form.title.data = oldTitle
    form.price.data = oldPrice
    form.address.data = oldAddress
    form.body.data = oldBody
    return render_template('edit_property.html', form=form)

@main.route('/admin/property_delete/<int:id>', methods=[ 'GET','POST'])
@login_required
@admin_required
def delete_property (id):
    delete_query=delete(mongo.db.Estates, uniqueid=id)
    flash('The property has been deleted.')
    return redirect(url_for('.admin_properties'))



@main.route('/admin/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit(id):
    query =mongo.db.Posts.find({'_id': id},{ "Title": "1", "Summary": "1", "Body": "1" ,"Date":"1"
    })

    for  i in query:
        oldTitle = i['Title']
        oldSummary = i['Summary']
        oldBody = i['Body']
        date = i['Date']
    form = PostForm()
    if form.validate_on_submit():
        photo_filename =images.save(request.files['image'])
        photo_url = images.url(photo_filename)
        mongo.db.Posts.update({'_id':id},{'Title' : request.form['title'], 'Summary' : request.form['summary'], 'Body' : request.form['body'] ,'Image_url': photo_url,'Image_filename':photo_filename, 'Date': date ,'Edit-Date': datetime.now()})
        flash('The post has been updated.')
        return redirect(url_for('main.post', id=id))
    form.title.data = oldTitle
    form.summary.data = oldSummary
    form.body.data = oldBody
    return render_template('edit_post.html', form=form)

@main.route('/admin/post_delete/<int:id>', methods=[ 'GET','POST'])
@login_required
@admin_required
def delete_post (id):
    delete_query=delete(mongo.db.Posts, uniqueid=id)
    flash('The post has been deleted.')
    return redirect(url_for('.admin_posts'))

@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    query = mongo.db.Users.find({'_id' : id},{'_id': '1' ,'password':'1', 'email': '1', 'username': '1', 'name': '1' , 'location': '1', 'about_me': '1' , 'Date':'1'})
    for i in query:
        oldId = i['_id']
        oldPassword = i['password']
        oldEmail = i['email']
        oldUsername = i['username']
        oldName = i['name']
        oldLocation = i['location']
        oldAboutme = i['about_me']
        date = i['Date']

    form = EditProfileAdminForm( )
    if form.validate_on_submit():
        mongo.db.Users.update( {'_id':id},{'_id': oldId, 'password': oldPassword, 'email' : request.form['email'], 'username' : request.form['username'] ,'name': request.form['name'], 'location' : request.form['location'],'about_me' : request.form['about_me'] ,'role': request.form['role'] , 'Date' : date , 'Edit-date': datetime.now()})
        flash('The profile has been updated.')
        return redirect(url_for('.admin_users'))
    form.email.data = oldEmail
    form.username.data = oldUsername
    form.name.data = oldName
    form.location.data = oldLocation
    form.about_me.data = oldAboutme
    return render_template('edit_profile.html', form=form)
