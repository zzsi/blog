project=your-gcp-project-id
app=example-app
platform=linux/amd64
region=us-central1
docker build --platform $platform -t example-app-image .

image=us.gcr.io/$project/$app:latest
docker tag example-app-image $image
docker push $image
gcloud run deploy $app --image $image --cpu 1 --memory 1Gi --min-instances 1 --region $region --allow-unauthenticated
