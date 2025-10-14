const apiUrl = "https://dev-api.safa.ai";

Cypress.on("window:before:load", (window) => {
  // Disable the cookie banner.
  window.document.cookie = `wpcc=dismiss`;
  window.localStorage.setItem("onboarding", "true");
});

Cypress.Commands.add(
  "chainRequest",
  {
    prevSubject: true,
  },
  (subject: Cypress.Response<unknown>, cb) => {
    return cy.request(cb(subject));
  }
);

Cypress.Commands.add("dbToken", () => {
  const validUser = Cypress.env("validUser");

  cy.request("POST", `${apiUrl}/login`, validUser);
});

Cypress.Commands.add("dbResetJobs", () => {
  cy.dbToken()
    .then(() => {
      cy.request<{ id: string }[]>({
        method: "GET",
        url: `${apiUrl}/jobs/user`,
      }).then(({ body: jobs }) =>
        jobs.forEach((job) =>
          cy.request({
            method: "DELETE",
            url: `${apiUrl}/jobs/${job.id}`,
          })
        )
      );
    })
    .clearAllCookies();
});

Cypress.Commands.add("dbResetProjects", () => {
  cy.dbToken()
    .then(() => {
      cy.request<{ projectId: string }[]>({
        method: "GET",
        url: `${apiUrl}/projects`,
      }).then(({ body: projects }) =>
        projects.forEach(({ projectId }) =>
          cy.request({
            method: "DELETE",
            url: `${apiUrl}/projects/${projectId}`,
          })
        )
      );
    })
    .clearAllCookies();
});

Cypress.Commands.add("dbResetDocuments", () => {
  cy.dbToken()
    .then(() => {
      cy.request<{ projectId: string }[]>({
        method: "GET",
        url: `${apiUrl}/projects`,
      })
        .chainRequest<{ versionId: string }>(({ body: projects }) => ({
          method: "GET",
          url: `${apiUrl}/projects/${projects[0].projectId}/versions/current`,
        }))
        .chainRequest<{ documents: { documentId: string }[] }>(
          ({ body: { versionId } }) => ({
            method: "GET",
            url: `${apiUrl}/projects/versions/${versionId}`,
          })
        )
        .then(({ body: { documents } }) =>
          documents.forEach(({ documentId }) =>
            cy.request({
              method: "DELETE",
              url: `${apiUrl}/projects/documents/${documentId}`,
            })
          )
        );
    })
    .clearAllCookies();
});

Cypress.Commands.add("dbResetVersions", () => {
  cy.dbToken()
    .then(() => {
      cy.request<{ projectId: string }[]>({
        method: "GET",
        url: `${apiUrl}/projects`,
      }).then(({ body: projects }) => {
        const projectId = projects[0].projectId;
        cy.request<{ versionId: string }[]>({
          method: "GET",
          url: `${apiUrl}/projects/${projectId}/versions`,
        }).then(({ body: versions }) => {
          versions.slice(0, -1).forEach(({ versionId }) =>
            cy.request({
              method: "DELETE",
              url: `${apiUrl}/projects/versions/${versionId}`,
            })
          );
          cy.request({
            method: "POST",
            url: `${apiUrl}/projects/${projectId}/versions/revision`,
          });
        });
      });
    })
    .clearAllCookies();
});

Cypress.Commands.add("dbDeleteUser", (email, password) => {
  cy.request({
    method: "POST",
    url: `${apiUrl}/login`,
    failOnStatusCode: false,
    body: { email, password },
  }).then(() => {
    cy.request({
      method: "POST",
      url: `${apiUrl}/accounts/delete`,
      body: { password },
      failOnStatusCode: false,
    });
  });
});

Cypress.Commands.add("dbGenerateUsers", () => {
  const { validUser, editUser, deleteUser, inviteUser } = Cypress.env();

  for (const user of [validUser, editUser, deleteUser, inviteUser]) {
    cy.request<{ token: string }>({
      failOnStatusCode: false,
      method: "POST",
      // TODO: update to `${apiUrl}/accounts/create-verified` once the API is updated.
      url: `${apiUrl}/accounts/create`,
      body: { email: user.email, password: user.password },
    });
  }
});

Cypress.Commands.add("dbDeleteGeneratedUsers", () => {
  const { validUser, editUser, deleteUser, inviteUser } = Cypress.env();

  for (const user of [validUser, editUser, deleteUser, inviteUser]) {
    cy.dbDeleteUser(user.email, user.password);
  }
});
