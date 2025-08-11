API Reference
=============

This section provides detailed documentation for the USNAN SDK API endpoints and their JSON responses.

Overview
--------

The endpoints provide access to different data objects within NAN. In this initial release, that includes:

 * Datasets (also known as experiments) (:class:`usnan_sdk.models.datasets.Dataset`)
 * Facilities (:class:`usnan_sdk.models.facilities.Facility`)
 * Spectrometers (also known as spectrometers) (:class:`usnan_sdk.models.spectrometers.Spectrometer`)
 * Probes (:class:`usnan_sdk.models.probes.Probe`)

Furthermore, some of these data objects have other data objects embedded inside of them. For example, a facility object
has staff objects associated with it. These embedded objects are implemented as Python dataclasses in the SDK models
and their JSON structure is documented in the respective endpoint sections below.


Endpoints
---------

Dataset Fetch Endpoint
~~~~~~~~~~~~~~~~~~~~~~

* ``GET /nan/public/datasets/{dataset_id}`` - Retrieve a specific dataset by ID

**JSON Response Structure:**

.. code-block:: json

   {
     "id": 0,
     "classification": "string",
     "dataset_name": "string",
     "decoupling_sequence": "string",
     "experiment_end_time": "string",
     "experiment_name": "string",
     "experiment_start_time": "string",
     "facility_identifier": "string",
     "identifier": "string",
     "is_knowledgebase": true,
     "is_locked": true,
     "is_multi_receiver": true,
     "is_non_uniform": true,
     "mas_rate": 0.0,
     "mixing_sequence": "string",
     "mixing_time": 0.0,
     "notes": "string",
     "num_dimension": 0,
     "num_dimension_collected": 0,
     "number_in_set": 0,
     "pi_name": "string",
     "preferred": true,
     "public_time": "string",
     "published_time": "string",
     "pulse_sequence": "string",
     "sample_id": 0,
     "sample_sparsity": 0.0,
     "session_id": 0,
     "solvent": "string",
     "source": "string",
     "spectrometer_identifier": "string",
     "state": "string",
     "tags": ["string"],
     "temperature_k": 0.0,
     "time_shared": true,
     "title": "string",
     "version": "string",
     "z0_drift_correction": true,
     "dimensions": [
       {
         "dimension": 0,
         "nucleus": "string",
         "is_direct": true,
         "spectral_width_ppm": 0.0,
         "maximum_evolution_time": 0.0,
         "num_points": 0
       }
     ],
     "versions": [
       {
         "id": 0,
         "version": 0
       }
     ]
   }

**Response Fields:**

* ``id`` - [Add description]
* ``classification`` - [Add description]
* ``dataset_name`` - [Add description]
* ``decoupling_sequence`` - [Add description]
* ``experiment_end_time`` - [Add description]
* ``experiment_name`` - [Add description]
* ``experiment_start_time`` - [Add description]
* ``facility_identifier`` - [Add description]
* ``identifier`` - [Add description]
* ``is_knowledgebase`` - [Add description]
* ``is_locked`` - [Add description]
* ``is_multi_receiver`` - [Add description]
* ``is_non_uniform`` - [Add description]
* ``mas_rate`` - [Add description]
* ``mixing_sequence`` - [Add description]
* ``mixing_time`` - [Add description]
* ``notes`` - [Add description]
* ``num_dimension`` - [Add description]
* ``num_dimension_collected`` - [Add description]
* ``number_in_set`` - [Add description]
* ``pi_name`` - [Add description]
* ``preferred`` - [Add description]
* ``public_time`` - [Add description]
* ``published_time`` - [Add description]
* ``pulse_sequence`` - [Add description]
* ``sample_id`` - [Add description]
* ``sample_sparsity`` - [Add description]
* ``session_id`` - [Add description]
* ``solvent`` - [Add description]
* ``source`` - [Add description]
* ``spectrometer_identifier`` - [Add description]
* ``state`` - [Add description]
* ``tags`` - [Add description]
* ``temperature_k`` - [Add description]
* ``time_shared`` - [Add description]
* ``title`` - [Add description]
* ``version`` - [Add description]
* ``z0_drift_correction`` - [Add description]

**Dimension Object Fields:**

* ``dimension`` - [Add description]
* ``nucleus`` - [Add description]
* ``is_direct`` - [Add description]
* ``spectral_width_ppm`` - [Add description]
* ``maximum_evolution_time`` - [Add description]
* ``num_points`` - [Add description]

**Version Object Fields:**

* ``id`` - [Add description]
* ``version`` - [Add description]

