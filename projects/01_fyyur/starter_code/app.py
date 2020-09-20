#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
from __future__ import annotations
import babel
import dateutil.parser
import json
import pytz
import logging
from datetime import datetime
from flask import (
    Flask, render_template, request, Response,
    flash, redirect, url_for, abort, jsonify
)
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from logging import Formatter, FileHandler
from sqlalchemy.types import ARRAY

from forms import *
from helpers import aggregate_venues


#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
app = Flask(__name__)
moment = Moment(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, default='')
    genres = db.Column(ARRAY(db.String, dimensions=1), default=[])
    city = db.Column(db.String(120), default='')
    state = db.Column(db.String(120), default='')
    address = db.Column(db.String(120), default='')
    phone = db.Column(db.String(120), default='')
    image_link = db.Column(db.String(500), default='')
    facebook_link = db.Column(db.String(120), default='')
    website = db.Column(db.String(120), default='')
    seeking_talent = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(300), default='')

    shows = db.relationship('Show', lazy=True)

    def __getitem__(self, key):
        return getattr(self, key)

    @staticmethod
    def from_dict(form):
        return Venue(
            name=form.get('name'),
            genres=form.get('genres'),
            city=form.get('city'),
            state=form.get('state'),
            address=form.get('address'),
            phone=form.get('phone'),
            image_link=form.get('image_link'),
            facebook_link=form.get('facebook_link'),
            website=form.get('website'),
            seeking_talent=form.get('seeking_talent'),
            seeking_description=form.get('seeking_description')
        )

    @property
    def past_shows(self):
        return [show for show in self.shows if show.start_time < datetime.now()]

    @property
    def past_shows_count(self):
        return len(self.past_shows)

    @property
    def upcoming_shows(self):
        return [show for show in self.shows if show.start_time >= datetime.now()]

    @property
    def upcoming_shows_count(self):
        return len(self.upcoming_shows)

    @property
    def num_upcoming_shows(self):
        return self.upcoming_shows_count

    @property
    def serialize(self):
        """ Return object data in easily serializeable format"""

        return {
            "id": self.id,
            "name": self.name,
            "genres": self.genres,
            "city": self.city,
            "state": self.state,
            "phone": self.phone,
            "website": self.website,
            "facebook_link": self.facebook_link,
            "seeking_talent": self.seeking_talent,
            "seeking_description": self.seeking_description,
            "image_link": self.image_link,
            "past_shows": [show.serialize for show in self.past_shows],
            "upcoming_shows":  [show.serialize for show in self.upcoming_shows],
            "past_shows_count": self.past_shows_count,
            "upcoming_shows_count": self.upcoming_shows_count,
        }


class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, default='')
    city = db.Column(db.String(120), default='')
    state = db.Column(db.String(120), default='')
    phone = db.Column(db.String(120), default='')
    genres = db.Column(ARRAY(db.String, dimensions=1), default=[])
    image_link = db.Column(db.String(500), default='')
    website = db.Column(db.String(120), default='')
    facebook_link = db.Column(db.String(120), default='')
    seeking_venue = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(300), default='')

    shows = db.relationship('Show', lazy=True)

    @property
    def past_shows(self):
        return [show for show in self.shows if show.start_time < datetime.now()]

    @property
    def past_shows_count(self):
        return len(self.past_shows)

    @property
    def upcoming_shows(self):
        return [show for show in self.shows if show.start_time >= datetime.now()]

    @property
    def upcoming_shows_count(self):
        return len(self.upcoming_shows)

    @property
    def num_upcoming_shows(self):
        return self.upcoming_shows_count

    @property
    def serialize(self):
        """ Return object data in easily serializeable format"""

        return {
            "id": self.id,
            "name": self.name,
            "genres": self.genres,
            "city": self.city,
            "state": self.state,
            "phone": self.phone,
            "website": self.website,
            "facebook_link": self.facebook_link,
            "seeking_venue": self.seeking_venue,
            "seeking_description": self.seeking_description,
            "image_link": self.image_link,
            "past_shows": [show.serialize for show in self.past_shows],
            "upcoming_shows":  [show.serialize for show in self.upcoming_shows],
            "past_shows_count": self.past_shows_count,
            "upcoming_shows_count": self.upcoming_shows_count,
        }


