custom-form-app
###############

|pypi-badge| |ci-badge| |codecov-badge| |doc-badge| |pyversions-badge|
|license-badge| |status-badge|

Purpose
*******

``custom-form-app`` stores and serves custom registration fields for Open edX
accounts. It adds its API through the LMS plugin URL mechanism and does not
modify the core Open edX account API.

Custom Account Fields API
**************************

The API is mounted under ``/api/custom-reg-form/v1/``. Requests must be made
by an authenticated user. JSON requests should use the
``Content-Type: application/json`` header.

Endpoints
=========

.. list-table::
     :header-rows: 1
     :widths: 35 65

     * - Method and path
         - Access
     * - ``GET /api/custom-reg-form/v1/me/``
         - Read the authenticated user's fields.
     * - ``PATCH /api/custom-reg-form/v1/me/``
         - Partially update the authenticated user's fields.
     * - ``GET /api/custom-reg-form/v1/accounts/{username}/``
         - Read the user's fields. A user may read their own fields; staff may
             read another user's fields.
     * - ``PATCH /api/custom-reg-form/v1/accounts/{username}/``
         - Partially update the user's fields. Updates are allowed only when the
             authenticated user is the target user; cross-user updates are denied,
             including for staff.

Supported fields
================

The API supports these six fields. Values for choice fields must use the
listed API value, not the display label.

.. list-table::
     :header-rows: 1
     :widths: 35 65

     * - Field
         - Accepted values
     * - ``ethnicity``
         - ``w``, ``ba``, ``na``, ``as``, ``nhpi``, ``hl``, ``me``, ``bm``,
             ``o``, or ``prefer-not-to-say``
     * - ``employment_status``
         - ``efw``, ``selfemployed``, ``student``, ``homemaker``, ``oowlfw``,
             ``oownclfw``, ``military``, ``retired``, ``utw``, or
             ``prefer-not-to-say``
     * - ``enrolled_in_school``
         - ``no``, ``yes``, or ``prefer-not-to-say``
     * - ``enrolled_in_school_type``
         - ``hs``, ``two-year``, ``four-year``, ``grad``, ``ne``, ``instructor``,
             or ``prefer-not-to-say``
     * - ``local_community_living``
         - ``ls``, ``su``, ``sct``, ``ra``, or ``prefer-not-to-say``
     * - ``zipcode``
         - A five-digit ZIP Code or ZIP+4 value, for example ``12345`` or
             ``12345-6789``

GET example
===========

.. code-block:: console

     $ curl -b cookies.txt \
             https://lms.example.com/api/custom-reg-form/v1/me/

The response contains all six fields. A field without a saved value is
``null``. The ``metadata.visibility`` object contains visibility for the same
six fields:

.. code-block:: json

     {
         "ethnicity": "ba",
         "employment_status": null,
         "enrolled_in_school": "yes",
         "enrolled_in_school_type": "four-year",
         "local_community_living": null,
         "zipcode": "12345",
         "metadata": {
             "visibility": {
                 "ethnicity": "optional",
                 "employment_status": "required",
                 "enrolled_in_school": "optional",
                 "enrolled_in_school_type": "hidden",
                 "local_community_living": "optional",
                 "zipcode": "optional"
             }
         }
     }

PATCH example
=============

``PATCH`` accepts any subset of the six fields and returns the complete
response payload shown above. For example:

.. code-block:: console

     $ curl -X PATCH -b cookies.txt \
             -H 'Content-Type: application/json' \
             -d '{"employment_status":"student","zipcode":"12345-6789"}' \
             https://lms.example.com/api/custom-reg-form/v1/me/

The related custom-field record is created automatically when the user does
not have one. An empty JSON object leaves the values unchanged and returns the
current response.

Responses and errors
====================

Successful ``GET`` and ``PATCH`` requests return HTTP 200 and a JSON object
with the six field values and ``metadata.visibility``. Unauthenticated
requests return HTTP 401:

.. code-block:: json

     {"detail": "Authentication credentials were not provided."}

Validation errors return HTTP 400 as a field-keyed JSON object. For example,
an invalid ZIP Code returns:

.. code-block:: json

     {"zipcode": ["Must be a valid zipcode"]}

Invalid JSON or a non-object JSON body returns HTTP 400:

.. code-block:: json

     {"detail": "JSON body must be an object."}

Cross-user access that is not permitted returns HTTP 403:

.. code-block:: json

     {"detail": "You do not have permission to access this account."}

An unknown username returns HTTP 404:

.. code-block:: json

     {"detail": "Account not found."}

Authorization and visibility
============================

