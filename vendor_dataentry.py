#from flask import Flask, flash, render_template,request,redirect,url_for # For flask implementation
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from wtforms import Form, StringField, TextAreaField, PasswordField, RadioField, validators
from pymongo import MongoClient # Database connector
from bson.objectid import ObjectId # For ObjectId to work

client = MongoClient('localhost', 27017)    #Configure the connection to the database
db = client.mdh      #Select the database
vendors = db.vendors #Select the collection

#APP settings
app = Flask(__name__)
app.secret_key = "secret_key_1234566"

title = "MDH metadata manager"
heading = "Vendor Details"
#modify=ObjectId()

# Vendor Form Class
class VendorForm(Form):
    name = StringField('name', [validators.Length(min=1)])
    code = StringField('code', [validators.Length(min=1,max=10)])
    desc = TextAreaField('desc', [validators.Length(min=30)])


def redirect_url():
    return request.args.get('next') or \
           request.referrer or \
           url_for('index')

@app.route("/list")
def lists ():
	#Display the all Vendors
	vendors_l = vendors.find()
	a1="active"
	return render_template('index.html',a1=a1,vendors=vendors_l,t=title,h=heading)

@app.route("/")
@app.route("/uncompleted")
def tasks ():
	#Display the Uncompleted Vendors
	vendors_l = vendors.find({"done":"no"})
	a2="active"
	return render_template('index.html',a2=a2,vendors=vendors_l,t=title,h=heading)


@app.route("/completed")
def completed ():
	#Display the Completed Tasks
	vendors_l = vendors.find({"done":"yes"})
	a3="active"
	return render_template('index.html',a3=a3,vendors=vendors_l,t=title,h=heading)

@app.route("/done")
def done ():
	#Done-or-not ICON
	id=request.values.get("_id")
	task=vendors.find({"_id":ObjectId(id)})
	if(task[0]["done"]=="yes"):
		vendors.update({"_id":ObjectId(id)}, {"$set": {"done":"no"}})
	else:
		vendors.update({"_id":ObjectId(id)}, {"$set": {"done":"yes"}})
	redir=redirect_url()	# Re-directed URL i.e. PREVIOUS URL from where it came into this one

#	if(str(redir)=="http://localhost:5000/search"):
#		redir+="?key="+id+"&refer="+refer
	return redirect(redir)

#@app.route("/add")
#def add():
#	return render_template('add.html',h=heading,t=title)

@app.route("/action2")
def about2():
	return render_template('add.html',t=title,h=heading)

# THIS IS TO ADD A NEW VENDOR
@app.route("/action", methods=['POST'])
def action ():
    form = VendorForm(request.form)

    if request.method == 'POST' and form.validate():
        name = form.name.data
        # code = form.code.data
        # desc = form.desc.data
        # contactname = form.desc.data

    #Adding a new Vendor
    name=request.values.get("name")
    code=request.values.get("code")
    desc=request.values.get("desc")
    date=request.values.get("date")
    cd1=request.values.get("contactname")
    cd2=request.values.get("contactmail")
    cd3=request.values.get("contactweb")
    pr=request.values.get("pr")

    vendors.insert({ "name":name, "code":code, "desc":desc, "date":date, "pr":pr, "done":"no", "contactname":cd1, "contactemail":cd2, "contactweb":cd3})
    flash('Vendor Added', 'yellow')
    return redirect("/")
    # return render_template('list.html',h=heading,t=title)
    # return redirect(url_for('lists'))
    # return render_template('add.html',h=heading,t=title)

# def action():
#     render_template('add2.html',h=heading,t=title)


@app.route("/remove")
def remove ():
	#Deleting a Task with various references
	key=request.values.get("_id")
	vendors.remove({"_id":ObjectId(key)})
	flash('Vendor Removed', 'yellow')
	return redirect("/")

@app.route("/update")
def update ():
	id=request.values.get("_id")
	task=vendors.find({"_id":ObjectId(id)})
	return render_template('update.html',tasks=task,h=heading,t=title)

@app.route("/action3", methods=['POST'])
def action3 ():
	#Updating a Task with various references
	name=request.values.get("name")
	code=request.values.get("code")
	desc=request.values.get("desc")
	date=request.values.get("date")
	cd1=request.values.get("contactname")
	cd2=request.values.get("contactmail")
	cd3=request.values.get("contactweb")
	pr=request.values.get("pr")

	id=request.values.get("_id")
	# vendors.update({"_id":ObjectId(id)}, {'$set':{ "name":name, "code":code, "desc":desc, "date":date, "pr":pr }})
	vendors.update({"_id":ObjectId(id)}, {'$set':{ "name":name, "code":code, "desc":desc, "date":date, "pr":pr, "done":"no", "contactname":cd1, "contactemail":cd2, "contactweb":cd3}})

	return redirect("/")

@app.route("/search", methods=['GET'])
def search():
	#Searching a Task with various references
	key=request.values.get("key")
	refer=request.values.get("refer")
	if(key=="_id"):
		vendors_l = vendors.find({refer:ObjectId(key)})
	else:
		vendors_l = vendors.find({refer:key})
	return render_template('searchlist.html',vendors=vendors_l,t=title,h=heading)

@app.route("/about")
def about():
	return render_template('credits.html',t=title,h=heading)



if __name__ == "__main__":
    app.run(debug=True)
# Careful with the debug mode..
