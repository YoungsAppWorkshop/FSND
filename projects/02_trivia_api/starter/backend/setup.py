from setuptools import find_packages, setup

setup(
    name='flaskr',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=False,
    zip_safe=False,
    install_requires=[
        'flask',
        'aniso8601',
        'Click',
        'Flask',
        'Flask-Cors',
        'Flask-RESTful',
        'Flask-SQLAlchemy',
        'itsdangerous',
        'Jinja2',
        'MarkupSafe',
        'marshmallow',
        'psycopg2-binary',
        'pytest',
        'pytz',
        'six',
        'SQLAlchemy',
        'Werkzeug',
    ],
)