Dataset Search Endpoint
~~~~~~~~~~~~~~~~~~~~~~~

* ``GET /nan/public/datasets/search`` - Search for datasets using various filters

Parameters:

* ``filters`` - A dictionary of search filter configurations, JSON encoded. Details below.
* ``records`` (integer) - The number of records to return at a time. Defaults to 100.
* ``offset`` (integer) - An integer offset into the results. Defaults to 0.
* ``sort_field`` (string) - The name of the field to sort by. Must match one of the fields in the Experiment response.
* ``sort_order`` ('ASC' or 'DESC') - Specifies whether to sort by the sort_field in ascending or descending order.

Some examples of the filters parameter, prior to being stringified:

* ``{id: [{value: 363067, matchMode: 'equals', operator: 'OR'}, {value: 363068, matchMode: 'equals', operator: 'OR'}]}`` - Filters where the dataset ID has the exact value 363067 OR 363068.
* ``{is_knowledgebase: [{value: true, matchMode: 'equals'}], num_dimension: [{value: 2, match_mode: 'greaterThan'}]}`` - Filters where the dataset is a knowledgebase and has at least 2 dimensions.

These filter types an options are documented fully in :doc:`filters`.

**JSON Response Structure:**

.. code-block:: json

   {
     "last_page": "boolean",
     "experiments": "Dataset[]"
   }


* ``last_page`` (boolean) - True when this response contains the last page of results for the query. When false, more records can be obtained by repeating the query with a higher `offset` value.
* ``experiments`` (Dataset[]) - An array of dataset objects. (See the structure of this object in the `Dataset Fetch Endpoint`_ documentation.)

Facilities Endpoint
~~~~~~~~~~~~~~~~~~~

**API Endpoints:**

* ``GET /nan/public/facilities`` - List all facilities
* ``GET /nan/public/facilities/{facility_id}`` - Retrieve a specific facility by ID

**JSON Response Structure:**

.. code-block:: json

   {
     "identifier": "string",
     "long_name": "string",
     "short_name": "string",
     "description": "string",
     "institution": "string",
     "url": "string",
     "color": "string",
     "logo": "string",
     "services": [
       {
         "service": "string",
         "description": "string"
       }
     ],
     "webpages": [
       {
         "urltype": "string",
         "url": "string"
       }
     ],
     "staff": [
       {
         "first_name": "string",
         "last_name": "string",
         "middle_initial": "string",
         "work_phone": "string",
         "mobile_phone": "string",
         "email": "string",
         "roles": ["string"],
         "responsibilities": ["string"],
         "expertise": ["string"]
       }
     ],
     "contacts": [
       {
         "name": "string",
         "work_phone": "string",
         "mobile_phone": "string",
         "email": "string",
         "details": "string",
         "responsibilities": ["string"]
       }
     ],
     "addresses": [
       {
         "address_type": ["string"],
         "address1": "string",
         "address2": "string",
         "address3": "string",
         "city": "string",
         "state": "string",
         "zipcode": "string",
         "zipcode_ext": "string",
         "country": "string"
       }
     ]
   }

**Response Fields:**

The core facility information.

* ``identifier`` (string) - The unique identifier for the facility. Choosen by administrators rather than being randomly assigned.
* ``long_name`` (string) - A long name for the facility, including the center name.
* ``short_name`` (string) - A shorter name for the facility.
* ``description`` (string) - A description of the facility.
* ``institution`` (string) - The name of the institution that the facility is located at.
* ``url`` (string) - The official URL for the facility.
* ``color`` (string) - A hex color code used to style the facilities pages.
* ``logo`` (string) - The facility logo in SVG format.
* ``services`` (Service[]) - See below
* ``webpages`` (Webpage[]) - See below
* ``staff`` (Staff[]) - See below
* ``contacts`` (Contact[]) - See below
* ``addresses`` (Address[]) - See below

**Service Fields:**

A service the facility provides.

* ``service`` (string) - A string describing the type of service provided. Valid values are one of the following: ``"Analysis", "Data Processing", "Experiment Setup", "Remote Access", "Rotor Packing", "Sample Preparation", "Self Service", "Shipping and Handling", "Consultation", "Training"``
* ``description`` (string) - Additional information about the service provided at this facility.

**Webpage Fields:**

A web page assosciated with the facility.

* ``urltype`` (string) - A string describing the type of URL provided. Valid values are one of the following: ``"Contact", "Facility Access", "Overview", "Policy", "Rates", "Research", "Service", "Spectrometers"``
* ``url`` (string) - The URL to the web page.

