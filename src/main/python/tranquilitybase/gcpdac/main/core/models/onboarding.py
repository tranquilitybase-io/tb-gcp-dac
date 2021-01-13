class OnboardingModel:

    def json_builder(project_id, local_repo):
        url_prefix = "https://source.cloud.google.com/"
        return {"repo_name": local_repo,
                "project_id": project_id,
                "head_link": url_prefix + project_id + "/" + local_repo + "/+/master:",
                "path_link": project_id + "/" + local_repo + "/master//",
                "browser_link": url_prefix + project_id + "/" + local_repo,
                "git_clone": "git clone " + url_prefix + "p/" + project_id + "/r/" + local_repo,
                "cloud_sdk": "gcloud source repos clone " + local_repo + " --project=" + project_id}
