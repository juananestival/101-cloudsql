provider "google" {
    project = var.project
    region  = var.region
}

module "project-services" {
  source  = "terraform-google-modules/project-factory/google//modules/project_services"
  version = "~> 13.0"

  project_id                  = var.project
  activate_apis = [
    "sql-component.googleapis.com",
    "cloudresourcemanager.googleapis.com",
    "compute.googleapis.com",
    "sqladmin.googleapis.com",
    "cloudbuild.googleapis.com",
    "cloudfunctions.googleapis.com",
    "pubsub.googleapis.com",
    "secretmanager.googleapis.com",
    "dialogflow.googleapis.com"
  ]
}

module "cloudsql_postgresql_instance" {
  depends_on = [module.project-services]
  source               = "./modules/cloudSQL"
  project              = var.project
  region = var.region

}

module "python_function_main" {
  source               = "./modules/function"
  project              = var.project
  function_name        = "python-webhook"
  function_entry_point = "main"
  sourcefn             = "python"
  runtimefn              = "python310"
  region = var.region
}