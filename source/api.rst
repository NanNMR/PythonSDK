API Reference
=============

This section provides detailed documentation for the USNAN SDK API endpoints and their JSON responses.

Overview
--------

The endpoints provide access to different data objects within NAN. In this initial release, that includes:

 * Datasets (also known as experiments) (:class:`usnan.models.datasets.Dataset`)
 * Facilities (:class:`usnan.models.facilities.Facility`)
 * Spectrometers (also known as spectrometers) (:class:`usnan.models.spectrometers.Spectrometer`)
 * Probes (:class:`usnan.models.probes.Probe`)

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

* ``id`` (integer) - The unique ID of the dataset. Note that this ID refers to a specific *version* of a dataset. (Which may be the original version.)
* ``identifier`` (string) - The identifier of the dataset more broadly - allowing access to all versions of the dataset. This is used to generate the unique ARK records for a dataset.
* ``classification`` (string) - An optional classification value entered by the user. Chosen from the following: ``"Calibration experiment", "Failed-sample related", "Failed-instrument related", "Failed-setup related", "Successful experiment", "Test experiment"``
* ``dataset_name`` (string) - The name of the dataset, which can be edited by the user. If the user has edited the name, this will be a more human-readable name than the `experiment_name` which is set automatically and is immutable.
* ``decoupling_sequence`` (string) - [Add description]
* ``experiment_end_time`` (string) - The end date and time (with timezone) of the experiment.
* ``experiment_name`` (string) - The name of the experiment as ran on the spectrometer. May not be edited.
* ``experiment_start_time`` (string) - The start date and time (with timezone) of the experiment.
* ``facility_identifier`` (string) - The identifier of the facility the experiment was ran in.
* ``is_knowledgebase`` (boolean) - Whether or not the dataset has been marked as a knowledgebase.
* ``is_locked`` (boolean) - [Add description]
* ``is_multi_receiver`` (boolean) - [Add description]
* ``is_non_uniform`` (boolean) - [Add description]
* ``mas_rate`` (float) - [Add description]
* ``mixing_sequence`` (string) - [Add description]
* ``mixing_time`` (float) - [Add description]
* ``notes`` (string) - Arbitrary text notes on the dataset entered by the user.
* ``num_dimension`` (integer) - [Add description]
* ``num_dimension_collected`` (integer) - [Add description]
* ``number_in_set`` (integer) - Often multiple experiments are ran with the same `experiment_name` but only one is the actual experiment, whereas the others are calibrations or tests. This indicates how many experiments were ran in a row with the same `experiment_name`. Usually, only one of these experiments will be marked as `preferred` - the non-preferred experiments are hidden by default.
* ``preferred`` (boolean) - Whether or not the dataset has been marked as preferred out of a set. See `number_in_set` above.
* ``pi_name`` (string) - The name of the principal investigator who has authority over the dataset.
* ``public_time`` (string) - The date and time (with timezone) the dataset will become or has become public. As the current endpoint only support unauthenticated access, this will always be in the past.
* ``published_time`` (string) - The date and time (with timezone) that the dataset was published. Publishing creates an immutable copy of the metadata and data of the dataset and causes an `ARK <https://arks.org/>`_ record to be issued. Published datasets are issued a version number to allow individual published versions to be referenced.
* ``pulse_sequence`` (string) - [Add description]
* ``sample_id`` (integer) - The ID of the sample linked to the dataset.
* ``sample_sparsity`` (float) - [Add description]
* ``session_id`` (integer) - A unique session identifier. This can be used to locate other experiments ran before or after a given experiment on the same spectrometer by the same user.
* ``solvent`` (string) - [Add description]
* ``source`` (string) - Whether the dataset was captured directly by NDTS (`NDTS-auto`), whether it was manually uploaded later from the spectrometer by a facility manager (`NDTS-manual`), or whether it was uploaded via the web GUI by an arbitrary user (`NAN-arbitrary`)
* ``spectrometer_identifier`` (string) - The identifier of the spectromter the experiment was ran on. Can be used to look up the spectrometer information.
* ``state`` (string) - [Add description]
* ``tags`` (string[]) - Arbitrary text tags associated with the experiment for user convenience.
* ``temperature_k`` (float) - The temperature the spectrometer recorded the experiment was ran at.
* ``time_shared`` (boolean) - [Add description]
* ``title`` (string) - The title of the experiment. Set by the user, this is a formal title for a dataset.
* ``version`` (string) - The version of the dataset. Null for original datasets, set to a non-zero increasing number for published datasets.
* ``z0_drift_correction`` (boolean) - [Add description]

**Dimension Object Fields:**

* ``dimension`` (integer) - [Add description]
* ``nucleus`` (string) - [Add description]
* ``is_direct`` (boolean) - [Add description]
* ``spectral_width_ppm`` (float) - [Add description]
* ``maximum_evolution_time`` (float) - [Add description]
* ``num_points`` (integer) - [Add description]

**Version Object Fields:**

* ``id`` (integer) - The identifier of the dataset with the version specified.
* ``version`` (integer) - The version of the dataset with the id above.

The version object allows you to look up other versions of a given dataset.

Dataset Search Endpoint
~~~~~~~~~~~~~~~~~~~~~~~

* ``GET /nan/public/datasets/search`` - Search for datasets using various filters

Parameters:

* ``filters`` (json) - A dictionary of search filter configurations, JSON encoded. Details below.
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

Facilities Endpoints
~~~~~~~~~~~~~~~~~~~~

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

