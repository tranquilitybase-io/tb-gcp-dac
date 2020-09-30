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
# Workspace Project  Creation
###

provider "google-beta" {
  region = var.region
  zone = var.region_zone
  project = var.shared_vpc_host_project
  version = "~> 3.17"
}

resource "google_project" "workspace_project" {
  name = "${var.solution_name}-workspace"
  project_id = "workspace-${var.random_element}-${var.tb_discriminator}"
  folder_id = var.folder_id
  billing_account = var.billing_account
  labels = {
    "cost-code" = var.cost_code,
    "business-unit" = var.business_unit
    "solution-id" = var.solution_id
    "created-by" = var.created_by
    "team" = var.team
  }
}

resource "google_project_iam_binding" "project_member" {
  project = google_project.workspace_project.project_id
  role = var.project_access_role
  members = var.team_members
}

resource "google_folder_iam_binding" "folder_member" {
  folder = var.folder_id
  role = var.folder_access_role
  members = var.team_members
}

resource "google_project_service" "workspace" {
  project = google_project.workspace_project.project_id
  service = "compute.googleapis.com"
  depends_on = [
    google_project.workspace_project]
}

resource "google_compute_shared_vpc_service_project" "workspace_service" {
  count = (var.shared_vpc_host_project != "dummy" ? 1 : 0)
  host_project = var.shared_vpc_host_project
  service_project = google_project.workspace_project.project_id
  provider = google-beta
  depends_on = [
    google_project_service.workspace]
}
