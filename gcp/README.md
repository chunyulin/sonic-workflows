# Note

Script to deploy Triton servers  on GCP VMs.

1) Prepare model repository on the S3 bucket via `gsutil` command.
2) Run `prepare_startup_script.sh` to generate startup script for each VM.
3) Run `deploy_tritons.sh` to deply multiple Triton. (It will take ~minutes to complete all the tasks including installation of NVIDIA driver and initialization of Triton container.)

--
