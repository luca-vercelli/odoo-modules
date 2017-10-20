.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===================================
Report To Printer - Windows version
===================================

This module allows users to send reports to a printer attached to the server.


It adds an optional behaviour on reports to send it directly to a printer.

* `Send to Client` is the default behaviour providing you a downloadable PDF
* `Send to Printer` prints the report on selected printer

Report behaviour is defined by settings.


Settings can be configured:

* globaly
* per user
* per report
* per user and report

Installation
============

You must install:
* win32api Python module (i.e. PyPI pypiwin32 package)
* GSView at http://pages.cs.wisc.edu/~ghost/gsview/get50.htm
* Ghostscript at https://ghostscript.com

WARNING: currently, this works if and only if Odoo is launched as program, not as service (working on this yet).

Configuration
=============

After installing enable the "Printing / Print User" option under access
rights to give users the ability to view the print menu.

You must fix Ghostscript and GSView paths in "System parameters" menu (this should be improved in future).


Usage
=====

To show all available printers for your server, use the
`Settings/Configuration/Printing/Update Printers from CUPS` wizard.


Then go to the user profile and set the users printing action and default
printer.

Caveat
------

The notification when a report is sent to a printer will not be
displayed for the deprecated report types (RML, Webkit, ...).

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/144/9.0


Known issues / Roadmap
======================



Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/report-print-send/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smashing it by providing a detailed and welcomed feedback.

Credits
=======

Images
------

* Odoo Community Association: `Icon <https://github.com/OCA/maintainer-tools/blob/master/template/module/static/description/icon.svg>`_.

Contributors
------------

* Ferran Pegueroles <ferran@pegueroles.com>
* Albert Cervera i Areny <albert@nan-tic.com>
* Davide Corio <davide.corio@agilebg.com>
* Lorenzo Battistini <lorenzo.battistini@agilebg.com>
* Yannick Vaucher <yannick.vaucher@camptocamp.com>
* Lionel Sausin <ls@numerigraphe.com>
* Guewen Baconnier <guewen.baconnier@camptocamp.com>
* Dave Lasley <dave@laslabs.com>
* Sylvain Garancher <sylvain.garancher@syleam.fr>
* Luca Vercelli <luca.vercelli.to@gmail.com>

Maintainer
----------

This module is *not* currently maintained by the OCA, but it could be.
