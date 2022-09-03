import { validUser } from "../fixtures";

const apiUrl = "https://dev-api.safa.ai";

Cypress.Commands.add("dbToken", () => {
  return cy.request<{ token: string }>("POST", `${apiUrl}/login`, validUser);
});

Cypress.Commands.add("dbResetJobs", () => {
  cy.dbToken().then((sessionRes) => {
    const token = sessionRes.body.token;

    cy.request<{ id: string }[]>({
      method: "GET",
      url: `${apiUrl}/jobs`,
      headers: { Authorization: token },
    }).then((jobJes) => {
      jobJes.body.forEach((job) => {
        cy.request({
          method: "DELETE",
          url: `${apiUrl}/jobs/${job.id}`,
          headers: { Authorization: token },
        });
      });
    });
  });
});

Cypress.Commands.add("dbResetProjects", () => {
  cy.dbToken().then((sessionRes) => {
    const token = sessionRes.body.token;

    cy.request<{ projectId: string }[]>({
      method: "GET",
      url: `${apiUrl}/projects`,
      headers: { Authorization: token },
    }).then((projectRes) => {
      projectRes.body.forEach((project) => {
        cy.request({
          method: "DELETE",
          url: `${apiUrl}/projects/${project.projectId}`,
          headers: { Authorization: token },
        });
      });
    });
  });
});

Cypress.Commands.add("dbResetDocuments", () => {
  cy.dbToken().then((sessionRes) => {
    const token = sessionRes.body.token;

    cy.request<{ projectId: string }[]>({
      method: "GET",
      url: `${apiUrl}/projects`,
      headers: { Authorization: token },
    }).then((projectRes) => {
      const project = projectRes.body[0];

      cy.request<{ versionId: string }>({
        method: "GET",
        url: `${apiUrl}/projects/${project.projectId}/versions/current`,
        headers: { Authorization: token },
      }).then((versionRes) => {
        cy.request<{ documents: { documentId: string }[] }>({
          method: "GET",
          url: `${apiUrl}/projects/versions/${versionRes.body.versionId}`,
          headers: { Authorization: token },
        }).then((docRes) => {
          docRes.body.documents.forEach(({ documentId }) => {
            cy.request({
              method: "DELETE",
              url: `${apiUrl}/projects/documents/${documentId}`,
              headers: { Authorization: token },
            });
          });
        });
      });
    });
  });
});
