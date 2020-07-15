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
# Environment Project  Creation
###

resource "google_project" "workspace_project" {
  name = "${var.solution_name}-workspace"
  project_id = "workspace-${var.random_element}-${var.tb_discriminator}"
  folder_id = var.folder_id
  billing_account = var.billing_account
  labels = {
    "cost_centre" = var.cost_centre,
    "business_unit" = var.business_unit
    "solution_id" = var.solution_id
    "team" = var.team
  }

}

//resource "google_project_iam_binding" "project" {
//  project = "your-project-id"
//  role    = "roles/editor"
//
//  members = [
//    "user:jane@example.com",
//  ]
//}


//resource "google_project_iam_binding" "project_admin" {
//  project = google_project.workspace_project.project_id
//  role    = var.admin_role
//  members = var.team_admins
//}

resource "google_project_iam_binding" "project_member" {
  project = google_project.workspace_project.project_id
  role    = var.member_role
  members = var.team_members
}


