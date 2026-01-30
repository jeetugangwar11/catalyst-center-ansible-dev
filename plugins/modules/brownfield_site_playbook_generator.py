#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) 2026, Cisco Systems
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module to generate YAML playbooks for Site Workflow Manager from Cisco Catalyst Center."""
from __future__ import absolute_import, division, print_function

__metaclass__ = type
__author__ = "Vidhya Rathinam"

DOCUMENTATION = r"""
---
module: brownfield_site_playbook_generator
short_description: Generate YAML playbook for 'site_workflow_manager' module.
description:
- Generates YAML configurations compatible with the `site_workflow_manager`
  module, reducing the effort required to manually create Ansible playbooks and
  enabling programmatic modifications.
- The YAML configurations generated represent the site hierarchy (areas, buildings, floors)
  configured on the Cisco Catalyst Center.
version_added: 6.45.0
extends_documentation_fragment:
- cisco.dnac.workflow_manager_params
author:
- Vidhya Rathinam (@VidhyaGit)
options:
  config_verify:
    description: Set to True to verify the Cisco Catalyst
      Center after applying the playbook config.
    type: bool
    default: false
  state:
    description: The desired state of Cisco Catalyst Center after module execution.
    type: str
    choices: [gathered]
    default: gathered
  config:
    description:
    - A list of filters for generating YAML playbook compatible with the `site_workflow_manager`
      module.
    - Filters specify which components to include in the YAML configuration file.
    - If "components_list" is specified, only those components are included, regardless of the filters.
    type: list
    elements: dict
    required: true
    suboptions:
      generate_all_configurations:
        description:
          - When set to True, automatically generates YAML configurations for all sites and all supported site types.
          - This mode discovers all managed sites in Cisco Catalyst Center and extracts all supported configurations.
          - When enabled, the config parameter becomes optional and will use default values if not provided.
          - A default filename will be generated automatically if file_path is not specified.
          - This is useful for complete brownfield infrastructure discovery and documentation.
        type: bool
        required: false
        default: false
      file_path:
        description:
        - Path where the YAML configuration file will be saved.
        - If not provided, the file will be saved in the current working directory with
          a default file name  "<module_name>_playbook_<YYYY-MM-DD_HH-MM-SS>.yml".
        - For example, "site_workflow_manager_playbook_2026-01-24_12-33-20.yml".
        type: str
      component_specific_filters:
        description:
          - Filters to specify which components to include in the YAML configuration
            file.
          - If "components_list" is specified, only those components are included,
            regardless of other filters.
        type: dict
        suboptions:
          components_list:
            description:
            - List of components to include in the YAML configuration file.
            - Valid values are
              - Area "area"
              - Building "building"
              - Floor "floor"
            - If not specified, all components are included.
            - For example, ["area", "building", "floor"].
            type: list
            elements: str
          areas:
            description:
            - Areas to filter sites by site name or parent site name.
            type: list
            elements: dict
            suboptions:
              site_name:
                description:
                - Site name to filter areas by area name.
                type: str
              parent_site_name:
                description:
                - Parent site name to filter areas by parent site name.
                type: str
          buildings:
            description:
            - Buildings to filter sites by site name or parent site name.
            type: list
            elements: dict
            suboptions:
              site_name:
                description:
                - Site name to filter buildings by building name.
                type: str
              parent_site_name:
                description:
                - Parent site name to filter buildings by parent site name.
                type: str
          floors:
            description:
            - Floors to filter sites by site name, parent site name, or RF model.
            type: list
            elements: dict
            suboptions:
              site_name:
                description:
                - Site name to filter floors by floor name.
                type: str
              parent_site_name:
                description:
                - Parent site name to filter floors by parent site name.
                type: str
              rf_model:
                description:
                - RF model to filter floors by RF model type.
                type: str
requirements:
- dnacentersdk >= 2.3.7.9
- python >= 3.9
notes:
- SDK Methods used are
    - sites.Sites.get_sites
- Paths used are
    - GET /dna/intent/api/v1/sites
"""

EXAMPLES = r"""
- name: Auto-generate YAML Configuration for all site components which
     includes areas, buildings, and floors.
  cisco.dnac.brownfield_site_playbook_generator:
    dnac_host: "{{dnac_host}}"
    dnac_username: "{{dnac_username}}"
    dnac_password: "{{dnac_password}}"
    dnac_verify: "{{dnac_verify}}"
    dnac_port: "{{dnac_port}}"
    dnac_version: "{{dnac_version}}"
    dnac_debug: "{{dnac_debug}}"
    dnac_log: true
    dnac_log_level: "{{dnac_log_level}}"
    state: gathered
    config:
      - generate_all_configurations: true

- name: Generate YAML Configuration with File Path specified
  cisco.dnac.brownfield_site_playbook_generator:
    dnac_host: "{{dnac_host}}"
    dnac_username: "{{dnac_username}}"
    dnac_password: "{{dnac_password}}"
    dnac_verify: "{{dnac_verify}}"
    dnac_port: "{{dnac_port}}"
    dnac_version: "{{dnac_version}}"
    dnac_debug: "{{dnac_debug}}"
    dnac_log: true
    dnac_log_level: "{{dnac_log_level}}"
    state: gathered
    config:
      - file_path: "/tmp/catc_site_components_config.yaml"

