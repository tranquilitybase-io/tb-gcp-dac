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

variable "shared_vpc_host_project" {
  type        = string
  description = "shared vpc host project"
}

variable "environment_project_ids" {
  type        = list(string)
  description = "list of environment project ids"
}

variable "workspace_project_id" {
  type        = string
  description = "workspace project id"
}

