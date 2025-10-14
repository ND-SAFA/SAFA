import { defineConfig } from "cypress";

export default defineConfig({
  projectId: "5kk96a",
  chromeWebSecurity: false,
  e2e: {
    numTestsKeptInMemory: 0,
    video: false,
    baseUrl: "https://localhost.safa.ai:8080",
    experimentalInteractiveRunEvents: true,
    env: {
      // Get with `cy.env("key")`
      validUser: {
        email: `test-${Math.random()}@test.com`,
        password: "123",
      },
      invalidUser: {
        email: `test-invalid-${Math.random()}@test.com`,
        password: "super-invalid-password",
      },
      editUser: {
        email: `test-edit-${Math.random()}@test.com`,
        password: "123",
        newPassword: "newPassword",
      },
      createUser: {
        email: `test-create-${Math.random()}@test.com`,
        password: "123",
      },
      deleteUser: {
        email: `test-delete-${Math.random()}@test.com`,
        password: "123",
      },
      inviteUser: {
        email: `test-invite-${Math.random()}@test.com`,
        invalidEmail: `test-invite-${Math.random()}@test.com`,
        password: "123",
      },
    },
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
