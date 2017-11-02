
==============
Mustache views
==============

Basic support for Mustache template engine, as opposed to QWeb.

The main Mustache feature is it is logic-less. That means, for example, there's no way to include an "if" condition itside a report. All logics must be put outside.
As a consequence, in most cases you will need a custom Report class to provide business logic to the report.

This module depends on account, because "Invoice report" is our first use case. That report may be put somewhere else in future.