- name: Generate YAML Configuration with specific area components only
  cisco.dnac.brownfield_site_playbook_generator:
    dnac_host: "{{dnac_host}}"
    dnac_username: "{{dnac_username}}"
    dnac_password: "{{dnac_password}}"
    dnac_verify: "{{dnac_verify}}"
    dnac_port: "{{dnac_port}}"
    dnac_version: "{{dnac_version}}"
    dnac_debug: "{{dnac_debug}}"
    dnac_log: true
    dnac_log_level: "{{dnac_log_level}}"
    state: gathered
    config:
      - file_path: "/tmp/catc_site_components_config.yaml"
        component_specific_filters:
          components_list: ["area"]

- name: Generate YAML Configuration with specific building components only
  cisco.dnac.brownfield_site_playbook_generator:
    dnac_host: "{{dnac_host}}"
    dnac_username: "{{dnac_username}}"
    dnac_password: "{{dnac_password}}"
    dnac_verify: "{{dnac_verify}}"
    dnac_port: "{{dnac_port}}"
    dnac_version: "{{dnac_version}}"
    dnac_debug: "{{dnac_debug}}"
    dnac_log: true
    dnac_log_level: "{{dnac_log_level}}"
    state: gathered
    config:
      - file_path: "/tmp/catc_site_components_config.yaml"
        component_specific_filters:
          components_list: ["building"]

- name: Generate YAML Configuration with specific floor components only
  cisco.dnac.brownfield_site_playbook_generator:
    dnac_host: "{{dnac_host}}"
    dnac_username: "{{dnac_username}}"
    dnac_password: "{{dnac_password}}"
    dnac_verify: "{{dnac_verify}}"
    dnac_port: "{{dnac_port}}"
    dnac_version: "{{dnac_version}}"
    dnac_debug: "{{dnac_debug}}"
    dnac_log: true
    dnac_log_level: "{{dnac_log_level}}"
    state: gathered
    config:
      - file_path: "/tmp/catc_site_components_config.yaml"
        component_specific_filters:
          components_list: ["floor"]

- name: Generate YAML Configuration for areas with site name filter
  cisco.dnac.brownfield_site_playbook_generator:
    dnac_host: "{{dnac_host}}"
    dnac_username: "{{dnac_username}}"
    dnac_password: "{{dnac_password}}"
    dnac_verify: "{{dnac_verify}}"
    dnac_port: "{{dnac_port}}"
    dnac_version: "{{dnac_version}}"
    dnac_debug: "{{dnac_debug}}"
    dnac_log: true
    dnac_log_level: "{{dnac_log_level}}"
    state: gathered
    config:
      - file_path: "/tmp/catc_site_components_config.yaml"
        component_specific_filters:
          components_list: ["area"]
          areas:
            - site_name: "Global/USA"
            - site_name: "Global/Europe"

- name: Generate YAML Configuration for buildings and floors with multiple filters
  cisco.dnac.brownfield_site_playbook_generator:
    dnac_host: "{{dnac_host}}"
    dnac_username: "{{dnac_username}}"
    dnac_password: "{{dnac_password}}"
    dnac_verify: "{{dnac_verify}}"
    dnac_port: "{{dnac_port}}"
    dnac_version: "{{dnac_version}}"
    dnac_debug: "{{dnac_debug}}"
    dnac_log: true
    dnac_log_level: "{{dnac_log_level}}"
    state: gathered
    config:
      - file_path: "/tmp/catc_site_components_config.yaml"
        component_specific_filters:
          components_list: ["building", "floor"]
          buildings:
            - site_name: "Global/USA/San Jose/Building1"
            - site_name: "Global/USA/San Jose/Building2"
          floors:
            - parent_site_name: "Global/USA/San Jose/Building1"
            - rf_model: "Cubes And Walled Offices"
"""


RETURN = r"""
# Case_1: Success Scenario
response_1:
  description: A dictionary with the response returned by the Cisco Catalyst Center Python SDK
  returned: always
  type: dict
  sample: >
    {
      "response":
        {
          "response": String,
          "version": String
        },
      "msg": String
    }
# Case_2: Error Scenario
response_2:
  description: A string with the response returned by the Cisco Catalyst Center Python SDK
  returned: always
  type: list
  sample: >
    {
      "response": [],
      "msg": String
    }
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cisco.dnac.plugins.module_utils.brownfield_helper import (
    BrownFieldHelper,
    SingleQuotedStr,
    DoubleQuotedStr,
)
from ansible_collections.cisco.dnac.plugins.module_utils.dnac import (
    DnacBase,
)
from ansible_collections.cisco.dnac.plugins.module_utils.validation import (
    validate_list_of_dicts,
)
import time
import logging

try:
    import yaml

    HAS_YAML = True
except ImportError:
    HAS_YAML = False
    yaml = None
from collections import OrderedDict

