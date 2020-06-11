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
# $1 - name of repo
# $2 - project to create repo in
# $3 - project to switch back to
# TODO add validation of params and better error handling
exec >> /var/log/create_gcp_repo.log 2>&1
echo "$(date) Creating GCP Repo ${1} in ${2}"
gcloud config set project $2
gcloud services enable sourcerepo.googleapis.com
gcloud source repos create $1
gcloud config set project $3
echo "$(date) Created GCP Repo ${1} in ${2}"
