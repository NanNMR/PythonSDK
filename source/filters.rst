Dataset Filtering Guide
=======================

This guide explains how to use filters when searching for datasets in the USNAN SDK. The filtering system is based on PrimeNG table filters and provides powerful search capabilities.

Overview
--------

Dataset filtering is performed using the ``SearchConfig`` class, which allows you to build complex search queries by combining multiple filters with different match modes and operators.

Basic Usage
-----------

To search for datasets, create a ``SearchConfig`` object and add filters:

.. code-block:: python

    import usnan

    client = usnan.USNANClient()
    
    # Create a search configuration
    search_config = usnan.models.SearchConfig()
    
    # Add a filter
    search_config.add_filter('is_knowledgebase', value=True, match_mode='equals')
    
    # Execute the search
    results = client.datasets.search(search_config)
    
    # Iterate through results
    for dataset in results:
        print(f"Dataset: {dataset.dataset_name}")

SearchConfig Parameters
-----------------------

The ``SearchConfig`` class accepts the following parameters:

* ``records`` (int, default=25): Number of records to fetch per batch
* ``offset`` (int, default=0): Starting offset for results
* ``sort_order`` (str, default='ASC'): Sort order ('ASC' or 'DESC')
* ``sort_field`` (str, optional): Field to sort by

.. code-block:: python

    # Configure pagination and sorting
    search_config = usnan.models.SearchConfig(
        records=50,
        offset=0,
        sort_order='DESC',
        sort_field='dataset_name'
    )

Adding Filters
--------------

Use the ``add_filter()`` method to add search criteria:

.. code-block:: python

    search_config.add_filter(
        field='field_name',
        value='search_value',
        match_mode='equals',  # optional, default='equals'
        operator='AND'        # optional, default='AND'
    )

Match Modes
-----------

The following match modes are supported:

Text Matching
~~~~~~~~~~~~~

* ``equals`` - Exact match
* ``notEquals`` - Not equal to
* ``startsWith`` - Starts with the specified value
* ``endsWith`` - Ends with the specified value
* ``contains`` - Contains the specified value
* ``notContains`` - Does not contain the specified value
* ``similarTo`` - Similar to (fuzzy matching)

Null Checking
~~~~~~~~~~~~~

* ``isNull`` - Field is null/empty
* ``isNotNull`` - Field is not null/empty

Numeric Comparison
~~~~~~~~~~~~~~~~~~

* ``greaterThan`` - Greater than the specified value
* ``lessThan`` - Less than the specified value

Array Operations
~~~~~~~~~~~~~~~~

* ``includes`` - Array includes the specified value
* ``notIncludes`` - Array does not include the specified value

Examples by Match Mode
----------------------

Exact Match
~~~~~~~~~~~

.. code-block:: python

    # Find datasets that are knowledge base entries
    search_config = usnan.models.SearchConfig()
    search_config.add_filter('is_knowledgebase', value=True, match_mode='equals')

Text Search
~~~~~~~~~~~

.. code-block:: python

    # Find datasets with names containing "protein"
    search_config = usnan.models.SearchConfig()
    search_config.add_filter('dataset_name', value='protein', match_mode='contains')

Numeric Comparison
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Find 2D datasets
    search_config = usnan.models.SearchConfig()
    search_config.add_filter('num_dimension', value=2, match_mode='equals')

Null Checking
~~~~~~~~~~~~~

.. code-block:: python

    # Find datasets with descriptions
    search_config = usnan.models.SearchConfig()
    search_config.add_filter('description', match_mode='isNotNull')

Multiple Filters
----------------

You can combine multiple filters to create complex search queries:

.. code-block:: python

    # Find 2D knowledge base datasets
    search_config = (usnan.models.SearchConfig()
                    .add_filter('is_knowledgebase', value=True, match_mode='equals')
                    .add_filter('num_dimension', value=2, match_mode='equals'))

Operators
---------

When adding multiple filters for the same field, you can specify the operator:

* ``AND`` (default) - All conditions must be true
* ``OR`` - Any condition can be true

.. code-block:: python

    # Find datasets with specific names (OR logic)
    search_config = usnan.models.SearchConfig()
    search_config.add_filter('dataset_name', value='protein', match_mode='contains', operator='OR')
    search_config.add_filter('dataset_name', value='nucleic', match_mode='contains', operator='OR')

