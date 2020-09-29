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

variable "region" {
  type = string
  description = "region name."
}

variable "region_zone" {
  type = string
  description = "zone name in the region provided."
}

variable "deployment_folder_id" {
  type = string
  description = "id for the parent where these folders will be created."
}

variable "tb_discriminator" {
  type = string
  default = ""
  description = "suffix added to the Tranquility Base folder allowing coexistence of other TBase instances within the same Organisation/Folder. Example: 'uat', 'dev-am'. Default value is empty so no suffix will be added."
}

variable "sandbox_name" {
  type = string
  description = "name of the sandbox to be created"
}

variable "sandbox_id" {
  type = string
  description = "sandbox_id"
}

variable "billing_account" {
  type = string
  description = "billing_account"
}

variable "random_element" {
  type = string
  description = "random element introduced to ensure uniqueness"
}

variable "labels" {
  type        = map(string)
  description = "Labels to assign to resources."
}

variable "project_access_role" {
  type = string
  description = "name of the project acccess role"
  default = "roles/viewer"
}

variable "folder_access_role" {
  type = string
  description = "name of the folder access role"
  default = "roles/resourcemanager.folderViewer"
}

variable "shared_vpc_host_project" {
  type = string
  description = "shared vpc host project"
  default = "dummy"
}

