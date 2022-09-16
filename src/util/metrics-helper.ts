import { datadogRum } from "@datadog/browser-rum";

datadogRum.init({
  applicationId: "4470d612-52c0-4667-9b83-f7158df0c432",
  clientToken: "pubbd23f8a1ec0d66645eb858fe01bf45b6",
  site: "datadoghq.com",
  service: "safa",
  version: process.version,
  sampleRate: 100,
  premiumSampleRate: 100,
  trackInteractions: true,
  defaultPrivacyLevel: "mask-user-input",
});