**Important**: All filters for the same field must use the same operator. Mixing operators for the same field will raise a ``ValueError``.

Pagination
----------

The search results are returned as a generator that automatically handles pagination:

.. code-block:: python

    search_config = usnan.models.SearchConfig(records=25)
    results = client.datasets.search(search_config)
    
    count = 0
    for dataset in results:
        count += 1
        print(f"Dataset {count}: {dataset.dataset_name}")
        
        # The generator will automatically fetch more results
        # when the current batch is exhausted
        if count >= 100:  # Stop after 100 results
            break

Cloning Search Configurations
-----------------------------

You can clone a search configuration to create variations:

.. code-block:: python

    # Base configuration
    base_config = usnan.models.SearchConfig()
    base_config.add_filter('is_knowledgebase', value=True, match_mode='equals')
    
    # Clone and modify
    modified_config = base_config.clone()
    modified_config.add_filter('num_dimension', value=2, match_mode='equals')

Error Handling
--------------

Common errors and how to handle them:

Invalid Filter Names
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    try:
        search_config = usnan.models.SearchConfig()
        search_config.add_filter('invalid_field_name', value=True, match_mode='equals')
        results = client.datasets.search(search_config)
        next(results)  # Error occurs when executing the search
    except RuntimeError as e:
        print(f"Invalid filter: {e}")

Mixed Operators
~~~~~~~~~~~~~~~

.. code-block:: python

    try:
        search_config = usnan.models.SearchConfig()
        search_config.add_filter('field', value='value1', operator='OR')
        search_config.add_filter('field', value='value2', operator='AND')  # Error!
    except ValueError as e:
        print(f"Operator mismatch: {e}")

Invalid Dataset IDs
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    try:
        client = usnan.USNANClient()
        dataset = client.datasets.get("invalid_id")  # Should be integer
    except TypeError as e:
        print(f"Invalid ID type: {e}")

    try:
        dataset = client.datasets.get(999999)  # Non-existent ID
    except KeyError as e:
        print(f"Dataset not found: {e}")

Complete Example
----------------

Here's a comprehensive example showing various filtering techniques:

.. code-block:: python

    import usnan

    def search_datasets():
        client = usnan.USNANClient()
        
        # Create a complex search
        search_config = (usnan.models.SearchConfig(records=50)
                        .add_filter('is_knowledgebase', value=True, match_mode='equals')
                        .add_filter('num_dimension', value=2, match_mode='equals'))
        
        print("Searching for 2D datasets in knowledge base...")
        
        results = client.datasets.search(search_config)
        count = 0
        
        for dataset in results:
            count += 1
            print(f"{count}. {dataset.dataset_name}")
            print(f"   Experiment: {dataset.experiment_name}")
            print(f"   Facility: {dataset.facility.name if dataset.facility else 'Unknown'}")
            print(f"   Dimensions: {dataset.num_dimension}")
            print()
            
            if count >= 10:  # Limit output
                break
        
        if count == 0:
            print("No datasets found matching the criteria.")
        else:
            print(f"Found {count} datasets (showing first 10)")

    if __name__ == "__main__":
        search_datasets()

Best Practices
--------------

1. **Use specific filters**: Start with the most selective filters to reduce the result set quickly.

2. **Handle pagination**: Don't assume all results will fit in memory. Process results as you iterate.

3. **Clone configurations**: When creating variations of searches, clone the base configuration rather than recreating it.

4. **Error handling**: Always wrap search operations in try-catch blocks to handle invalid filters or network issues.

5. **Performance**: When fetching many datasets, the SDK will automatically increase the number of records fetched at once to reduce network latency. Increasing the number of records returned is only helpful when it is known initially that a large number of results is expected and all results must be fetched.

6. **Field validation**: Refer to the dataset model documentation for valid field names and types.

Common Dataset Fields
---------------------

Here are some commonly used fields for filtering:

* ``dataset_name`` - Name of the dataset (may be edited by the user for readability)
* ``experiment_name`` - Name of the experiment (as captured on the spectrometer)
* ``is_knowledgebase`` - Boolean indicating if it's a knowledge base entry
* ``num_dimension`` - Number of dimensions (1D, 2D, etc.)
* ``description`` - Dataset description

For a complete list of available fields, refer to the Dataset model documentation or inspect a dataset object's attributes.
