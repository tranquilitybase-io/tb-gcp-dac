# Folder and Project Structure for a Solution

Currently very simple, creates a solutions folder

Requires a user with "roles/resourcemanager.folderCreator"

1. Authenticate to GCP using the gcloud init command, providing the email address for the GCP user

2. Amend the terraform.tfvars file accordingly

3. Run the following commands:

```
    terraform init
    terraform plan
    terraform apply
```