The ``/me/`` routes always resolve to the authenticated user. The username
routes allow self-access, allow staff to read another user's fields, and deny
all cross-user updates. Authentication is required for every endpoint.

Visibility is read from Django's ``REGISTRATION_EXTRA_FIELDS`` setting for
these six custom fields. Each field is reported as ``required``, ``optional``,
or ``hidden``. If a field is missing from the setting, the API reports
``optional``. Other registration fields are not included or changed by this
API.

TODO: The ``README.rst`` file should start with a brief description of the repository and its purpose.
It should be described in the context of other repositories under the ``openedx``
organization. It should make clear where this fits into the overall Open edX
codebase and should be oriented towards people who are new to the Open edX
project.

Getting Started with Development
********************************

Please see the Open edX documentation for `guidance on Python development`_ in this repo.

.. _guidance on Python development: https://docs.openedx.org/en/latest/developers/how-tos/get-ready-for-python-dev.html

Deploying
*********

For details on how to deploy this component, see the `deployment how-to`_.

.. _deployment how-to: https://docs.openedx.org/projects/custom-form-app/how-tos/how-to-deploy-this-component.html

Getting Help
************

Documentation
=============

Start with `the documentation`_. If you need more help, see below.

.. _the documentation: https://docs.openedx.org/projects/custom-form-app

More Help
=========

If you're having trouble, we have discussion forums at
https://discuss.openedx.org where you can connect with others in the
community.

Our real-time conversations are on Slack. You can request a `Slack
invitation`_, then join our `community Slack workspace`_.

For anything non-trivial, the best path is to open an issue in this
repository with as many details about the issue you are facing as you
can provide.

https://github.com/CUCWD/custom-form-app/issues

For more information about these options, see the `Getting Help <https://openedx.org/getting-help>`__ page.

.. _Slack invitation: https://openedx.org/slack
.. _community Slack workspace: https://openedx.slack.com/

License
*******

The code in this repository is licensed under the AGPL 3.0 unless
otherwise noted.

Please see `LICENSE.txt <LICENSE.txt>`_ for details.

Contributing
************

Contributions are very welcome.
Please read `How To Contribute <https://openedx.org/r/how-to-contribute>`_ for details.

This project is currently accepting all types of contributions, bug fixes,
security fixes, maintenance work, or new features.  However, please make sure
to discuss your new feature idea with the maintainers before beginning development
to maximize the chances of your change being accepted.
You can start a conversation by creating a new issue on this repo summarizing
your idea.

The Open edX Code of Conduct
****************************

All community members are expected to follow the `Open edX Code of Conduct`_.

.. _Open edX Code of Conduct: https://openedx.org/code-of-conduct/

People
******

The assigned maintainers for this component and other project details may be
found in `Backstage`_. Backstage pulls this data from the ``catalog-info.yaml``
file in this repo.

.. _Backstage: https://backstage.openedx.org/catalog/default/component/custom-form-app

Reporting Security Issues
*************************

Please do not report security issues in public. Please email security@openedx.org.

.. |pypi-badge| image:: https://img.shields.io/pypi/v/custom-form-app.svg
    :target: https://pypi.python.org/pypi/custom-form-app/
    :alt: PyPI

.. |ci-badge| image:: https://github.com/CUCWD/custom-form-app/actions/workflows/ci.yml/badge.svg?branch=main
    :target: https://github.com/CUCWD/custom-form-app/actions/workflows/ci.yml
    :alt: CI

.. |codecov-badge| image:: https://codecov.io/github/CUCWD/custom-form-app/coverage.svg?branch=main
    :target: https://codecov.io/github/CUCWD/custom-form-app?branch=main
    :alt: Codecov

.. |doc-badge| image:: https://readthedocs.org/projects/custom-form-app/badge/?version=latest
    :target: https://docs.openedx.org/projects/custom-form-app
    :alt: Documentation

.. |pyversions-badge| image:: https://img.shields.io/pypi/pyversions/custom-form-app.svg
    :target: https://pypi.python.org/pypi/custom-form-app/
    :alt: Supported Python versions

.. |license-badge| image:: https://img.shields.io/github/license/CUCWD/custom-form-app.svg
    :target: https://github.com/CUCWD/custom-form-app/blob/main/LICENSE.txt
    :alt: License

.. TODO: Choose one of the statuses below and remove the other status-badge lines.
.. |status-badge| image:: https://img.shields.io/badge/Status-Experimental-yellow
.. .. |status-badge| image:: https://img.shields.io/badge/Status-Maintained-brightgreen
.. .. |status-badge| image:: https://img.shields.io/badge/Status-Deprecated-orange
.. .. |status-badge| image:: https://img.shields.io/badge/Status-Unsupported-red
