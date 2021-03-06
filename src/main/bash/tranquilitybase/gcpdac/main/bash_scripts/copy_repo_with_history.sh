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
# This script copies all the code from the source repo to the gcp target repo with history
# $1 - source repo url
# $2 - name of target gcp repo
# $3 - project gcp repo is in
# $4 - project to switch back to
echo "$(date) Copying Source Repo ${1} to GCP Repo ${2}"
gcloud auth activate-service-account --key-file "$GOOGLE_APPLICATION_CREDENTIALS"
gcloud config set project "$3"
tmp_dir_source_repo=$(mktemp -d -t ci-XXXXXXXXXX)

echo "Working directory for source repo is ${tmp_dir_source_repo}"
cd "$tmp_dir_source_repo" || exit

echo "Cloning source repo from ${1}"
git clone "$1"
sourcerepodir="$(ls -d -- */)"
cd "$tmp_dir_source_repo/$sourcerepodir" || exit

echo "Configure git to allow pushing to gcp repo"
git config --global credential.'https://source.developers.google.com'.helper gcloud.sh

echo "Adding GCP repo remote ${2}"
git remote add google "https://source.developers.google.com/p/$3/r/$2"

echo "Pushing to GCP repo ${2}"
git push --all google
gcloud config set project "$4"
cd "$HOME" || exit

echo "Removing Working directory"
rm -rf "$tmp_dir_source_repo"

echo "$(date) Copied Activator Repo ${1} to GCP Repo ${2}"
