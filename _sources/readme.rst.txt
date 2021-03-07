astro-ph
========

|PyPI| |Python| |Test| |License|

Translate and post arXiv articles to various apps

Installation
------------

Use pip or other package manager to install the Python package.

.. code:: shell

   $ pip install astro-ph

Usage
-----

After installation, command line interface, ``astro-ph``, is available, with which you can translate and post arXiv articles to various apps. Note that only ``slack`` app is currently available. In this case, you need to `create a custom Slack app to get an URL of incoming webhook <https://slack.com/help/articles/115005265063-Incoming-webhooks-for-Slack>`__.

.. code:: shell

   $ astro-ph slack --keywords galaxy,galaxies \
                    --categories astro-ph.GA,astro-ph.IM \
                    --lang_to ja \
                    --webhook_url https://hooks.slack.com/services/***/***

The posted article looks like this.

.. figure:: https://raw.githubusercontent.com/astropenguin/astro-ph/master/docs/_static/astro-ph-slack.png
   :alt: astro-ph-slack.png

   astro-ph-slack.png

For detailed information, see the built-in help by the following command.

.. code:: shell

   $ astro-ph slack --help

Example
-------

It would be nice to regularly run the command by GitHub Actions. Here is a live example in which daily (2 days ago) arXiv articles in `astro-ph.GA <https://arxiv.org/list/astro-ph.GA/new>`__ and `astro-ph.IM <https://arxiv.org/list/astro-ph.IM/new>`__ are posted to different channels of a Slack workspace.

-  `a-lab-nagoya/astro-ph-slack: Translate and post arXiv articles to Slack <https://github.com/a-lab-nagoya/astro-ph-slack>`__

References
----------

-  `fkubota/Carrier-Owl: arxiv–> DeepL –> Slack <https://github.com/fkubota/Carrier-Owl>`__

   -  The astro-ph package is highly inspired by their work

-  `a-lab-nagoya/astro-ph-slack: Translate and post arXiv articles to Slack <https://github.com/a-lab-nagoya/astro-ph-slack>`__

   -  A live example using the astro-ph package

-  `pyppeteer/pyppeteer: Headless chrome/chromium automation library (unofficial port of puppeteer) <https://github.com/pyppeteer/pyppeteer>`__

   -  Used for async Chromium operation

-  `aio-libs/aiohttp: Asynchronous HTTP client/server framework for asyncio and Python <https://github.com/aio-libs/aiohttp>`__

   -  Used for async article posts to Slack

-  `google/python-fire: Python Fire is a library for automatically generating command line interfaces (CLIs) from absolutely any Python object. <https://github.com/google/python-fire>`__

   -  Used for creating command line interface

.. |PyPI| image:: https://img.shields.io/pypi/v/astro-ph.svg?label=PyPI&style=flat-square
   :target: https://pypi.org/project/astro-ph/
.. |Python| image:: https://img.shields.io/pypi/pyversions/astro-ph.svg?label=Python&color=yellow&style=flat-square
   :target: https://pypi.org/project/astro-ph/
.. |Test| image:: https://img.shields.io/github/workflow/status/astropenguin/astro-ph/Test?logo=github&label=Test&style=flat-square
   :target: https://github.com/astropenguin/astro-ph/actions
.. |License| image:: https://img.shields.io/badge/license-MIT-blue.svg?label=License&style=flat-square
   :target: LICENSE
