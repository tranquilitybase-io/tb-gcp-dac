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

###
# Environment Project Creation - creates a project for each environment specified in environments array
###

resource "google_project" "environment_project" {
  count = length(var.environments)
  name = "${var.solution_name}-${var.environments[count.index]}"
  project_id = "${var.environments[count.index]}-${var.random_element}-${var.tb_discriminator}"
  folder_id = var.folder_id
  billing_account = var.billing_account
//  labels = "${var.environments[count.index].labels}"
  labels = {
    "cost_centre" = var.cost_centre,
    "business_unit" = var.business_unit
    "solution_id" = var.solution_id
    "team" = var.team
    "environment" = var.environments[count.index]
    "created_by" = var.created_by
  }
}

resource "google_project_iam_binding" "project_member" {
  count = length(var.environments)
  project = google_project.environment_project[count.index].project_id
  role    = var.project_access_role
  members = var.team_members
}

resource "google_folder_iam_binding" "folder_member" {
  count = length(var.environments)
  folder = var.folder_id
  role    = var.folder_access_role
  members = var.team_members
}

resource "google_compute_shared_vpc_service_project" "service" {
  count = length(var.shared_vpc_host_project) > 0 ? 1 : 0
  host_project    = var.shared_vpc_host_project
  service_project = google_project.environment_project[count.index].project_id
  depends_on = [google_project.environment_project]
}

