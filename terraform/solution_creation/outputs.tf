output "solution_folder_id" {
  value = module.solution_folder.solution_id
}

output "workspace_project_id" {
  value = module.workspace_project.project_number
}

output "environment_project_ids" {
  value = module.environment_projects.project_number
}