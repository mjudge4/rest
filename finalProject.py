#import Flask class from the flask library
from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database_create import Base, Restaurant, MenuItem

#create an instance of this class with the name of the running application as the argument
app = Flask(__name__)

#Creates the database and adds tables and columns
engine = create_engine('sqlite:///restaurantMenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
    items = session.query(Restaurant).all()
    return render_template('restaurant.html', items = items)

#Making an API Endpoint (GET Request)
@app.route('/restaurants/JSON')
def showRestaurantsJSON():
    items = session.query(Restaurant).all()
    return jsonify(Restaurants=[i.serializeRest for i in items])

@app.route('/restaurant/new/', methods = ['GET','POST'])
def newRestaurant():
    if request.method == 'POST':
        newRestaurant = Restaurant(name = request.form['name'])
        session.add(newRestaurant)
        session.commit()
        flash(newRestaurant.name + " created")
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('newrestaurant.html')

@app.route('/restaurant/<int:restaurant_id>/edit/', methods = ['GET','POST'])
def editRestaurant(restaurant_id):
    editedRestaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedRestaurant.name = request.form['name']
        session.add(editedRestaurant)
        session.commit()
        flash(editedRestaurant.name + " edited")
        return redirect(url_for('showRestaurants'))
                        
    else:                    
        return render_template('editrestaurant.html', restaurant_id = restaurant_id, editedRestaurant = editedRestaurant)

@app.route('/restaurant/<int:restaurant_id>/delete/', methods = ['GET','POST'])
def deleteRestaurant(restaurant_id):
    deletedRestaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST':
        session.delete(deletedRestaurant)
        session.commit()
        flash(deletedRestaurant.name + " deleted")
        return redirect(url_for('showRestaurants'))
                        
    else:                    
        return render_template('deleterestaurant.html', restaurant_id = restaurant_id, deletedRestaurant = deletedRestaurant)

@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
    return render_template('menu.html', restaurant = restaurant, items = items)

#Making an API Endpoint (GET Request)
@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def showMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
    return jsonify(MenuItems=[i.serialize for i in items])
    


@app.route('/restaurant/<int:restaurant_id>/menu/new/', methods = ['GET','POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(name = request.form['name'], restaurant_id = restaurant_id)
        session.add(newItem)
        session.commit()
        flash(newItem.name + " added")
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))

    else:
        return render_template('newmenuitem.html', restaurant_id = restaurant_id)
                                              
#Making an API Endpoint (GET Request)
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def showMenuItemJSON(restaurant_id, menu_id):
    menuItem = session.query(MenuItem).filter_by(id = menu_id).one()
    return jsonify(MenuItem=[menuItem.serialize])                                              

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/', methods = ['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
    editedItem = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
       if request.form['name']:
           editedItem.name = request.form['name']
       session.add(editedItem)
       session.commit()
       flash(editedItem.name + " edited")
       return redirect(url_for('showMenu', restaurant_id = restaurant_id))

    else:
        return render_template('editmenuitem.html', restaurant_id = restaurant_id, menu_id = menu_id, editedItem = editedItem)
        

    
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/', methods = ['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
    deletedItem = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        session.delete(deletedItem)
        session.commit()
        flash(deletedItem.name + " deleted")
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
                        
    else:                    
        return render_template('deletemenuitem.html', deletedItem=deletedItem)
    


#makes sure the script only runs if the script is executed directly from the python interpreter
if __name__ == '__main__':
    app.secret_key = "super_secret_key"
    app.debug = True
    app.run(port = 5000)
