
Build Docker Image - docker buildx build --platform linux/amd64,linux/arm64 -t gcr.io/elegant-tangent-422918-m1/fastapi-app --push .
Deploy to GCP - gcloud run deploy fastapi-app --image gcr.io/elegant-tangent-422918-m1/fastapi-app --platform managed --region us-central1
