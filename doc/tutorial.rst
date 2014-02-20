.. _tutorial:

Flask-Inform Tutorial
=====================

This tutorial gives an introduction to how to create an self-describing, 
ReSTful web service using the Flask-Inform package.

Example Tutorial
----------------

This intoductory sentence should state the intent and goal of the tutorial. Keep it brief.

This next block should state any assumptions that you the writer are making. Present them in list form. Example: 

This tutorial assumes:

* GeoServer is running on http://localhost:8080/geoserver
* PostGIS is installed on the system

Getting started
```````````````

State any introductory steps in this section. These might include:

* Downloading data
* Creating a database


Creating and wrapping your app
``````````````````````````````

Flask-Inform, like many Flask extensions, works by wrapping the Flask app.

.. literalinclude:: example1.py


Adding Content
``````````````

In a single sentence, state what will be acheived in this section.

.. literalinclude:: example2.py
   :lines: 3,9-15

#. Step one
#. Step two

