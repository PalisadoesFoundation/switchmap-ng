Webserver
=========

You can access ``switchmap-ng`` on its default port 7000, however you may want to access it on port 80 by integrating it with an Apache or Nginx webserver. This page explains how.


Apache setup for ``switchmap-ng``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``switchmap-ng`` has sample configurations for the Apache webserver.

Run the following commands from the top directory of ``switchmap-ng``

::

    $ sudo cp examples/linux/apache/switchmap-ng-apache.conf /etc/apache2/conf-available
    $ sudo ln -s /etc/apache2/conf-available/switchmap-ng-apache.conf /etc/apache2/conf-enabled/switchmap-ng-apache.conf

    # (Ubuntu only)
    $ sudo a2enmod proxy_http
    $ sudo systemctl restart apache2.service

    # (RedHat / CentOS)
    $ sudo systemctl restart httpd.service

You should now be able to access your ``switchmap-ng`` web pages using the following link.

::

   http://SERVER_NAME/switchmap/


Nginx setup for ``switchmap-ng``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``switchmap-ng`` has sample configurations for the Nginx webserver.

Run the following commands from the top directory of ``switchmap-ng``

::

    $ sudo cp examples/linux/nginx/switchmap-ng-nginx.conf /etc/nginx/sites-available
    $ sudo ln -s /etc/nginx/sites-available/switchmap-ng-nginx.conf /etc/nginx/conf-enabled/switchmap-ng-nginx.conf

**Note:** Edit the ``/etc/nginx/conf-enabled/switchmap-ng-nginx.conf`` file and change the IP address of the server then restart Nginx.

::

    $ systemctl restart nginx.service

You should now be able to access your ``switchmap-ng`` web pages using the following link.

::

   http://SERVER_NAME/switchmap-ng/