class Show(db.Model):
    __tablename__ = 'shows'

    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey(
        'venues.id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey(
        'artists.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)

    venue = db.relationship('Venue', lazy=True)
    artist = db.relationship('Artist', lazy=True)

    @property
    def serialize(self):
        """ Return object data in easily serializeable format"""

        return {
            "venue_id": self.venue_id,
            "venue_name": self.venue.name,
            "venue_image_link": self.venue.image_link,
            "artist_id": self.artist_id,
            "artist_name": self.artist.name,
            "artist_image_link": self.artist.image_link,
            "start_time": self.start_time.replace(tzinfo=pytz.utc).isoformat()
        }


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#
def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
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
    try:
        venues = Venue.query.all()
        data = aggregate_venues(venues)
    except:
        abort(500)
    finally:
        db.session.close()
    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    search_term = request.form.get('search_term')
    try:
        venues = Venue.query.filter(Venue.name.ilike(f'%{search_term}%')).all()
        response = {
            "count": len(venues),
            "data": [v.serialize for v in venues]
        }
    except:
        abort(500)
    finally:
        db.session.close()
    return render_template(
        'pages/search_venues.html',
        results=response,
        search_term=request.form.get('search_term', '')
    )


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    try:
        venue = Venue.query.get(venue_id)
        data = venue.serialize
    except:
        abort(500)
    finally:
        db.session.close()
    return render_template('pages/show_venue.html', venue=data)


#  Create Venue
#  ----------------------------------------------------------------
@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    form = VenueForm()
    new_venue = Venue.from_dict(form.data)

    try:
        db.session.add(new_venue)
        db.session.commit()
        flash(f'Venue {new_venue.name} was successfully listed!')
    except:
        flash(
            f'An error occurred. Venue {new_venue.name} could not be listed.', 'error'
        )
        abort(500)
    finally:
        db.session.close()
    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    try:
        Venue.query.filter_by(id=venue_id).delete()
        db.session.commit()
        res = {'status': 'success'}
    except:
        db.session.rollback()
        res = {'status': 'failed'}
    finally:
        db.session.close()
    return jsonify(res)


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    try:
        artists = Artist.query.all()
        data = [artist.serialize for artist in artists]
    except:
        abort(500)
    finally:
        db.session.close()
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    response = {
        "count": 1,
        "data": [{
            "id": 4,
            "name": "Guns N Petals",
            "num_upcoming_shows": 0,
        }]
    }
    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    try:
        artist = Artist.query.get(artist_id)
        data = artist.serialize
    except:
        abort(500)
    finally:
        db.session.close()
    return render_template('pages/show_artist.html', artist=data)


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = {
        "id": 4,
        "name": "Guns N Petals",
        "genres": ["Rock n Roll"],
        "city": "San Francisco",
        "state": "CA",
        "phone": "326-123-5000",
        "website": "https://www.gunsnpetalsband.com",
        "facebook_link": "https://www.facebook.com/GunsNPetals",
        "seeking_venue": True,
        "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
        "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
    }
    # TODO: populate form with fields from artist with ID <artist_id>
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes

    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = {
        "id": 1,
        "name": "The Musical Hop",
        "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
        "address": "1015 Folsom Street",
        "city": "San Francisco",
        "state": "CA",
        "phone": "123-123-1234",
        "website": "https://www.themusicalhop.com",
        "facebook_link": "https://www.facebook.com/TheMusicalHop",
        "seeking_talent": True,
        "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
        "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
    }
    # TODO: populate form with values from venue with ID <venue_id>
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    return redirect(url_for('show_venue', venue_id=venue_id))


#  Create Artist
#  ----------------------------------------------------------------
@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion

    # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------
@app.route('/shows')
def shows():
    try:
        shows = Show.query.all()
        serialized = [show.serialize for show in shows]
    except:
        abort(500)
    finally:
        db.session.close()
    return render_template('pages/shows.html', shows=serialized)


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
    flash('Show was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
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
