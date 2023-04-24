import { user } from "@/fixtures/data/user";

const apiUrl = "https://dev-api.safa.ai";

Cypress.on("window:before:load", (window) => {
  // Disable the cookie banner.
  window.document.cookie = `wpcc=dismiss`;
});

Cypress.Commands.add(
  "chainRequest",
  {
    prevSubject: true,
  },
  (subject: Cypress.Response<any>, cb) => {
    return cy.request(cb(subject));
  }
);

Cypress.Commands.add("dbToken", () => {
  cy.request<{ token: string }>("POST", `${apiUrl}/login`, user.validUser);
});

Cypress.Commands.add("dbResetJobs", () => {
  cy.dbToken()
    .then(() => {
      cy.request<{ id: string }[]>({
        method: "GET",
        url: `${apiUrl}/jobs`,
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
  cy.request<{ token: string }>({
    method: "POST",
    url: `${apiUrl}/login`,
    body: { email, password },
    failOnStatusCode: false,
  }).then(() => {
    cy.request<{ token: string }>({
      method: "POST",
      url: `${apiUrl}/accounts/delete`,
      body: { password },
      failOnStatusCode: false,
    });
  });
});

Cypress.Commands.add("generateUsers", () => {
  // Create the account for validUser and editUser
  cy.request<{ token: string }>({
    method: "POST",
    url: `${apiUrl}/user`,
    body: user.validUser,
  }).request<{ token: string }>({
    method: "POST",
    url: `${apiUrl}/user`,
    body: user.editUser,
  });
});

Cypress.Commands.add("deleteGeneratedUsers", () => {
  // Delete the account for all the users in the user object
  cy.request<{ token: string }>({
    method: "DELETE",
    url: `${apiUrl}/user/${user.validUser.email}`,
  }).request<{ token: string }>({
    method: "DELETE",
    url: `${apiUrl}/user/${user.editUser.email}`,
  });
});
