Testing
=======

This section outlines how to test ``switchmap-ng``.

Testing Setup for Developers
----------------------------

Follow the installation steps above to have the application ready, then add these steps for developing code.


Database Configuration
~~~~~~~~~~~~~~~~~~~~~~

Create the ``switchmap_unittest`` database, and grant privileges to a ``switchmap_unittest`` user with the password ``switchmap_unittest``.

::
   
     $ sudo mysql
     >>> CREATE DATABASE switchmap_unittest;
     >>> GRANT ALL PRIVILEGES ON switchmap_unittest.* TO 'switchmap_unittest'@'localhost' IDENTIFIED BY 'switchmap_unittest';
     >>> FLUSH PRIVILEGES;
     >>> EXIT;

Setup the Test Config File
~~~~~~~~~~~~~~~~~~~~~~~~~~

Create the testing configuration file which will be stored in a hidden directory in ``$HOME``

::
   
   (venv) $ tests/bin/test_db_config_setup.py

Run the Test Suite
~~~~~~~~~~~~~~~~~~

**NOTE:** The test cases are written to be run only from the root directory of the repository this to ensure no errors in importing both the required test and code modules.

You can run all the tests with this command.

::
   
   (venv) $ cd /path/to/switchmap
   (venv) $ tests/bin/_do_all_tests.py

An alternative method is to use pytest.

::
   
   (venv) $ cd /path/to/switchmap
   (venv) $ pytest tests/switchmap_


You can run individual tests with this command.

::
   
   (venv) $ cd /path/to/switchmap
   (venv) $ tests/switchmap_/path/to/test.py


Populating the Database Using the Ingester
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pollers post network data to the Switchmap-NG server. The Ingester process reads this posted data and uses it to update the database. 

You may not have access to network devices for testing, however there is test data data that can be imported using the ingester.

An easy way to populate the database using this data is to:

1) Configure switchmap
2) Copy the test files in ``tests/testdata_`` to the configure ``cache_directory``
3) Start or restart the poller daemon or app
4) The updated data should now be visible in the web UI
