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
# Sandbox Project  Creation
###

resource "google_project" "sandbox_project" {
  name = var.sandbox_name
  project_id = var.sandbox_project_id
  folder_id = var.folder_id
  billing_account = var.billing_account
  labels = var.labels
  auto_create_network =  false
}

resource "google_project_service" "sandbox" {
  project = google_project.sandbox_project.project_id
  service = "compute.googleapis.com"
  depends_on = [
    google_project.sandbox_project]
}

resource "google_project_iam_binding" "project_role_1" {
  project = google_project.sandbox_project.project_id
  role = "roles/resourcemanager.projectIamAdmin"
  members = var.iam_accounts
}

resource "google_project_iam_binding" "project_role_2" {
  project = google_project.sandbox_project.project_id
  role = "roles/servicemanagement.quotaAdmin"
  members = var.iam_accounts
}

resource "google_project_iam_binding" "project_role_3" {
  project = google_project.sandbox_project.project_id
  role = "roles/serviceusage.serviceUsageAdmin"
  members = var.iam_accounts
}

resource "google_folder_iam_binding" "folder_access" {
  folder = var.folder_id
  role = "roles/resourcemanager.folderViewer"
  members = var.iam_accounts
}