**Staff Fields:**

A staff member at the facility.

* ``first_name`` (string) - The staff member's given name(s).
* ``last_name`` (string) - The staff member's family name(s).
* ``middle_initial`` (string) - The staff member's middle initial(s).
* ``work_phone`` (string) - The staff member's work phone number.
* ``mobile_phone`` (string) - The staff member's mobile phone number.
* ``email`` (string) - The staff member's e-mail.
* ``roles`` (string[]) - The staff member's roles. A list of one or more of the following strings: ``"Administrator", "Director", "Engineer", "FacilityManager", "Researcher", "Technician", "Approver"``
* ``responsibilities`` (string) - The staff member's responsibilties. A list of one or more of the following strings: ``"Administrative Services", "Equipment Maintenance", "Experiment Support", "Sample Shipping and Handling", "Scheduling"``
* ``expertise`` (string) - The staff member's expertise. A list of one or more of the following strings: ``"Bruker", "DNA/RNA", "Material", "Metabolomics", "Protein", "Pulse Sequence Programming", "Rotor Packing", "Small Molecule", "Solid State", "Solution", "Varian", "Carbohydrates"``

**Contact Fields:**

A contact at the facility, who may or may not also be a staff member.

* ``name`` (string) - The contact's name.
* ``work_phone`` (string) - The contact's work phone number.
* ``mobile_phone`` (string) - The contact's mobile phone.
* ``email`` (string) - The contact's e-mail address.
* ``details`` (string) - Details about the contact, or under what circumstances they are the appropriate contact.
* ``responsibilities`` (string[]) - The staff member's responsibilties. A list of one or more of the following strings: ``"Administrative Services", "Equipment Maintenance", "Experiment Support", "Sample Shipping and Handling", "Scheduling"``

**Address Fields:**

An address associated with the facility.

* ``address_type`` (string[]) - The type of the address record. One or more of the following strings: ``"Physical", "Mailing", "Shipping"``
* ``address1`` (string) - The first line of the facility address.
* ``address2`` (string) - The second line of the facility address.
* ``address3`` (string) - The third line of the facility address.
* ``city`` (string) - The city the address is located at.
* ``state`` (string) - The state the address is located at.
* ``zipcode`` (string) - The zip code of the address.
* ``zipcode_ext`` (string) - The zip code extension of the address.
* ``country`` (string) - The country of the address.

Spectrometers Endpoint
~~~~~~~~~~~~~~~~~~~~~~

**API Endpoints:**

* ``GET /nan/public/instruments`` - List all spectrometers/instruments
* ``GET /nan/public/instruments/{instrument_id}`` - Retrieve a specific spectrometer by ID

**JSON Response Structure:**

.. code-block:: json

   {
     "identifier": "string",
     "name": "string",
     "year_commissioned": 0,
     "status": "string",
     "is_public": true,
     "rates_url": "string",
     "magnet_vendor": "string",
     "field_strength_mhz": 0.0,
     "bore_mm": 0.0,
     "is_pumped": true,
     "console_vendor": "string",
     "model": "string",
     "serial_no": "string",
     "year_configured": 0,
     "channel_count": 0,
     "receiver_count": 0,
     "operating_system": "string",
     "version": "string",
     "sample_changer_id": 0,
     "facility_identifier": "string",
     "sample_changer_default_temperature_control": true,
     "sample_changer": {
       "model": "string",
       "vendor": "string",
       "min_temp": 0.0,
       "max_temp": 0.0,
       "num_spinners": 0,
       "num_96_racks": 0
     },
     "software": {
       "software": "string",
       "versions": [
         {
           "version": "string",
           "installed_software": ["string"]
         }
       ]
     },
     "installed_probe": {
       "identifier": "string"
     },
     "compatible_probes": [
       {
         "identifier": "string"
       }
     ],
     "install_schedule": [
       {
         "identifier": "string",
         "install_start": "string"
       }
     ],
     "field_drifts": [
       {
         "rate": 0.0,
         "recorded": "string"
       }
     ]
   }

**Response Fields:**

* ``identifier`` - [Add description]
* ``name`` - [Add description]
* ``year_commissioned`` - [Add description]
* ``status`` - [Add description]
* ``is_public`` - [Add description]
* ``rates_url`` - [Add description]
* ``magnet_vendor`` - [Add description]
* ``field_strength_mhz`` - [Add description]
* ``bore_mm`` - [Add description]
* ``is_pumped`` - [Add description]
* ``console_vendor`` - [Add description]
* ``model`` - [Add description]
* ``serial_no`` - [Add description]
* ``year_configured`` - [Add description]
* ``channel_count`` - [Add description]
* ``receiver_count`` - [Add description]
* ``operating_system`` - [Add description]
* ``version`` - [Add description]
* ``sample_changer_id`` - [Add description]
* ``facility_identifier`` - [Add description]
* ``sample_changer_default_temperature_control`` - [Add description]

