output "solution_folder_id" {
  value = module.solution_folder.solution_id
}

output "workspace_project_id" {
  value = module.workspace_project.project_number
}

output "environment_project_ids" {
  value = module.environment_projects.project_id
}

output "environment_project_names" {
  value = module.environment_projects.project_name
}

output "environment_project_numbers" {
  value = module.environment_projects.project_number
}

output "solution_folder" {
  value = module.solution_folder
}

output "workspace_project" {
  value = module.workspace_project
}

output "environment_projects" {
  value = module.environment_projects
}