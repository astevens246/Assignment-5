from flask import Flask, request, redirect, render_template, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from pymongo.mongo_client import MongoClient
import certifi
# Use certifi to locate the CA certificate file
ca = certifi.where()

# MongoDB connection URI (replace with your actual credentials)
uri = "mongodb+srv://astevens2:<3A2pny1t1rvIsbdK>@astevens2.hw53pfi.mongodb.net/?retryWrites=true&w=majority"

############################################################
# SETUP
############################################################

app = Flask(__name__)

# Configure the Flask app with PyMongo
app.config["MONGO_URI"] = "mongodb://localhost:27017/plantsDatabase"
mongo = PyMongo(app)

############################################################
# ROUTES
############################################################

@app.route('/')
def plants_list():
    """Display the plants list page."""
    # TODO: Replace the following line with a database call to retrieve *all*
    # plants from the Mongo database's `plants` collection.
    plants_data = mongo.db.plants.find()

    context = {
        'plants': plants_data,
    }
    return render_template('plants_list.html', **context)

@app.route('/about')
def about():
    """Display the about page."""
    return render_template('about.html')

@app.route('/create', methods=['GET', 'POST'])
def create():
    """Display the plant creation page & process data from the creation form."""
    if request.method == 'POST':
        # TODO: Get the new plant's name, variety, photo, & date planted, and 
        # store them in the object below.
        new_plant = {
            'name': request.form.get('plant_name'),  # Use 'plant_name' from the form
            'variety': request.form.get('variety'),
            'photo_url': request.form.get('photo'),
            'date_planted': request.form.get('date_planted')
        }
        # TODO: Make an `insert_one` database call to insert the object into the
        result = mongo.db.plants.insert_one(new_plant)

        # database's `plants` collection, and get its inserted id. Pass the 
        # inserted id into the redirect call below.
        return redirect(url_for('detail', plant_id=result.inserted_id))

    else:
        return render_template('create.html')

@app.route('/plant/<plant_id>')
def detail(plant_id):
    """Display the plant detail page & process data from the harvest form."""
    
    # Use the ObjectId from bson to convert the plant_id string to ObjectId
    plant_to_show = mongo.db.plants.find_one({'_id': ObjectId(plant_id)})

    # TODO: Use the `find` database operation to find all harvests for the
    # plant's id.
    # HINT: This query should be on the `harvests` collection, not the `plants`
    # collection.
    harvests = mongo.db.harvests.find({'plant_id': ObjectId(plant_id)})

    context = {
        'plant': plant_to_show,
        'harvests': harvests
    }
    return render_template('detail.html', **context)


@app.route('/harvest/<plant_id>', methods=['POST'])
def harvest(plant_id):
    """
    Accepts a POST request with data for 1 harvest and inserts into database.
    """
    # TODO: Create a new harvest object by passing in the form data from the
    # detail page form.
    new_harvest = {
        'quantity': request.form.get('harvested_amount'),
        'date': request.form.get('date_planted'),
        'plant_id': plant_id
    }

    # TODO: Make an `insert_one` database call to insert the object into the 
    # `harvests` collection of the database.
    mongo.db.harvests.insert_one(new_harvest)

    return redirect(url_for('detail', plant_id=plant_id))

@app.route('/edit/<plant_id>', methods=['GET', 'POST'])
def edit(plant_id):
    """Shows the edit page and accepts a POST request with edited data."""
    if request.method == 'POST':
        # TODO: Make an `update_one` database call to update the plant with the
        # given id. Make sure to put the updated fields in the `$set` object.
        updated_data = {
            'name': request.form.get('plant_name'),
            'variety': request.form.get('variety'),
            'photo_url': request.form.get('photo'),
            'date_planted': request.form.get('date_planted')
        }
        mongo.db.plants.update_one({'_id': plant_id}, {'$set': updated_data})
        
        return redirect(url_for('detail', plant_id=plant_id))
    else:
        # TODO: Make a `find_one` database call to get the plant object with the
        # passed-in _id.
        plant_to_show = mongo.db.plants.find_one({'_id': plant_id})

        context = {
            'plant': plant_to_show
        }

        return render_template('edit.html', **context)

@app.route('/delete/<plant_id>', methods=['POST'])
def delete(plant_id):
    # Convert the plant_id to ObjectId
    plant_id_object = ObjectId(plant_id)

    # TODO: Make a `delete_one` database call to delete the plant with the given
    # id.
    mongo.db.plants.delete_one({'_id': plant_id_object})

    # TODO: Also, make a `delete_many` database call to delete all harvests with
    # the given plant id.
    mongo.db.harvests.delete_many({'plant_id': plant_id_object})

    return redirect(url_for('plants_list'))


if __name__ == '__main__':
    app.run(debug=True)
