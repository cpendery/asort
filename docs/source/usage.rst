Usage
=====

.. _installation:

Installation
------------

To use asort, first install it using pip:

.. code-block:: console

   (.venv) $ pip install asort


Running asort
-------------

asort can be run directly from the command line

.. code-block:: console

   (.venv) $ asort __init__.py directory/1
   Fixing directory/1/__init__.py
   Fixing directory/1/2/__init__.py

or it can be used as a python library

>>> from asort import ASort
>>> ASort().process_path("directory/1")
['directory/1/__init__.py', 'directory/1/2/__init__.py']
