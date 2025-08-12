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

Traverse the objects, starting with a facility:

.. code-block:: python

   mullen = client.facilities.get('UCHC-Mullen')
   print(mullen)
   spectrometers = mullen.spectrometers
   print(repr(spectrometers))
   # If you've never accessed the spectrometers before, accessing any of their properties will automatically fetch them.
   # In other words, the code above ONLY hits the facilities endpoint, and represents the linked spectrometers solely by their ID.
   # The moment you access one of these lazily-resolved spectrometers, the module will automatilly hit the spectrometers endpoint to fetch it.
   print(spectrometers[0])
   # What probe is currently installed in the spectrometer? (Again, the probes were not actually fetched until accessed.)
   print(spectrometers[0].installed_probe)
   # What probes are compatible with the spectrometer?
   print(spectrometers[0].compatible_probes)


Search for knowledgebase datasets with 3 dimensions:

.. code-block:: python

   search_config = (usnan.models.SearchConfig()
                        .add_filter('is_knowledgebase', value=True, match_mode='equals')
                        .add_filter('num_dimension', value=3, match_mode='equals'))
   results = client.datasets.search(search_config)
   print(next(results).dimensions))

Download the raw data for knowledgebase datasets with 3 dimensions (for the first 10 experiments):

.. code-block:: python

    search_config = (usnan.models.SearchConfig()
                        .add_filter('is_knowledgebase', value=True, match_mode='equals')
                        .add_filter('num_dimension', value=3, match_mode='equals')
                        )
    datasets = list(client.datasets.search(search_config))
    client.datasets.download([_.id for _ in datasets[:10]], location='./3d_knowledgebase')

Learn more about dataset filtering: :doc:`filters`

View the spectrometer and facility for a dataset:

.. code-block:: python

   dataset = client.datasets.get(363067)
   spectrometer = dataset.spectrometer
   facility = dataset.facility
   print(spectrometer)
   print(facility)


By default this module will cache facility, spectrometer, and probe information. (Datasets are not cached.) For example, if you
previously loaded the spectrometers for a given facility, and then later you search for a dataset and access its linked spectrometer,
you will get back the spectrometer object that was loaded previously. As facility, spectrometer, and probe information rarely changes,
this provides a significant performance boost versus loading each of these objects over and over. If you are using this code for an analysis
or to perform a quick calculation, this is probably desired behavior. If you use this code in a daemon, you will probably want to clear the cache
occasionally. Note that any existing objects in memory won't be refreshed, but any future objects fetched via the client will use the newly fetched objects.

It's easy to clear the cache:

.. code-block:: python

    client.clear_cache()


Next Steps
----------

* Use the built in python `help()`, your IDE, or the full documentation :doc:`dataclasses` to learn more about what attributes each object has.
* Check out the :doc:`api` for detailed API documentation. This is not particularly relevant if you are only using this module, but may be helpful to see the structure of the data objects.
* Explore the examples in the repository in the tests folder.

