import { validUser } from "../fixtures";

const apiUrl = "https://dev-api.safa.ai";

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
  cy.dbToken().then(({ body: { token } }) => {
    const headers = { Authorization: token };

    cy.request<{ id: string }[]>({
      method: "GET",
      url: `${apiUrl}/jobs`,
      headers,
    }).then(({ body: jobs }) =>
      jobs.forEach((job) =>
        cy.request({
          method: "DELETE",
          url: `${apiUrl}/jobs/${job.id}`,
          headers,
        })
      )
    );
  });
});

Cypress.Commands.add("dbResetProjects", () => {
  cy.dbToken().then(({ body: { token } }) => {
    const headers = { Authorization: token };

    cy.request<{ projectId: string }[]>({
      method: "GET",
      url: `${apiUrl}/projects`,
      headers,
    }).then(({ body: projects }) =>
      projects.forEach(({ projectId }) =>
        cy.request({
          method: "DELETE",
          url: `${apiUrl}/projects/${projectId}`,
          headers,
        })
      )
    );
  });
});

Cypress.Commands.add("dbResetDocuments", () => {
  cy.dbToken().then(({ body: { token } }) => {
    const headers = { Authorization: token };

    cy.request<{ projectId: string }[]>({
      method: "GET",
      url: `${apiUrl}/projects`,
      headers,
    })
      .chainRequest<{ versionId: string }>(({ body: projects }) => ({
        method: "GET",
        url: `${apiUrl}/projects/${projects[0].projectId}/versions/current`,
        headers,
      }))
      .chainRequest<{ documents: { documentId: string }[] }>(
        ({ body: { versionId } }) => ({
          method: "GET",
          url: `${apiUrl}/projects/versions/${versionId}`,
          headers,
        })
      )
      .then(({ body: { documents } }) =>
        documents.map(({ documentId }) => ({
          method: "DELETE",
          url: `${apiUrl}/projects/documents/${documentId}`,
          headers,
        }))
      );
  });
});
