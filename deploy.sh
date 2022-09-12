gcloud beta run deploy tgen-test --source . \
  --execution-environment gen2 \
  --allow-unauthenticated \
  --service-account fs-identity \
  --update-env-vars BUCKET=safa-tgen-models
