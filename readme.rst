:author: Lukas Turcani
:contact: lukasturcani93@gmail.com

Introduction.
=============

Molder is a data collection website for molecules. When hosted on a
server, it looks like this:

.. image:: pictures/molder.png

The point is for users to give their opinion on a bunch of molecules
in a database. Data collected in this way can be used for machine
learning or in some other way. The number of buttons and question the
user answer can be changed depending on the task.

Data collection should also work from phones and tablets. The desktop
version of the site may have to be requested for this to work however.

How it works.
=============

On loading the website the user is asked to give a username. This
allows the user to pick up from where they left off on a machine.
For each user the server creates a folder with the same name. In this
folder two files are held for each user. The first, ``history.json``,
stores the InChI keys of molecules previously seen by the user in an
array. The second, ``opinions.json``, stores the rating the user gave
to a molecule. The storage is done in a dictionary where the key is the
InChI of the molecule and value corresponds to the button pressed.

When the user presses a button  a request is sent to the server. The
request delivers the molecule and button pressed. A server-side
Python script, ``next_mol.cgi``, stores this data in ``opinions.json``
in the user's directory. The script then selects the next molecule in
``database.json`` to be shown to the user. Modifications to this
script need to be done if the order or algorithm through which
molecules are presented to users is to be changed. See the script
itself for more details.

Files.
======

:database.json: Holds the database of molecules which are to be
evaluated by users.