Spectrometers Endpoints
~~~~~~~~~~~~~~~~~~~~~~~


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

* ``identifier`` (uuid) - A unique identifier for the spectrometer.
* ``name`` (string) - The facility assigned name of the spectrometer.
* ``year_commissioned`` (integer) - [Add description]
* ``status`` (string) - The current status of the instrument. One of the following: ``"Decommissioned", "Operational", "Under Repair"``
* ``is_public`` (boolean) - Whether the instrument is public. Will always be true for the public (unauthenticated) API.
* ``rates_url`` (string) - A hyperlink to a page with information about usage rates.
* ``magnet_vendor`` (string) - The vendor of the spectrometer magnet. One of the following: ``"Agilent/Varian", "Bruker", "JEOL", "Q One", "Tech MAG"``
* ``field_strength_mhz`` (integer) - The field strength of the spectrometer in megahertz
* ``bore_mm`` (integer) - [Add description]
* ``is_pumped`` (boolean) - [Add description]
* ``console_vendor`` (string) - The vendor of the spectrometer console. One of the following: ``"Agilent/Varian", "Bruker", "JEOL", "Q One", "Tech MAG"``
* ``model`` (string) - The model of the spectrometer.
* ``serial_no`` (string) - The serial number of the spectrometer.
* ``year_configured`` (integer) - The year the spectrometer was configured.
* ``channel_count`` (integer) - [Add description]
* ``receiver_count`` (integer) - [Add description]
* ``operating_system`` (string) - The operating system of the spectrometer console. One of the following: ``"Windows", "RedHat", "CentOS", "Ubuntu", "Alma"``
* ``version`` (string) - The version of the operating system of the spectrometer console.
* ``sample_changer_id`` (integer) - The identifier of the sample changer in use.
* ``facility_identifier`` (string) - The identifier of the facility the spectrometer is located in.
* ``sample_changer_default_temperature_control`` (string) - The temperature control of the sample changer. One of the following: ``"Cooled", "Heated", "Room Temperature"``
* ``sample_changer`` (SampleChanger) - See below.
* ``software`` (Software) - See below.
* ``installed_probe`` (ProbeStub) - See below.
* ``compatible_probes`` (ProbeStub[]) - See below

**Sample Changer Object Fields:**

* ``model`` (string) - The model of the sample changer.
* ``vendor`` (string) - The vendor of the sample changer.
* ``min_temp`` (string) - The minimum temperature the sample changer can operate at.
* ``max_temp`` (string) - The maximum temperature the sample changer can operate at.
* ``num_spinners`` (string) - [Add description]
* ``num_96_racks`` (string) - [Add description]

**Software Object Fields:**

* ``software`` (string) - The software package installed on the spectrometer.
* ``versions`` (SoftwareVersion[]) - The versions of the software package installed on the spectrometer.

**Software Version Object Fields:**

* ``version`` (string) - The version number of the installed software
* ``installed_software`` (string[]) - An array of features of the installed software version.

**Probe Stub Object Fields:**

* ``identifier`` (uuid) - The identifier of a probe. Can be used to look up the probe using the probes endpoint.

**Install Schedule Object Fields:**

* ``identifier`` (uuid) - The identifier of the probe that was or will be installed on the `install_start` date.
* ``install_start`` (string) - A date with time and timezone that the probe was or will be installed.

**Field Drift Object Fields:**

* ``rate`` (string) - [Add description]
* ``recorded`` (string) - The date the rate was recorded.

Probes Endpoints
~~~~~~~~~~~~~~~~

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

* ``identifier`` (string) - [Add description]
* ``status`` (string) - [Add description]
* ``status_detail`` (string) - [Add description]
* ``kind`` (string) - [Add description]
* ``vendor`` (string) - [Add description]
* ``model`` (string) - [Add description]
* ``serial_number`` (string) - [Add description]
* ``cooling`` (string) - [Add description]
* ``sample_diameter`` (string) - [Add description]
* ``max_spinning_rate`` (string) - [Add description]
* ``gradient`` (string) - [Add description]
* ``x_gradient_field_strength`` (string) - [Add description]
* ``y_gradient_field_strength`` (string) - [Add description]
* ``z_gradient_field_strength`` (string) - [Add description]
* ``h1_fieldstrength_mhz`` (string) - [Add description]
* ``min_temperature_c`` (string) - [Add description]
* ``max_temperature_c`` (string) - [Add description]
* ``facility_identifier`` (string) - [Add description]
* ``facility_short_name`` (string) - [Add description]
* ``facility_long_name`` (string) - [Add description]

**Installed On Object Fields:**

* ``spectrometer_identifier`` (string) - [Add description]
* ``install_start`` (string) - [Add description]

**Channel Object Fields:**

* ``ch_number`` (string) - [Add description]
* ``amplifier_cooled`` (string) - [Add description]
* ``inner_coil`` (string) - [Add description]
* ``outer_coil`` (string) - [Add description]
* ``min_frequency_nucleus`` (string) - [Add description]
* ``max_frequency_nucleus`` (string) - [Add description]
* ``broadband`` (string) - [Add description]
* ``nuclei`` (string) - [Add description]

**Nucleus Object Fields:**

* ``nucleus`` (string) - [Add description]
* ``sensitivity_measurements`` (string) - [Add description]

**Sensitivity Measurement Object Fields:**

* ``is_user`` (string) - [Add description]
* ``sensitivity`` (string) - [Add description]
* ``measurement_date`` (string) - [Add description]
* ``name`` (string) - [Add description]
* ``composition`` (string) - [Add description]

