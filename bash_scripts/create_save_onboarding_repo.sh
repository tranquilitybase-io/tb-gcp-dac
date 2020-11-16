#!/bin/bash
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
# $1 - name of local git repo
# $2 - project to create repo in
echo "$(date) Creating GCP Repo ${1} in ${2}"

gcloud auth activate-service-account --key-file "$GOOGLE_APPLICATION_CREDENTIALS"
current_project=$(gcloud config list --format 'value(core.project)' 2>/dev/null)
gcloud config set project "$2"
gcloud services enable sourcerepo.googleapis.com
# REPOSITORY_NAME
#    Name of the repository. May contain between 3 and 63 (inclusive) lowercase letters, digits, and hyphens. Must start with a letter, and may not end with a hyphen
gcloud source repos create "$1"

#Clone local_git_repo to gcp_remote
gcloud source repos clone ${1} --project=${2}

gcloud config set project "$current_project"
echo "$(date) Created GCP Repo ${1} in ${2}"
