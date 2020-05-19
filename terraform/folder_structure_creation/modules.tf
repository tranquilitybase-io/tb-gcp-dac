# python app writes to this file to determine what modules get executed and how many times

# example follows - this would be written by python app before terraform executed
resource "google_folder" "department1" {
  display_name = "Department 1"
  parent       = "folder/${var.root_id}"
}

# Folder nested under another folder.
resource "google_folder" "team-abc" {
  display_name = "Team ABC"
  parent       = google_folder.department1.name
}

