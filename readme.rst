:author: Lukas Turcani
:contact: lukasturcani93@gmail.com

Introduction.
=============

Molder is a data collection website for molecules. When hosted on a
server, it looks like this:

.. image:: pictures/molder.png

Note that the website shows an interactive 3D rendering of the
molecule and not a 2D picture.

The point is for users to give their opinion on a bunch of molecules
in a database. Data collected in this way can be used for machine
learning or in some other way. The number of buttons and question the
users answer can be changed depending on the task.

Data collection should also work from phones and tablets. The desktop
version of the site may have to be requested by the user's phone for
this to work, however.

.. image:: pictures/desktop_request.png


How it works.
=============

On loading the website the user is asked to give a username. This
allows the user to pick up from where they left off on a different
machine. For each user, the server creates a folder with the same name.
In this folder two files are held for each user. The first,
``history.json``, stores the InChI keys of molecules previously seen by
the user in an array. The second, ``opinions.json``, stores the ratings
the user gave to molecules. The storage is done in a dictionary where
the key is the InChI of the molecule and value corresponds to the
button pressed.

When the user presses a button a request is sent to the server. The
request delivers the molecule and button pressed. A server-side
Python script, ``next_mol.cgi``, stores this data in ``opinions.json``
in the user's directory. The script then selects the next molecule in
``database.json`` to be shown to the user. This script needs to be
modified if the order or algorithm through which molecules are
presented to users is to be changed. See the ``next_mol.cgi`` for more
details.

Files.
======

:database.json: Holds the database of molecules which are to be
                evaluated by users. The molecules are stored as a
                dictionary where the key is the InChI of the molecule
                and the value is the structural info of the molecule.
                The structural info is the content of a V3000 ``.mol``
                file of the molecule. The content of other molecular
                structure files may work as well, but they're not
                tested.
:index.html: The website.
:index.css: Styles the website.
:index.js: Makes the website interactive. Handles communication with
           the server.
:init_state.cgi: A server-side Python script. This script is run when
                 the user first loads the website. It initializes the
                 session by loading the history of the user (so they
                 can use the ``back`` button) and sends them their
                 first molecule of the session.
:next_mol.cgi: A server-side Python script. This script is invoked
               every time the user presses a button, excluding
               ``back``. The script saves the molecule and button
               pressed on the server and sends the user their next
               molecule.
:get_mol.cgi: A server-side Python script. Each time the ``back``
              button is pressed the user sends a request to the
              server. The server runs this script,  which looks at
              sends back the structural info the molecule the user
              requested.
