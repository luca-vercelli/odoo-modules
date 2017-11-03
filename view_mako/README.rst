
==============
Mako views
==============

Basic support for Mako template engine, as opposed to QWeb.

This module defines a new view type "Mako" and handles its rendering.

Inside a Mako view, one can use the following ad-hoc functions intended for formatting:

* number(q)
* currency(amount)
* date(date)
* time(time)
* datetime(datetime)
* b64encode(data)
* render(template_external_id, **more_values)

So far, Mako templates are **not** translatable.

This module depends on **account**, because the "Invoice report" is our first use case. That report may be put somewhere else in future.

