import { defineConfig } from "cypress";

export default defineConfig({
  projectId: "5kk96a",
  videoUploadOnPasses: false,
  e2e: {
    baseUrl: "http://localhost:8080",
  },
});
