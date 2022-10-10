# https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/cloudfunctions_function
locals {
  timestamp = formatdate("YYMMDDhhmmss", timestamp())
	root_dir = abspath("src/${var.sourcefn}")
}

# Compress source code
data "archive_file" "source" {
  type        = "zip"
  source_dir  = local.root_dir
  output_path = "/tmp/function-${var.sourcefn}-${local.timestamp}.zip"
}

# Create bucket that will host the source code
resource "google_storage_bucket" "bucket" {
  name = "${var.project}-${var.sourcefn}-function"
  location = "US"
  uniform_bucket_level_access = true
}

# Add source code zip to bucket
resource "google_storage_bucket_object" "zip" {
  # Append file MD5 to force bucket to be recreated
  name   = "source.zip#${data.archive_file.source.output_md5}"
  bucket = google_storage_bucket.bucket.name
  source = data.archive_file.source.output_path
}

# Create Main tree Cloud Function
resource "google_cloudfunctions_function" "function" {
  name    = var.function_name
  runtime = var.runtimefn # Switch to a different runtime if needed
  available_memory_mb   = 256
  timeout               = 60
  source_archive_bucket = google_storage_bucket.bucket.name
  source_archive_object = google_storage_bucket_object.zip.name
  trigger_http          = true
  entry_point           = var.function_entry_point
  environment_variables = {
    gcp_connection_name = "",
    gcp_project_id = var.project
    gcp_table_name = ""
    gcp_table_field1 = ""
    gcp_table_field2 = ""
    gcp_db_name = ""
    
  }
}


# Create IAM entry so all users can invoke the function
resource "google_cloudfunctions_function_iam_member" "invoker" {
  project        = google_cloudfunctions_function.function.project
  region         = google_cloudfunctions_function.function.region
  cloud_function = google_cloudfunctions_function.function.name
  role   = "roles/cloudfunctions.invoker"
  member = "user:owner@estival.altostrat.com"
}
output "function_url" {
  value = google_cloudfunctions_function.function.https_trigger_url
}