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

from forms import ArtistForm, VenueForm, ShowForm
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

    @classmethod
    def from_dict(cls, form):
        return cls(
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

    @classmethod
    def from_dict(cls, form):
        return cls(
            name=form.get('name'),
            genres=form.get('genres'),
            city=form.get('city'),
            state=form.get('state'),
            phone=form.get('phone'),
            image_link=form.get('image_link'),
            facebook_link=form.get('facebook_link'),
            website=form.get('website'),
            seeking_venue=form.get('seeking_venue'),
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

    @classmethod
    def from_dict(cls, form):
        return cls(
            artist_id=form.get('artist_id'),
            venue_id=form.get('venue_id'),
            start_time=form.get('start_time'),
        )

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
    if not form.validate_on_submit():
        flash(f'An error occurred. Venue could not be listed.', 'error')
        return render_template('pages/home.html')

    try:
        new_venue = Venue.from_dict(form.data)
        db.session.add(new_venue)
        db.session.commit()
        flash(f'Venue {new_venue.name} was successfully listed!')
    except:
        db.session.rollback()
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
    search_term = request.form.get('search_term')
    try:
        artists = Artist.query.filter(
            Artist.name.ilike(f'%{search_term}%')).all()
        response = {
            "count": len(artists),
            "data": [a.serialize for a in artists]
        }
    except:
        abort(500)
    finally:
        db.session.close()
    return render_template(
        'pages/search_artists.html',
        results=response,
        search_term=request.form.get('search_term', '')
    )


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
    try:
        artist = Artist.query.get(artist_id)
        form = ArtistForm(
            name=artist.name,
            city=artist.city,
            state=artist.state,
            phone=artist.phone,
            image_link=artist.image_link,
            genres=artist.genres,
            facebook_link=artist.facebook_link,
        )
    except:
        abort(500)
    finally:
        db.session.close()
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    form = ArtistForm()
    if not form.validate_on_submit():
        flash(f'An error occurred. Artist could not be updated.', 'error')
        return redirect(url_for('show_artist', artist_id=artist_id))

    try:
        artist = Artist.query.get(artist_id)
        for key in form.data:
            if form.data.get(key) is not None:
                setattr(artist, key, form.data.get(key))
        db.session.commit()
        flash(f'Artist {artist.name} was successfully updated!')
    except:
        db.session.rollback()
        abort(500)
    finally:
        db.session.close()

    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    try:
        venue = Venue.query.get(venue_id)
        form = VenueForm(
            name=venue.name,
            city=venue.city,
            state=venue.state,
            address=venue.address,
            phone=venue.phone,
            image_link=venue.image_link,
            genres=venue.genres,
            facebook_link=venue.facebook_link,
        )
    except:
        abort(500)
    finally:
        db.session.close()
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    form = VenueForm()
    if not form.validate_on_submit():
        flash(f'An error occurred. Venue could not be updated.', 'error')
        return redirect(url_for('show_venue', venue_id=venue_id))

    try:
        venue = Venue.query.get(venue_id)
        for key in form.data:
            if form.data.get(key) is not None:
                setattr(venue, key, form.data.get(key))
        db.session.commit()
        flash(f'Venue {venue.name} was successfully updated!')
    except:
        db.session.rollback()
        abort(500)
    finally:
        db.session.close()

    return redirect(url_for('show_venue', venue_id=venue_id))


#  Create Artist
#  ----------------------------------------------------------------
@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    form = ArtistForm()
    if not form.validate_on_submit():
        flash(f'An error occurred. Artist could not be listed.', 'error')
        return render_template('pages/home.html')

    try:
        new_artist = Artist.from_dict(form.data)
        db.session.add(new_artist)
        db.session.commit()
        flash(f'Artist {new_artist.name} was successfully listed!')
    except Exception as e:
        print(e)
        abort(500)
    finally:
        db.session.close()

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
    form = ShowForm()
    if not form.validate_on_submit():
        flash(f'An error occurred. Show could not be listed.', 'error')
        return render_template('pages/home.html')

    try:
        new_show = Show.from_dict(form.data)
        print(new_show.id)
        db.session.add(new_show)
        db.session.commit()
        flash('Show was successfully listed!')
    except Exception as e:
        print(e)
        flash('An error occurred. Show could not be listed.')
    finally:
        db.session.close()

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
