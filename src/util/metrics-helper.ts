import { datadogRum } from "@datadog/browser-rum";

datadogRum.init({
  applicationId: process.env.VUE_APP_DDOG_APP_ID || "",
  clientToken: process.env.VUE_APP_DDOG_DDOG_TOKEN || "",
  site: "datadoghq.com",
  service: "safa",
  version: "1.0.0",
  sampleRate: 100,
  premiumSampleRate: 100,
  trackInteractions: true,
  defaultPrivacyLevel: "mask-user-input",
});
