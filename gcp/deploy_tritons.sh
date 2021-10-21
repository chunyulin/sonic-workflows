
CONF_T4="--project=harrisgroup-223921 --zone=us-central1-f \
  --machine-type=n1-standard-8 --network-interface=network-tier=PREMIUM,subnet=default --maintenance-policy=TERMINATE \
  --service-account=60153087361-compute@developer.gserviceaccount.com \
  --scopes=https://www.googleapis.com/auth/devstorage.read_only,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/trace.append \
  --accelerator=count=1,type=nvidia-tesla-t4  --tags=http-server,triton-server \
  --no-shielded-secure-boot --shielded-vtpm --shielded-integrity-monitoring --reservation-affinity=any \
  --metadata-from-file=ssh-keys=/home/lincy/.ssh/google_compute_engine.pub"

CONF_DISK="auto-delete=yes,boot=yes,image=projects/ml-images/global/images/c1-deeplearning-tf-2-3-cu110-v20211011-debian-10,mode=rw,size=50,type=projects/harrisgroup-223921/zones/us-central1-f/diskTypes/pd-balanced"


TRITONS="dm1 dm2 dtau ak4 ak8 ak8md ak8mr"

for mo in ${TRITONS}; do
  TAG=lincy-${mo}
  echo "Creating ${TAG} ..."

  gcloud compute instances create ${TAG} ${CONF_T4} \
     --create-disk=device-name=${TAG},${CONF_DISK}        \
     --metadata-from-file=startup-script="startup-${mo}.sh"
done

