# Copyright 2019 The Tranquility Base Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from python_terraform import Terraform

import config
from gcpdac.terraform_utils import terraform_init, terraform_destroy, terraform_apply
from gcpdac.utils import random_element, read_config_map

logger = config.logger

def run_terraform(folderstructuredata, terraform_command):
    # builds and destroys a folder structure
    # The configuration YAML file read by read_config_map() determines where this new infrastructure should sit
    # within a GCP project, as well as setting other properties like billing.
    # Accepts JSON content-type input.
    # returns return code and response from terraform
    tf_data = dict()
    folderStructure = folderstructuredata.get("folderStructure")

    config = read_config_map()

    # TODO implement