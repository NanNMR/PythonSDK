Quick Start
===========

This guide will help you get started with the USNAN SDK quickly.

Installation
------------

Install the USNAN SDK using pip:

.. code-block:: bash

   pip install usnan

Basic Usage
-----------

Here's a few simple examples. Before running them, please run:

.. code-block:: python

   import usnan
   client = usnan.USNANClient()

View a facility:

.. code-block:: python

   facilities = client.facilities.list()
   print(facilities[0])


Search for a knowledgebase dataset with 3 dimensions:

.. code-block:: python

   search_config = (usnan.models.SearchConfig()
                        .add_filter('is_knowledgebase', value=True, match_mode='equals')
                        .add_filter('num_dimension', value=3, match_mode='equals'))
   results = client.datasets.search(search_config)
   print(next(results).dimensions))

Next Steps
----------

* Check out the :doc:`api` for detailed class and method documentation
* Explore the examples in the repository
* Read the advanced usage guides
