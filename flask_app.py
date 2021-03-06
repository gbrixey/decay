from flask import Flask, flash, g, redirect, render_template, request
from degrade import degrade_text, fake_degrade_jpeg
from constants import MAX_FILES
from util import *
from PIL import Image
import uuid
import os
import sqlite3

app = Flask(__name__)
DATABASE = os.path.join(app.root_path, 'data.db')
UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'images')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def ensure_upload_directory():
    """Creates the image upload directory if necessary."""
    os.makedirs(UPLOAD_FOLDER, exist_ok = True)

def ensure_items_table():
    """Creates the database table if necessary."""
    db = sqlite3.connect(DATABASE)
    sql_create_table = '''
        create table if not exists items (
            id integer primary key,
            filename text,
            description text
        );
    '''
    db.cursor().execute(sql_create_table)
    db.close()

def degrade_database():
    """Degrades all images and text currently in the database."""
    sql_fetch = '''select * from items order by id desc'''
    items = g.db.cursor().execute(sql_fetch).fetchall()
    for index, item in enumerate(items):
        id = item['id']
        description = item['description']
        old_image_path = os.path.join(UPLOAD_FOLDER, item['filename'])
        new_filename = random_jpeg_filename()
        new_image_path = os.path.join(UPLOAD_FOLDER, new_filename)
        strong = index >= 10
        fake_degrade_jpeg(old_image_path, new_image_path, strong = strong)
        os.remove(old_image_path)
        new_description = degrade_text(description)
        sql_update = '''
            update items
            set filename = ?,
                description = ?
            where id = ?
        '''
        g.db.cursor().execute(sql_update, (new_filename, new_description, id))
    g.db.commit()
    return

def trim_database_if_necessary():
    """Ensures that the database does not contain more than the maximum number of images."""
    sql_fetch = '''select id from items order by id desc'''
    items = g.db.cursor().execute(sql_fetch).fetchall()
    for (index, item) in enumerate(items):
        if index >= MAX_FILES:
            id = item['id']
            sql_delete = '''delete from items where id = ?'''
            g.db.cursor().execute(sql_delete, (id,))
    g.db.commit()
    return
    
def random_jpeg_filename():
    """Returns a random filename ending in .jpg"""
    name = str(uuid.uuid4())[:8]
    return name + '.jpg'
    
def makedict(cursor, row):
    return dict((cursor.description[i][0], value) for i, value in enumerate(row))
    
@app.before_request
def before_request():
    g.db = sqlite3.connect(DATABASE)
    g.db.row_factory = makedict

@app.after_request
def after_request(response):
    g.db.close()
    return response
    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/content')
def get_content():
    sql_fetch = '''select * from items order by id desc'''
    items = g.db.cursor().execute(sql_fetch).fetchall()
    return render_template('content.html', items = items)

@app.route('/submit_image', methods=['POST'])
def submit_image():
    image_file = request.files.get('image')
    image = jpeg_image_from_file(image_file)
    if image == None:
        return redirect('/')
    # Rotate/resize image if necessary
    image = rotate_image_if_necessary(image)
    image = crop_image_if_necessary(image)
    image = resize_image_if_necessary(image)
    filename = random_jpeg_filename()
    path = os.path.join(UPLOAD_FOLDER, filename)
    image.save(path, quality = 50, optimize = True)
    # Degrade existing images and text before inserting the new image,
    # so that the new image will start off with no glitches.
    degrade_database()
    description = request.form['description']
    if len(description) > 1000:
        description = description[:1000]
    sql_insert = '''insert into items (filename, description) values (?, ?)'''
    g.db.cursor().execute(sql_insert, (filename, description))
    g.db.commit()
    # Remove the oldest image if necessary.
    trim_database_if_necessary()
    return redirect('/')
    
ensure_upload_directory()
ensure_items_table()

if __name__ == '__main__':
    app.run(debug = True)
