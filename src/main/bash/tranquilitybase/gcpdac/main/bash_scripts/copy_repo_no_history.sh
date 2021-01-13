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
# $1 - source repo url
# $2 - name of target gcp repo
# $3 - project gcp repo is in
# $4 - project to switch back to
echo "$(date) Copying Source Repo ${1} to GCP Repo ${2}"
gcloud auth activate-service-account --key-file "$GOOGLE_APPLICATION_CREDENTIALS"
gcloud config set project "$3"
tmp_dir_source_repo=$(mktemp -d -t ci-XXXXXXXXXX)
tmp_dir_gcp_repo=$(mktemp -d -t ci-XXXXXXXXXX)
echo "Working directory for source repo is ${tmp_dir_source_repo}"
echo "Working directory for gcp repo is ${tmp_dir_gcp_repo}"
cd "$tmp_dir_source_repo" || exit
# clone activator repo
git clone "$1"
sourcerepodir="$(ls -d -- */)"
# clone gcp repo
cd "$tmp_dir_gcp_repo" || exit
gcloud source repos clone "$2" --project="$3"
cd "$2" || exit
# copy activator repo to gcp repo
rsync -arv  "$tmp_dir_source_repo/$sourcerepodir" "$tmp_dir_gcp_repo/$2"--exclude .git --exclude .github
# commit and push to gcp repo
git config --global user.email "gcpdac@gft.com"
git config --global user.name "gcpdac"
git add .
git commit -m 'Push source repo code to GCP repo'
git push --all origin
gcloud config set project "$4"
cd "$HOME" || exit
# remove temporary working directories
rm -rf "$tmp_dir_source_repo"
rm -rf "$tmp_dir_gcp_repo"
echo "$(date) Copied Activator Repo ${1} to GCP Repo ${2}"
