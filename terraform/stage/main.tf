provider "heroku" {
  # Credentials provided by `heroku login`
}

terraform {
  backend "s3" {
    bucket         = "spare-terraform"
    key            = "spare-stage.tfstate"
    region         = "us-west-2"
    dynamodb_table = "spare-terraform"
    profile        = "spare-terraform"
  }
}

resource "heroku_app" "default" {
  name   = "${var.name}-test"
  region = "us"
  stack  = "container"

  config_vars = {
    SECRET_KEY             = "${var.secret_key}"
    DJANGO_SETTINGS_MODULE = "spare.settings.prod"
  }
}

resource "heroku_addon" "postgresql" {
  app  = "${heroku_app.default.name}"
  plan = "heroku-postgresql:hobby-dev"
}

resource "heroku_addon" "papertrail" {
  app  = "${heroku_app.default.name}"
  plan = "papertrail:choklad"
}
