import { defineConfig } from "cypress";

export default defineConfig({
  projectId: "5kk96a",
  videoUploadOnPasses: false,
  chromeWebSecurity: false,
  e2e: {
    baseUrl: "https://localhost.safa.ai:8080",
  },
  clientCertificates: [
    {
      url: "https://localhost.safa.ai/",
      ca: ["certs/localhost.safa.ai.pem"],
      certs: [
        {
          key: "certs/localhost.safa.ai-key.pem",
          cert: "certs/localhost.safa.ai.pem",
        },
      ],
    },
  ],
});
