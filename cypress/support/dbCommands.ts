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

Cypress.Commands.add(
  "requestAll",
  {
    prevSubject: true,
  },
  (subject: Cypress.Response<any>, cb) => {
    cb(subject).forEach((restOptions) => cy.request(restOptions));
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
    }).requestAll(({ body: jobs }) =>
      jobs.map((job) => ({
        method: "DELETE",
        url: `${apiUrl}/jobs/${job.id}`,
        headers,
      }))
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
    }).requestAll(({ body: projects }) =>
      projects.map(({ projectId }) => ({
        method: "DELETE",
        url: `${apiUrl}/projects/${projectId}`,
        headers,
      }))
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
      .requestAll(({ body: { documents } }) =>
        documents.map(({ documentId }) => ({
          method: "DELETE",
          url: `${apiUrl}/projects/documents/${documentId}`,
          headers,
        }))
      );
  });
});
