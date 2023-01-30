import { validUser } from "../fixtures";

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
  return cy.request<{ token: string }>("POST", `${apiUrl}/login`, validUser);
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
    .clearCookies();
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
    .clearCookies();
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
    .clearCookies();
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
            url: `${apiUrl}/projects/${projectId}/versions/minor`,
          });
        });
      });
    })
    .clearCookies();
});

// TODO: Fix this command with the correct API endpoint.
Cypress.Commands.add("dbDeleteUser", (email) => {
  cy.dbToken().then(() => {
    cy.request<{ id: string; username: string; password: string }[]>({
      method: "GET",
      url: `${apiUrl}/users`,
    }).then(({ body: users }) => {
      const user = users.find((user) => user.username === email);
      if (!user) {
        throw new Error(`User ${validUser.username} not found`);
      }
      cy.request({
        method: "DELETE",
        url: `${apiUrl}/users/${user.id}`,
      });
    });
  });
});
// Cypress.Commands.add("dbDeleteUser", (username: string, password: string) => {
//   cy.dbToken()
//     .then(() => {
//       cy.request<{ id: string; username: string; password: string }[]>({
//         method: "GET",
//         url: ${apiUrl}/users,
//       }).then(({ body: users }) => {
//         const user = users.find(
//           (user) => user.username === username && user.password === password
//         );
//         if (!user) {
//           throw new Error(User ${username} not found);
//         }
//         cy.request({
//           method: "DELETE",
//           url: ${apiUrl}/users/${user.id},
//         });
//       });
//     })
//     .clearCookies();
// });