LOGGER = logging.getLogger(__name__)


if HAS_YAML:

    class OrderedDumper(yaml.Dumper):
        def represent_dict(self, data):
            LOGGER.debug(
                "Entering OrderedDumper.represent_dict with data type: %s",
                type(data),
            )
            LOGGER.debug("Exiting OrderedDumper.represent_dict")
            return self.represent_mapping("tag:yaml.org,2002:map", data.items())

    OrderedDumper.add_representer(OrderedDict, OrderedDumper.represent_dict)
else:
    OrderedDumper = None


class SitePlaybookGenerator(DnacBase, BrownFieldHelper):
    """
    A class for generator playbook files for site hierarchy deployed within the Cisco Catalyst Center using the GET APIs.
    """

    values_to_nullify = ["NOT CONFIGURED"]

    def __init__(self, module):
        """
        Initialize an instance of the class.
        Args:
            module: The module associated with the class instance.
        Returns:
            The method does not return a value.
        """
        LOGGER.debug("Entering SitePlaybookGenerator.__init__")
        self.supported_states = ["gathered"]
        super().__init__(module)
        self.module_schema = self.get_workflow_elements_schema()
        self.module_name = "site_workflow_manager"
        self.log(
            f"Exiting SitePlaybookGenerator.__init__ with module_name={self.module_name}",
            "INFO",
        )

    def validate_input(self):
        """
        Validates the input configuration parameters for the playbook.
        Returns:
            object: An instance of the class with updated attributes:
                self.msg: A message describing the validation result.
                self.status: The status of the validation (either "success" or "failed").
                self.validated_config: If successful, a validated version of the "config" parameter.
        """
        self.log("Starting validation of input configuration parameters.", "INFO")

        # Check if configuration is available
        if not self.config:
            self.log("Entering if: configuration not provided", "INFO")
            self.status = "success"
            self.msg = "Configuration is not available in the playbook for validation"
            self.log(f"{self.msg}", "ERROR")
            self.log("Exiting validate_input", "INFO")
            return self

        # Expected schema for configuration parameters
        temp_spec = {
            "generate_all_configurations": {
                "type": "bool",
                "required": False,
                "default": False,
            },
            "file_path": {"type": "str", "required": False},
            "component_specific_filters": {"type": "dict", "required": False},
            "global_filters": {"type": "dict", "required": False},
        }

        # Validate params
        self.log("Validating configuration against schema.", "INFO")
        valid_temp, invalid_params = validate_list_of_dicts(self.config, temp_spec)

        if invalid_params:
            self.log("Entering if: invalid_params found", "INFO")
            self.msg = f"Invalid parameters in playbook: {invalid_params}"
            self.set_operation_result("failed", False, self.msg, "ERROR")
            self.log("Exiting validate_input", "INFO")
            return self

        # Set the validated configuration and update the result with success status
        self.validated_config = valid_temp
        self.msg = (
            "Successfully validated playbook configuration parameters using 'validated_input': "
            f"{valid_temp}"
        )
        self.set_operation_result("success", False, self.msg, "INFO")
        self.log("Exiting validate_input", "INFO")
        return self

    def get_workflow_elements_schema(self):
        """
        Description:
            Constructs and returns a structured mapping for managing various site elements
            such as areas, buildings, and floors. This mapping includes associated filters,
            temporary specification functions, API details, and fetch function references
            used in the site workflow orchestration process.

        Args:
            self: Refers to the instance of the class containing definitions of helper methods.

        Return:
            dict: A dictionary with site element configurations.
        """
        self.log("Entering get_workflow_elements_schema", "INFO")

        schema = {
            "network_elements": {
                "areas": {
                    "filters": ["site_name", "parent_site_name"],
                    "reverse_mapping_function": self.area_temp_spec,
                    "api_function": "get_sites",
                    "api_family": "site_design",
                    "get_function_name": self.get_areas_configuration,
                },
                "buildings": {
                    "filters": ["site_name", "parent_site_name"],
                    "reverse_mapping_function": self.building_temp_spec,
                    "api_function": "get_sites",
                    "api_family": "site_design",
                    "get_function_name": self.get_buildings_configuration,
                },
                "floors": {
                    "filters": ["site_name", "parent_site_name", "rf_model"],
                    "reverse_mapping_function": self.floor_temp_spec,
                    "api_function": "get_sites",
                    "api_family": "site_design",
                    "get_function_name": self.get_floors_configuration,
                },
            },
            "global_filters": [],
        }
        self.log("Exiting get_workflow_elements_schema", "INFO")
        return schema

    def get_parent_name(self, detail):
        """
        Derives parent_name from available fields in site detail.
        """
        self.log("Entering get_parent_name", "INFO")

        if not isinstance(detail, dict):
            self.log("Entering if: detail is not a dict", "INFO")
            self.log("Exiting get_parent_name with None", "INFO")
            return None

        parent_name = detail.get("parentName") or detail.get("parent_name")
        if parent_name:
            self.log("Entering if: parent_name found", "INFO")
            self.log("Exiting get_parent_name with parent_name", "INFO")
            return SingleQuotedStr(parent_name)

        name = detail.get("name")
        name_hierarchy = (
            detail.get("nameHierarchy")
            or detail.get("siteNameHierarchy")
            or detail.get("parentNameHierarchy")
        )

        if name and name_hierarchy:
            self.log("Entering if: name and name_hierarchy available", "INFO")
            token = "/" + str(name)
            if token in name_hierarchy:
                self.log("Entering if: token found in name_hierarchy", "INFO")
                self.log("Exiting get_parent_name with derived parent", "INFO")
                return SingleQuotedStr(name_hierarchy.split(token)[0])

        self.log("Exiting get_parent_name with None", "INFO")
        return None

    def get_site_type_area(self, detail):
        self.log("Entering get_site_type_area", "INFO")
        self.log("Exiting get_site_type_area with 'area'", "INFO")
        return "area"

    def get_site_type_building(self, detail):
        self.log("Entering get_site_type_building", "INFO")
        self.log("Exiting get_site_type_building with 'building'", "INFO")
        return "building"

    def get_site_type_floor(self, detail):
        self.log("Entering get_site_type_floor", "INFO")
        self.log("Exiting get_site_type_floor with 'floor'", "INFO")
        return "floor"

    def normalize_component_specific_filters(self, config):
        """
        Normalizes component names in component_specific_filters to match internal schema keys.
        """
        self.log("Entering normalize_component_specific_filters", "INFO")

        if not config:
            self.log("Entering if: config is empty", "INFO")
            self.log("Exiting normalize_component_specific_filters", "INFO")
            return config

        component_specific_filters = config.get("component_specific_filters")
        if not component_specific_filters:
            self.log("Entering if: component_specific_filters missing", "INFO")
            self.log("Exiting normalize_component_specific_filters", "INFO")
            return config

        component_map = {
            "area": "areas",
            "building": "buildings",
            "floor": "floors",
        }

        normalized_filters = {}
        for key, value in component_specific_filters.items():
            if key == "components_list" and isinstance(value, list):
                normalized_filters["components_list"] = [
                    component_map.get(component, component) for component in value
                ]
                continue

            normalized_key = component_map.get(key, key)
            normalized_filters[normalized_key] = value

        if normalized_filters == component_specific_filters:
            self.log("Entering if: normalized_filters unchanged", "INFO")
            self.log("Exiting normalize_component_specific_filters", "INFO")
            return config

        self.log(
            f"Normalized component_specific_filters to match internal schema keys: {normalized_filters}",
            "INFO",
        )
        updated_config = dict(config)
        updated_config["component_specific_filters"] = normalized_filters
        self.log("Exiting normalize_component_specific_filters", "INFO")
        return updated_config

    def area_temp_spec(self):
        """
        Constructs a temporary specification for areas.

        Returns:
            OrderedDict: An ordered dictionary defining the structure of area attributes.
        """

        self.log("Entering area_temp_spec", "INFO")
        self.log("Generating temporary specification for areas.", "INFO")
        area = OrderedDict(
            {
                "site": {
                    "type": "dict",
                    "options": OrderedDict(
                        {
                            "area": {
                                "type": "dict",
                                "options": OrderedDict(
                                    {
                                        "name": {"type": "str", "source_key": "name"},
                                        "parent_name": {
                                            "type": "str",
                                            "special_handling": True,
                                            "transform": self.get_parent_name,
                                        },
                                    }
                                ),
                            }
                        }
                    ),
                },
                "site_type": {
                    "type": "str",
                    "special_handling": True,
                    "transform": self.get_site_type_area,
                },
            }
        )
        self.log("Exiting area_temp_spec", "INFO")
        return area

    def building_temp_spec(self):
        """
        Constructs a temporary specification for buildings.

        Returns:
            OrderedDict: An ordered dictionary defining the structure of building attributes.
        """

        self.log("Entering building_temp_spec", "INFO")
        self.log("Generating temporary specification for buildings.", "INFO")
        building = OrderedDict(
            {
                "site": {
                    "type": "dict",
                    "options": OrderedDict(
                        {
                            "building": {
                                "type": "dict",
                                "options": OrderedDict(
                                    {
                                        "name": {"type": "str", "source_key": "name"},
                                        "parent_name": {
                                            "type": "str",
                                            "special_handling": True,
                                            "transform": self.get_parent_name,
                                        },
                                        "address": {
                                            "type": "str",
                                            "source_key": "address",
                                        },
                                        "latitude": {
                                            "type": "float",
                                            "source_key": "latitude",
                                        },
                                        "longitude": {
                                            "type": "float",
                                            "source_key": "longitude",
                                        },
                                        "country": {
                                            "type": "str",
                                            "source_key": "country",
                                            "transform": DoubleQuotedStr,
                                        },
                                    }
                                ),
                            }
                        }
                    ),
                },
                "site_type": {
                    "type": "str",
                    "special_handling": True,
                    "transform": self.get_site_type_building,
                },
            }
        )
        self.log("Exiting building_temp_spec", "INFO")
        return building

    def floor_temp_spec(self):
        """
        Constructs a temporary specification for floors.

        Returns:
            OrderedDict: An ordered dictionary defining the structure of floor attributes.
        """

        self.log("Entering floor_temp_spec", "INFO")
        self.log("Generating temporary specification for floors.", "INFO")
        floor = OrderedDict(
            {
                "site": {
                    "type": "dict",
                    "options": OrderedDict(
                        {
                            "floor": {
                                "type": "dict",
                                "options": OrderedDict(
                                    {
                                        "name": {
                                            "type": "str",
                                            "source_key": "name",
                                        },
                                        "parent_name": {
                                            "type": "str",
                                            "special_handling": True,
                                            "transform": self.get_parent_name,
                                        },
                                        "rf_model": {
                                            "type": "str",
                                            "source_key": "rfModel",
                                            "transform": SingleQuotedStr,
                                        },
                                        "length": {
                                            "type": "float",
                                            "source_key": "length",
                                        },
                                        "width": {
                                            "type": "float",
                                            "source_key": "width",
                                        },
                                        "height": {
                                            "type": "float",
                                            "source_key": "height",
                                        },
                                        "floor_number": {
                                            "type": "int",
                                            "source_key": "floorNumber",
                                        },
                                        "units_of_measure": {
                                            "type": "str",
                                            "source_key": "unitsOfMeasure",
                                            "transform": DoubleQuotedStr,
                                        },
                                    }
                                ),
                            }
                        }
                    ),
                },
                "site_type": {
                    "type": "str",
                    "special_handling": True,
                    "transform": self.get_site_type_floor,
                },
            }
        )
        self.log("Exiting floor_temp_spec", "INFO")
        return floor

    def get_areas_configuration(self, network_element, component_specific_filters=None):
        """
        Retrieves areas based on the provided network element and component-specific filters.

        Args:
            network_element (dict): A dictionary containing the API family and function for retrieving areas.
            component_specific_filters (list, optional): A list of dictionaries containing filters for areas.

        Returns:
            dict: A dictionary containing the modified details of areas.
        """

        self.log("Entering get_areas_configuration", "INFO")
        self.log(
            f"Starting to retrieve areas with network element: {network_element} and component-specific filters: {component_specific_filters}",
            "INFO",
        )

        final_areas = []
        api_family = network_element.get("api_family")
        api_function = network_element.get("api_function")

        self.log(
            f"Getting areas using family '{api_family}' and function '{api_function}'.",
            "INFO",
        )

        params = {"type": "area"}

        if component_specific_filters:
            self.log("Entering if: component_specific_filters provided", "INFO")
            for filter_param in component_specific_filters:
                self.log(f"Processing filter parameter: {filter_param}", "INFO")
                desired_parent_name = None
                for key, value in filter_param.items():
                    if key == "site_name":
                        self.log("Entering if: site_name filter detected", "INFO")
                        params["name"] = value
                    elif key == "parent_site_name":
                        self.log(
                            "Entering elif: parent_site_name filter detected", "INFO"
                        )
                        desired_parent_name = value
                    else:
                        self.log(
                            f"Ignoring unsupported filter parameter: {key}",
                            "INFO",
                        )

                area_details = self.execute_get_with_pagination(
                    api_family, api_function, params
                )
                if desired_parent_name:
                    self.log("Entering if: desired_parent_name provided", "INFO")
                    area_details = [
                        area
                        for area in area_details
                        if self.get_parent_name(area) == desired_parent_name
                    ]
                self.log(f"Retrieved area details: {area_details}", "INFO")
                final_areas.extend(area_details)
                params = {"type": "area"}
        else:
            self.log("Entering else: no component_specific_filters provided", "INFO")
            area_details = self.execute_get_with_pagination(
                api_family, api_function, params
            )
            self.log(f"Retrieved area details: {area_details}", "INFO")
            final_areas.extend(area_details)

        # Modify area details using temp_spec
        area_temp_spec = self.area_temp_spec()
        areas_details = self.modify_parameters(area_temp_spec, final_areas)

        self.log(
            f"Modified area details: {areas_details}",
            "INFO",
        )

        self.log("Exiting get_areas_configuration", "INFO")
        return areas_details

    def get_buildings_configuration(
        self, network_element, component_specific_filters=None
    ):
        """
        Retrieves buildings based on the provided network element and component-specific filters.

        Args:
            network_element (dict): A dictionary containing the API family and function for retrieving buildings.
            component_specific_filters (list, optional): A list of dictionaries containing filters for buildings.

        Returns:
            dict: A dictionary containing the modified details of buildings.
        """

        self.log("Entering get_buildings_configuration", "INFO")
        self.log(
            f"Starting to retrieve buildings with network element: {network_element} and component-specific filters: {component_specific_filters}",
            "INFO",
        )

        final_buildings = []
        api_family = network_element.get("api_family")
        api_function = network_element.get("api_function")

        self.log(
            f"Getting buildings using family '{api_family}' and function '{api_function}'.",
            "INFO",
        )

        params = {"type": "building"}

        if component_specific_filters:
            self.log("Entering if: component_specific_filters provided", "INFO")
            for filter_param in component_specific_filters:
                desired_parent_name = None
                for key, value in filter_param.items():
                    if key == "site_name":
                        self.log("Entering if: site_name filter detected", "INFO")
                        params["name"] = value
                    elif key == "parent_site_name":
                        self.log(
                            "Entering elif: parent_site_name filter detected", "INFO"
                        )
                        desired_parent_name = value
                    else:
                        self.log(
                            f"Ignoring unsupported filter parameter: {key}",
                            "INFO",
                        )

                building_details = self.execute_get_with_pagination(
                    api_family, api_function, params
                )
                if desired_parent_name:
                    self.log("Entering if: desired_parent_name provided", "INFO")
                    building_details = [
                        building
                        for building in building_details
                        if self.get_parent_name(building) == desired_parent_name
                    ]
                self.log(f"Retrieved building details: {building_details}", "INFO")
                final_buildings.extend(building_details)
                params = {"type": "building"}
        else:
            self.log("Entering else: no component_specific_filters provided", "INFO")
            building_details = self.execute_get_with_pagination(
                api_family, api_function, params
            )
            self.log(f"Retrieved building details: {building_details}", "INFO")
            final_buildings.extend(building_details)

        # Modify building details using temp_spec
        building_temp_spec = self.building_temp_spec()
        buildings_details = self.modify_parameters(building_temp_spec, final_buildings)

        self.log(
            f"Modified building details: {buildings_details}",
            "INFO",
        )

        self.log("Exiting get_buildings_configuration", "INFO")
        return buildings_details

    def get_floors_configuration(
        self, network_element, component_specific_filters=None
    ):
        """
        Retrieves floors based on the provided network element and component-specific filters.

        Args:
            network_element (dict): A dictionary containing the API family and function for retrieving floors.
            component_specific_filters (list, optional): A list of dictionaries containing filters for floors.

        Returns:
            dict: A dictionary containing the modified details of floors.
        """

        self.log("Entering get_floors_configuration", "INFO")
        self.log(
            f"Starting to retrieve floors with network element: {network_element} and component-specific filters: {component_specific_filters}",
            "INFO",
        )

        final_floors = []
        api_family = network_element.get("api_family")
        api_function = network_element.get("api_function")

        self.log(
            f"Getting floors using family '{api_family}' and function '{api_function}'.",
            "INFO",
        )

        params = {"type": "floor"}

        if component_specific_filters:
            self.log("Entering if: component_specific_filters provided", "INFO")
            for filter_param in component_specific_filters:
                desired_parent_name = None
                for key, value in filter_param.items():
                    if key == "site_name":
                        self.log("Entering if: site_name filter detected", "INFO")
                        params["name"] = value
                    elif key == "parent_site_name":
                        self.log(
                            "Entering elif: parent_site_name filter detected", "INFO"
                        )
                        desired_parent_name = value
                    elif key == "rf_model":
                        self.log("Entering elif: rf_model filter detected", "INFO")
                        # RF model filtering will be done post-retrieval
                        pass
                    else:
                        self.log(
                            f"Ignoring unsupported filter parameter: {key}",
                            "INFO",
                        )

                floor_details = self.execute_get_with_pagination(
                    api_family, api_function, params
                )
                self.log(f"Retrieved floor details: {floor_details}", "INFO")

                if desired_parent_name:
                    self.log("Entering if: desired_parent_name provided", "INFO")
                    floor_details = [
                        floor
                        for floor in floor_details
                        if self.get_parent_name(floor) == desired_parent_name
                    ]

                # Filter by RF model if specified
                if "rf_model" in filter_param:
                    self.log("Entering if: rf_model present in filter_param", "INFO")
                    rf_model = filter_param["rf_model"]
                    filtered_floors = [
                        floor
                        for floor in floor_details
                        if floor.get("rfModel") == rf_model
                    ]
                    final_floors.extend(filtered_floors)
                else:
                    self.log("Entering else: no rf_model filter applied", "INFO")
                    final_floors.extend(floor_details)

                params = {"type": "floor"}
        else:
            self.log("Entering else: no component_specific_filters provided", "INFO")
            floor_details = self.execute_get_with_pagination(
                api_family, api_function, params
            )
            self.log(f"Retrieved floor details: {floor_details}", "INFO")
            final_floors.extend(floor_details)

        # Modify floor details using temp_spec
        floor_temp_spec = self.floor_temp_spec()
        floors_details = self.modify_parameters(floor_temp_spec, final_floors)

        self.log(
            f"Modified floor details: {floors_details}",
            "INFO",
        )

        self.log("Exiting get_floors_configuration", "INFO")
        return floors_details

    def yaml_config_generator(self, yaml_config_generator):
        """
        Generates a YAML configuration file based on the provided parameters.

        Args:
            yaml_config_generator (dict): Contains file_path, global_filters, and component_specific_filters.

        Returns:
            self: The current instance with the operation result and message updated.
        """

        self.log("Entering yaml_config_generator", "INFO")
        self.log(
            f"Starting YAML config generation with parameters: {yaml_config_generator}",
            "INFO",
        )

        # Check if generate_all_configurations mode is enabled
        generate_all = yaml_config_generator.get("generate_all_configurations", False)
        if generate_all:
            self.log(
                "Auto-discovery mode enabled - will process all sites and all features",
                "INFO",
            )
        else:
            self.log("Entering else: generate_all_configurations disabled", "INFO")

        self.log("Determining output file path for YAML configuration", "INFO")
        file_path = yaml_config_generator.get("file_path")
        if not file_path:
            self.log(
                "No file_path provided by user, generating default filename", "INFO"
            )
            file_path = self.generate_filename()
        else:
            self.log(f"Using user-provided file_path: {file_path}", "INFO")

        self.log(f"YAML configuration file path determined: {file_path}", "INFO")

        self.log("Initializing filter dictionaries", "INFO")
        if generate_all:
            self.log(
                "Auto-discovery mode: Overriding any provided filters to retrieve all sites and all features",
                "INFO",
            )
            if yaml_config_generator.get("global_filters"):
                self.log(
                    "Warning: global_filters provided but will be ignored due to generate_all_configurations=True",
                    "WARNING",
                )
            if yaml_config_generator.get("component_specific_filters"):
                self.log(
                    "Warning: component_specific_filters provided but will be ignored due to generate_all_configurations=True",
                    "WARNING",
                )

            global_filters = {}
            component_specific_filters = {}
        else:
            self.log("Entering else: generate_all=False, honoring filters", "INFO")
            global_filters = yaml_config_generator.get("global_filters") or {}
            component_specific_filters = (
                yaml_config_generator.get("component_specific_filters") or {}
            )

        self.log("Retrieving supported network elements schema for the module", "INFO")
        module_supported_network_elements = self.module_schema.get(
            "network_elements", {}
        )

        self.log("Determining components list for processing", "INFO")
        components_list = component_specific_filters.get(
            "components_list", list(module_supported_network_elements.keys())
        )
        self.log(f"Components to process: {components_list}", "INFO")

        final_list = []
        for component in components_list:
            self.log(f"Processing component: {component}", "INFO")
            network_element = module_supported_network_elements.get(component)
            if not network_element:
                self.log(
                    f"Component {component} not supported by module, skipping processing",
                    "WARNING",
                )
                continue

            filters = component_specific_filters.get(component, [])
            operation_func = network_element.get("get_function_name")
            if callable(operation_func):
                self.log("Entering if: operation_func is callable", "INFO")
                details = operation_func(network_element, filters)
                self.log(f"Details retrieved for {component}: {details}", "INFO")
                if isinstance(details, list):
                    self.log("Entering if: details is list", "INFO")
                    final_list.extend(details)
                else:
                    self.log("Entering else: details is not list", "INFO")
                    final_list.append(details)

        if not final_list:
            self.log(
                "No configurations found to process, setting appropriate result",
                "WARNING",
            )
            self.msg = {
                "message": (
                    "No configurations or components to process for module "
                    f"'{self.module_name}'. Verify input filters or configuration."
                )
            }
            self.set_operation_result("ok", False, self.msg, "INFO")
            self.log("Exiting yaml_config_generator", "INFO")
            return self

        final_dict = {"config": final_list}
        self.log(f"Final dictionary created: {final_dict}", "INFO")

        if self.write_dict_to_yaml(final_dict, file_path):
            self.log("Entering if: write_dict_to_yaml succeeded", "INFO")
            self.msg = {
                f"YAML config generation Task succeeded for module '{self.module_name}'.": {
                    "file_path": file_path
                }
            }
            self.set_operation_result("success", True, self.msg, "INFO")
        else:
            self.log("Entering else: write_dict_to_yaml failed", "INFO")
            self.msg = {
                f"YAML config generation Task failed for module '{self.module_name}'.": {
                    "file_path": file_path
                }
            }
            self.set_operation_result("failed", True, self.msg, "ERROR")

        self.log("Exiting yaml_config_generator", "INFO")
        return self

    def get_want(self, config, state):
        """
        Creates parameters for API calls based on the specified state.

        Args:
            config (dict): The configuration data for the site elements.
            state (str): The desired state of the site elements ('gathered').
        """

        self.log("Entering get_want", "INFO")
        self.log(f"Creating Parameters for API Calls with state: {state}", "INFO")

        config = self.normalize_component_specific_filters(config)
        self.validate_params(config)

        # Set generate_all_configurations after validation
        self.generate_all_configurations = config.get(
            "generate_all_configurations", False
        )
        self.log(
            f"Set generate_all_configurations mode: {self.generate_all_configurations}",
            "INFO",
        )

        want = {}

        # Add yaml_config_generator to want
        want["yaml_config_generator"] = config
        self.log(
            f"yaml_config_generator added to want: {want['yaml_config_generator']}",
            "INFO",
        )

        self.want = want
        self.log(f"Desired State (want): {self.want}", "INFO")
        self.msg = "Successfully collected all parameters from the playbook for Site operations."
        self.status = "success"
        self.log("Exiting get_want", "INFO")
        return self

    def get_diff_gathered(self):
        """
        Executes the gather operations for site configurations in the Cisco Catalyst Center.
        """

        start_time = time.time()
        self.log("Entering get_diff_gathered", "INFO")
        operations = [
            (
                "yaml_config_generator",
                "YAML Config Generator",
                self.yaml_config_generator,
            )
        ]

        # Iterate over operations and process them
        self.log("Beginning iteration over defined operations for processing.", "INFO")
        for index, (param_key, operation_name, operation_func) in enumerate(
            operations, start=1
        ):
            self.log(
                f"Iteration {index}: Checking parameters for {operation_name} operation with param_key '{param_key}'.",
                "INFO",
            )
            params = self.want.get(param_key)
            if params:
                self.log(
                    f"Iteration {index}: Parameters found for {operation_name}. Starting processing.",
                    "INFO",
                )
                operation_func(params).check_return_status()
            else:
                self.log(
                    f"Iteration {index}: No parameters found for {operation_name}. Skipping operation.",
                    "WARNING",
                )

        end_time = time.time()
        self.log(
            f"Completed 'get_diff_gathered' operation in {end_time - start_time:.2f} seconds.",
            "INFO",
        )

        self.log("Exiting get_diff_gathered", "INFO")
        return self