**Sample Changer Object Fields:**

* ``model`` - [Add description]
* ``vendor`` - [Add description]
* ``min_temp`` - [Add description]
* ``max_temp`` - [Add description]
* ``num_spinners`` - [Add description]
* ``num_96_racks`` - [Add description]

**Software Object Fields:**

* ``software`` - [Add description]
* ``versions`` - [Add description]

**Software Version Object Fields:**

* ``version`` - [Add description]
* ``installed_software`` - [Add description]

**Installed Probe Object Fields:**

* ``identifier`` - [Add description]

**Install Schedule Object Fields:**

* ``identifier`` - [Add description]
* ``install_start`` - [Add description]

**Field Drift Object Fields:**

* ``rate`` - [Add description]
* ``recorded`` - [Add description]

Probes Endpoint
~~~~~~~~~~~~~~~

**API Endpoints:**

* ``GET /nan/public/probes`` - List all probes
* ``GET /nan/public/probes/{probe_id}`` - Retrieve a specific probe by ID

**JSON Response Structure:**

.. code-block:: json

   {
     "identifier": "string",
     "status": "string",
     "status_detail": "string",
     "kind": "string",
     "vendor": "string",
     "model": "string",
     "serial_number": "string",
     "cooling": "string",
     "sample_diameter": 0.0,
     "max_spinning_rate": 0.0,
     "gradient": true,
     "x_gradient_field_strength": 0.0,
     "y_gradient_field_strength": 0.0,
     "z_gradient_field_strength": 0.0,
     "h1_fieldstrength_mhz": 0.0,
     "min_temperature_c": 0.0,
     "max_temperature_c": 0.0,
     "facility_identifier": "string",
     "facility_short_name": "string",
     "facility_long_name": "string",
     "installed_on": {
       "spectrometer_identifier": "string",
       "install_start": "string"
     },
     "channels": [
       {
         "ch_number": 0,
         "amplifier_cooled": true,
         "inner_coil": "string",
         "outer_coil": "string",
         "min_frequency_nucleus": 0.0,
         "max_frequency_nucleus": 0.0,
         "broadband": true,
         "nuclei": [
           {
             "nucleus": "string",
             "sensitivity_measurements": [
               {
                 "is_user": true,
                 "sensitivity": 0.0,
                 "measurement_date": "string",
                 "name": "string",
                 "composition": "string"
               }
             ]
           }
         ]
       }
     ]
   }

**Response Fields:**

* ``identifier`` - [Add description]
* ``status`` - [Add description]
* ``status_detail`` - [Add description]
* ``kind`` - [Add description]
* ``vendor`` - [Add description]
* ``model`` - [Add description]
* ``serial_number`` - [Add description]
* ``cooling`` - [Add description]
* ``sample_diameter`` - [Add description]
* ``max_spinning_rate`` - [Add description]
* ``gradient`` - [Add description]
* ``x_gradient_field_strength`` - [Add description]
* ``y_gradient_field_strength`` - [Add description]
* ``z_gradient_field_strength`` - [Add description]
* ``h1_fieldstrength_mhz`` - [Add description]
* ``min_temperature_c`` - [Add description]
* ``max_temperature_c`` - [Add description]
* ``facility_identifier`` - [Add description]
* ``facility_short_name`` - [Add description]
* ``facility_long_name`` - [Add description]

**Installed On Object Fields:**

* ``spectrometer_identifier`` - [Add description]
* ``install_start`` - [Add description]

**Channel Object Fields:**

* ``ch_number`` - [Add description]
* ``amplifier_cooled`` - [Add description]
* ``inner_coil`` - [Add description]
* ``outer_coil`` - [Add description]
* ``min_frequency_nucleus`` - [Add description]
* ``max_frequency_nucleus`` - [Add description]
* ``broadband`` - [Add description]
* ``nuclei`` - [Add description]

**Nucleus Object Fields:**

* ``nucleus`` - [Add description]
* ``sensitivity_measurements`` - [Add description]

**Sensitivity Measurement Object Fields:**

* ``is_user`` - [Add description]
* ``sensitivity`` - [Add description]
* ``measurement_date`` - [Add description]
* ``name`` - [Add description]
* ``composition`` - [Add description]

