# Cloud Function to do the text summarization using Google Cloud Vertex AI

This application demonstrates a Cloud Function written in Python that initializes the Vertex AI module and then provides an endpoint to invoke PaLM 2 Text Bison model for text summarization.

> NOTE:
> 1. Before you move forward, ensure that you have Signed-in to the [Google Cloud Console](http://console.cloud.google.com/) and created a new project. You can reuse the existing project as well. You need to [create an account](https://accounts.google.com/SignUp) if you don't already have one for Gmail.
> 2. To use Cloud resources/APIs, you must [enable billing](https://medium.com/r/?url=https%3A%2F%2Fconsole.cloud.google.com%2Fbilling) in the Cloud Console. Users who are new to Google Cloud are eligible for the $300 USD Free Trial offer.

## Environment variables required

Your Cloud Function requires access to two environment variables:

- `GCP_PROJECT` : This is your project Project ID.
- `GCP_REGION` : This is the region where your Cloud Function will be deployed. For e.g., asia-south1.

These variables are required for the Vertex AI initialization. The specific code line from the `main.py` function is shown here:
`vertexai.init(project=PROJECT_ID)`

In Cloud Shell, execute the following commands:
```bash
export GCP_PROJECT='<Your GCP Project Id>'  # Change this
export GCP_REGION='asia-south1'             # If you change this, make sure region is supported by Model Garden. When in doubt, keep this.
```

These variables can be set via the following [instructions](https://cloud.google.com/functions/docs/configuring/env-var) via any of the following ways:

1. At the time of [deploying](https://cloud.google.com/functions/docs/configuring/env-var#setting_runtime_environment_variables) the Google Cloud Function. We will be using this method in the next section when we deploy the Cloud Function.
2. [Updating](https://cloud.google.com/functions/docs/configuring/env-var#updating_runtime_environment_variables) the environment variables after deploying the Google Cloud Function.

## Deploying the Cloud Function

Assuming that you have a copy of this project on your local machine with `gcloud` SDK setup on the machine, follow these steps:

1. Go to the root folder of this project.
2. You should have both the `main.py` and `requirements.txt` file present in this folder.
3. Provide the following command:

   ```bash
   gcloud functions deploy text-summarizer-function \
   --gen2 \
   --runtime=python311 \
   --region=$GCP_REGION \
   --source=. \
   --entry-point=text_summarizer \
   --set-env-vars=GCP_PROJECT=$GCP_PROJECT,GCP_REGION=$GCP_REGION \
   --trigger-http \
   --allow-unauthenticated \
   --max-instances=30
   ```

## Invoking the Cloud Function

You can call this Cloud Function directly because it is deployed with an HTTP trigger. Sample calls are shown below:

```bash
curl -m 70 -X POST https://$GCP_REGION-$GCP_PROJECT.cloudfunctions.net/text-summarizer-function \
-H "Content-Type: application/json" \
-d '{
  "inputText": "Google was founded on September 4, 1998, by American computer scientists Larry Page and Sergey Brin while they were PhD students at Stanford University in California. Together they own about 14% of its publicly listed shares and control 56% of its stockholder voting power through super-voting stock. The company went public via an initial public offering (IPO) in 2004. In 2015, Google was reorganized as a wholly owned subsidiary of Alphabet Inc. Google is Alphabet'\''s largest subsidiary and is a holding company for Alphabet'\''s internet properties and interests. Sundar Pichai was appointed CEO of Google on October 24, 2015, replacing Larry Page, who became the CEO of Alphabet. On December 3, 2019, Pichai also became the CEO of Alphabet. The company has since rapidly grown to offer a multitude of products and services beyond Google Search, many of which hold dominant market positions. These products address a wide range of use cases, including email (Gmail), navigation (Waze & Maps), cloud computing (Cloud), web browsing (Chrome), video sharing (YouTube), productivity (Workspace), operating systems (Android), cloud storage (Drive), language translation (Translate), photo storage (Photos), video calling (Meet), smart home (Nest), smartphones (Pixel), wearable technology (Pixel Watch & Fitbit), music streaming (YouTube Music), video on demand (YouTube TV), artificial intelligence (Google Assistant & Bard), and machine learning APIs (TensorFlow). Discontinued Google products include gaming (Stadia), Glass, Google+, Reader, Play Music, Nexus, Hangouts, and Inbox by Gmail."
}'
```
