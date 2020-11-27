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
# $3 - remote (GCP) repository name
echo "$(date) Creating GCP Repo ${3} in ${2}"

gcloud auth activate-service-account --key-file "$GOOGLE_APPLICATION_CREDENTIALS"
echo "Change to ${2} . . ."
gcloud config set project "${2}"
gcloud services enable sourcerepo.googleapis.com

# REPOSITORY_NAME
gcloud source repos create "${3}"
cd "${1}" || exit
#Clone local_git_repo to gcp_remote
git config credential.helper gcloud.sh
git pull --tags --all
git remote add google https://source.developers.google.com/p/"${2}"/r/"${3}"
git push --tags --force google
git push --all google

#Unset project before exiting
gcloud config unset project

cd ..
echo "$(date) Remove local_git_repo - ${1}"
rm -rf "${1}"
echo "$(date) Created GCP Repo ${3} in ${2}"
