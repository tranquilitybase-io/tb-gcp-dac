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


output "project_number" {
  description = "Number for the project created"
  value       = google_project.environment_project.*.number
}

output "project_name" {
  description = "name for the project created"
  value       = google_project.environment_project.*.name
}

output "project_id" {
  description = "id for the project created"
  value       = google_project.environment_project.*.id
}

output "projects" {
  description = "project created"
  value       = google_project.environment_project.*
}