def main():
    """main entry point for module execution"""
    LOGGER.debug("Entering main")
    # Define the specification for the module's arguments
    element_spec = {
        "dnac_host": {"required": True, "type": "str"},
        "dnac_port": {"type": "str", "default": "443"},
        "dnac_username": {"type": "str", "default": "admin", "aliases": ["user"]},
        "dnac_password": {"type": "str", "no_log": True},
        "dnac_verify": {"type": "bool", "default": True},
        "dnac_version": {"type": "str", "default": "2.2.3.3"},
        "dnac_debug": {"type": "bool", "default": False},
        "dnac_log_level": {"type": "str", "default": "WARNING"},
        "dnac_log_file_path": {"type": "str", "default": "dnac.log"},
        "dnac_log_append": {"type": "bool", "default": True},
        "dnac_log": {"type": "bool", "default": False},
        "validate_response_schema": {"type": "bool", "default": True},
        "config_verify": {"type": "bool", "default": False},
        "dnac_api_task_timeout": {"type": "int", "default": 1200},
        "dnac_task_poll_interval": {"type": "int", "default": 2},
        "config": {"required": True, "type": "list", "elements": "dict"},
        "state": {"default": "gathered", "choices": ["gathered"]},
    }

    # Initialize the Ansible module with the provided argument specifications
    module = AnsibleModule(argument_spec=element_spec, supports_check_mode=True)

    # Initialize the SitePlaybookGenerator object with the module
    ccc_site_playbook_generator = SitePlaybookGenerator(module)
    ccc_site_playbook_generator.log(
        "Initialized SitePlaybookGenerator in main", "DEBUG"
    )
    if (
        ccc_site_playbook_generator.compare_dnac_versions(
            ccc_site_playbook_generator.get_ccc_version(), "2.3.7.9"
        )
        < 0
    ):
        ccc_site_playbook_generator.log(
            "Entering if: Catalyst Center version unsupported", "DEBUG"
        )
        ccc_site_playbook_generator.msg = (
            "The specified version '{0}' does not support the YAML Playbook generation "
            "for Site Workflow Manager Module. Supported versions start from '2.3.7.9' onwards. "
            "Version '2.3.7.9' introduces APIs for retrieving site hierarchy including "
            "areas, buildings, and floors from the Catalyst Center".format(
                ccc_site_playbook_generator.get_ccc_version()
            )
        )
        ccc_site_playbook_generator.set_operation_result(
            "failed", False, ccc_site_playbook_generator.msg, "ERROR"
        ).check_return_status()

    # Get the state parameter from the provided parameters
    state = ccc_site_playbook_generator.params.get("state")

    # Check if the state is valid
    if state not in ccc_site_playbook_generator.supported_states:
        ccc_site_playbook_generator.log("Entering if: invalid state provided", "DEBUG")
        ccc_site_playbook_generator.status = "invalid"
        ccc_site_playbook_generator.msg = "State {0} is invalid".format(state)
        ccc_site_playbook_generator.check_return_status()

    # Validate the input parameters and check the return status
    ccc_site_playbook_generator.validate_input().check_return_status()
    config = ccc_site_playbook_generator.validated_config

    # Iterate over the validated configuration parameters
    for config in ccc_site_playbook_generator.validated_config:
        ccc_site_playbook_generator.log(f"Processing config entry: {config}", "DEBUG")
        ccc_site_playbook_generator.reset_values()
        ccc_site_playbook_generator.get_want(config, state).check_return_status()
        ccc_site_playbook_generator.get_diff_state_apply[state]().check_return_status()

    ccc_site_playbook_generator.log("Exiting main", "DEBUG")
    module.exit_json(**ccc_site_playbook_generator.result)


if __name__ == "__main__":
    main()
