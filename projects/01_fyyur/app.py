#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from datetime import datetime
from sqlalchemy import func, desc
from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False, unique=True)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False, unique=True)
    phone = db.Column(db.String(120), nullable=False, unique=True)
    genres = db.Column(db.ARRAY(db.String()), nullable=False)
    image_link = db.Column(db.String(500), nullable=True)
    website_link = db.Column(db.String(120), nullable=True, unique=True)
    facebook_link = db.Column(db.String(120), unique=True)
    seeking_talent = db.Column(db.Boolean, nullable=False)
    seeking_description = db.Column(db.Text, nullable=True)
    shows = db.relationship('Show', backref='venue', lazy=True)

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False, unique=True)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False, unique=True)
    genres = db.Column(db.ARRAY(db.String()), nullable=False)
    image_link = db.Column(db.String(500), nullable=True)
    website_link = db.Column(db.String(120), nullable=True)
    facebook_link = db.Column(db.String(120), unique=True)
    seeking_venue = db.Column(db.Boolean, nullable=False)
    seeking_description = db.Column(db.Text, nullable=True)
    shows = db.relationship('Show', backref='artist', lazy=True)

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Show(db.Model):
  __tablename__ = 'shows'

  id = db.Column(db.Integer, primary_key=True)
  venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'), nullable=False)
  artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable=False)
  start_time = db.Column(db.String(), nullable=False)

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data = []
  cities = Venue.query.with_entities(Venue.city, Venue.state).group_by(Venue.city, Venue.state).order_by(func.count(Venue.city).desc()).all()
  for city in cities:
    venues = []
    for venue in Venue.query.with_entities(Venue.id, Venue.name).filter_by(city=city.city).order_by(Venue.name).all():
      venues.append({
        'id': venue.id,
        'name': venue.name,
        'num_upcoming_shows': len(Show.query.filter(Show.start_time > datetime.now().strftime("%Y-%m-%d %H:%M:%S")).filter(Show.venue_id==venue.id).all())
      })
    data.append({
      'city': city.city,
      'state': city.state,
      'venues': venues
      
    })
  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term = request.form.get('search_term', '')
  key = '%{}%'.format(search_term)
  data = Venue.query.with_entities(Venue.id, Venue.name).filter(Venue.name.ilike(key)).all()
  response={
    "count": len(data),
    "data": data
  }
  return render_template('pages/search_venues.html', results=response, search_term=search_term)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  
  data = Venue.query.get(venue_id)
  if data:
    data = vars(data)
    data.update({
      'past_shows': Show.query.with_entities(Show.artist_id, Artist.name.label('artist_name'), Artist.image_link.label('artist_image_link'), Show.start_time).join(Artist).filter(Show.venue_id==venue_id).filter(Show.start_time < datetime.now().strftime("%Y-%m-%d %H:%M:%S")).all(),
      'upcoming_shows': Show.query.with_entities(Show.artist_id, Artist.name.label('artist_name'), Artist.image_link.label('artist_image_link'), Show.start_time).join(Artist).filter(Show.venue_id==venue_id).filter(Show.start_time > datetime.now().strftime("%Y-%m-%d %H:%M:%S")).all()
    })
    data.update({
      'past_shows_count': len(data['past_shows']),
      'upcoming_shows_count': len(data['upcoming_shows'])
    })
    return render_template('pages/show_venue.html', venue=data)
  else:
    return abort(404)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned form db insertion\
  error = False
  try:
    form = VenueForm(request.form)
    if form.validate():
      new_venue = Venue(
        name=form.name.data,
        city=form.city.data,
        state=form.state.data,
        address=form.address.data,
        phone=form.phone.data,
        genres=form.genres.data,
        image_link=form.image_link.data,
        website_link=form.website_link.data,
        facebook_link=form.facebook_link.data,
        seeking_talent=form.seeking_talent.data,
        seeking_description=form.seeking_description.data
      )
      db.session.add(new_venue)
      db.session.commit()
      # on successful db insert, flash success
      flash('Venue ' + form.name.data + ' was successfully listed!')
    else:
      print(form.errors)
      raise ValueError('ValidationError')
  except:
    db.session.rollback()
    error = True
    # TODO: on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Venue ' + form.name.data + ' could not be listed.') 
  finally:
    db.session.close()
  if error:
    return abort(500)
  else:
    return redirect(url_for('venues'))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  venue = Venue.query.get(venue_id)
  if venue:
    # TODO: populate form with values from venue with ID <venue_id>
    form = VenueForm(obj=venue)
    return render_template('forms/edit_venue.html', form=form, venue=venue)
  else:
    return abort(404)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  error = False
  venue = Venue.query.get(venue_id)
  try:
    form = VenueForm(request.form)
    if form.validate():
      venue.name = form.name.data
      venue.city = form.city.data
      venue.state = form.state.data
      venue.address = form.address.data
      venue.phone = form.phone.data
      venue.genres = form.genres.data
      venue.image_link = form.image_link.data
      venue.website_link = form.website_link.data
      venue.facebook_link = form.facebook_link.data
      venue.seeking_talent = form.seeking_talent.data
      venue.seeking_description = form.seeking_description.data

      db.session.commit()
    else:
      raise ValueError('ValidationError')
  except:
    db.session.rollback()
    error = True
    flash('An error occurred. Venue ' + venue.name + ' could not be edited.') 
  finally:
    db.session.close()
  if error:
    return abort(500)
  else:
    return redirect(url_for('show_venue', venue_id=venue_id))


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  error = False
  try:
    Venue.query.filter_by(id=venue_id).delete()
    db.session.commit()
    flash('An error occurred. Venue with ID: ' + venue_id + ' was deleted successfully.')
  except:
    db.session.rollback()
    error = True
    flash('An error occurred. Venue with ID: ' + venue_id + ' could not be deleted.')
  finally:
    db.session.close()
  if error:
    return abort(500)
  else:
    return redirect(url_for('index'), code=303)

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data = Artist.query.with_entities(Artist.id, Artist.name).order_by(Artist.name).all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term = request.form.get('search_term', '')
  key = '%{}%'.format(search_term)
  data = Artist.query.with_entities(Artist.id, Artist.name).filter(Artist.name.ilike(key)).all()
  response={
    "count": len(data),
    "data": data
  }
  return render_template('pages/search_artists.html', results=response, search_term=search_term)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  data = Artist.query.get(artist_id)
  if data:
    data = vars(data)
    data.update({
      'past_shows': Show.query.with_entities(Show.venue_id, Venue.name.label('venue_name'), Venue.image_link.label('venue_image_link'), Show.start_time).join(Venue).filter(Show.artist_id==artist_id).filter(Show.start_time < datetime.now().strftime("%Y-%m-%d %H:%M:%S")).all(),
      'upcoming_shows': Show.query.with_entities(Show.venue_id, Venue.name.label('venue_name'), Venue.image_link.label('venue_image_link'), Show.start_time).join(Venue).filter(Show.artist_id==artist_id).filter(Show.start_time > datetime.now().strftime("%Y-%m-%d %H:%M:%S")).all()
    })
    data.update({
      'past_shows_count': len(data['past_shows']),
      'upcoming_shows_count': len(data['upcoming_shows'])
    })
    return render_template('pages/show_artist.html', artist=data)
  else:
    return abort(404)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  artist = Artist.query.get(artist_id)
  if artist:
    # TODO: populate form with values from artist with ID <artist_id>
    form = ArtistForm(obj=artist)
    return render_template('forms/edit_artist.html', form=form, artist=artist)
  else:
    return abort(404)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  error = False
  artist = Artist.query.get(artist_id)
  try:
    form = ArtistForm(request.form)
    if form.validate():
      artist.name = form.name.data
      artist.city = form.city.data
      artist.state = form.state.data
      artist.phone = form.phone.data
      artist.genres = form.genres.data
      artist.image_link = form.image_link.data
      artist.website_link = form.website_link.data
      artist.facebook_link = form.facebook_link.data
      artist.seeking_venue = form.seeking_venue.data
      artist.seeking_description = form.seeking_description.data

      db.session.commit()
    else:
      raise ValueError('ValidationError')
  except:
    db.session.rollback()
    error = True
    flash('An error occurred. Artist ' + artist.name + ' could not be edited.') 
  finally:
    db.session.close()
  if error:
    return abort(500)
  else:
    return redirect(url_for('show_artist', artist_id=artist_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  error = False
  try:
    form = ArtistForm(request.form)
    if form.validate():
      new_artist = Artist(
        name=form.name.data,
        city=form.city.data,
        state=form.state.data,
        phone=form.phone.data,
        genres=form.genres.data,
        image_link=form.image_link.data,
        website_link=form.website_link.data,
        facebook_link=form.facebook_link.data,
        seeking_venue=form.seeking_venue.data,
        seeking_description=form.seeking_description.data
      )
      db.session.add(new_artist)
      db.session.commit()
      # on successful db insert, flash success
      flash('Artist ' + form.name.data + ' was successfully listed!')
    else:
      print(form.errors)
      raise ValueError('ValidationError')
  except:
    db.session.rollback()
    error = True
    # TODO: on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Artist ' + form.name.data + ' could not be listed.') 
  finally:
    db.session.close()
  if error:
    return abort(500)
  else:
    return redirect(url_for('artists'))


@app.route('/artist/<artist_id>', methods=['DELETE'])
def delete_artist(artist_id):
  # TODO: Complete this endpoint for taking a artist_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a artist on a artist Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  error = False
  try:
    Artist.query.filter_by(id=artist_id).delete()
    db.session.commit()
    flash('An error occurred. Artist with ID: ' + artist_id + ' was deleted successfully.')
  except:
    db.session.rollback()
    error = True
    flash('An error occurred. Artist with ID: ' + artist_id + ' could not be deleted.')
  finally:
    db.session.close()
  if error:
    return abort(500)
  else:
    return redirect(url_for('index'), code=303)


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data = Show.query.with_entities(Show.venue_id, Venue.name.label('venue_name'), Show.artist_id, Artist.name.label('artist_name'), Artist.image_link.label('artist_image_link'), Show.start_time).join(Venue).join(Artist).all()
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  # on successful db insert, flash success
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  error = False
  try:
    form = ShowForm(request.form)
    if form.validate():
      new_show = Show(
        artist_id=form.artist_id.data,
        venue_id=form.venue_id.data,
        start_time=form.start_time.data
      )
      db.session.add(new_show)
      db.session.commit()
      # on successful db insert, flash success
      flash('Show was successfully listed!')
    else:
      print(form.start_time.data)
      print(form.errors)
      raise ValueError('ValidationError')
  except:
    db.session.rollback()
    error = True
    # TODO: on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Show could not be listed.') 
  finally:
    db.session.close()
  if error:
    return abort(500)
  else:
    return redirect(url_for('shows'))

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
