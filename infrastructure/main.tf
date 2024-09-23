resource "aws_kms_key" "kms_key" {
  description             = "kms_key"
  deletion_window_in_days = 30
}

resource "aws_cloudwatch_log_group" "cloudwatch_log_group" {
  name = "cloudwatch_log_group"
}

resource "aws_ecs_cluster" "ecs_cluster" {
  name = "ecs_cluster"

  configuration {
    execute_command_configuration {
      kms_key_id = aws_kms_key.kms_key.arn
      logging    = "OVERRIDE"

      log_configuration {
        cloud_watch_encryption_enabled = true
        cloud_watch_log_group_name     = aws_cloudwatch_log_group.cloudwatch_log_group.name
      }
    }
  }
}