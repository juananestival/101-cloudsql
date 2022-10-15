# Cloud SQL
https://www.youtube.com/watch?v=iBArrntzWcU
https://github.com/terraform-google-modules/terraform-google-project-factory/issues/564

1. Create Project
2. Enable Billing

## Terraform tree
```sh
 terraform
    ├── main.tf
    └── modules
        └── cloudSQL
            ├── main.tf
            └── variables.tf
```

3. main root
```json
provider "google" {}
```

4. init terrafor to install dep
```sh
terradorm init
```
will create .terraform dir


## Enable api
First thing to write is enable api module

1. on root. Create variables.tf
```js
variable "project" {
    default = "cepf-l300-juananestival"
}
variable "region" {
    default = "us-central1"
}
```

2. Create terraform.tfvar
```js
project = "cepf-l300-juananestival"
```

3. edit the provider in main.tf

```js
provider "google" {
    project = var.project
    region  = var.region
}
```

4. enable the api on main.tf
```js
module "project-services" {
  source  = "terraform-google-modules/project-factory/google//modules/project_services"
  version = "~> 13.0"

  project_id                  = var.project
  activate_apis = [
    "sql-component.googleapis.com"
  ]
}
```

5. create the outputs.tf file

```js
output "function_enable_api" {
	value = module.project-services
}
```

6. Execute terraform init again to deploy the module
```sj
terraform init
```

7. create a service account with keys and access to enable apis 

```sh
export GOOGLE_APPLICATION_CREDENTIALS=
```

8. the service name can be taken from url
https://console.cloud.google.com/apis/library/sql-component.googleapis.com?project=cepf-l300-juananestival

9. terraform apply


## Create instance
1. edit the main of the module

2. edit main root
