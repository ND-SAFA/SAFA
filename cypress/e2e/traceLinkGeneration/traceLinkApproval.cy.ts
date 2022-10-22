import { DataCy } from "../../fixtures";

describe("Trace Link Approval", () => {
  //TODO: Figure out how to test this and structure the test
  // Folow the same before and before each as each other project

  before(() => {
    cy.dbResetJobs().dbResetProjects().loadNewProject();
  });

  beforeEach(() => {
    cy.loadCurrentProject().openApproveGeneratedTraceLinks();
  });

  describe("I can approve an un-reviewed or declined trace link", () => {
    it("Can decline a trace link and check that it is declined", () => {});

    it("Can approve an un-reviewed trace link and check that it is approved", () => {});

    it("Can approve a declined trace link and check that it is approved", () => {});
  });

  describe("I can decline an un-reviewed or approved trace link", () => {
    it("Can approve a trace link and check that it is approved", () => {});

    it("Can decline an un-reviewed trace link and check that it is declined", () => {});

    it("Can decline an approved trace link and check that it is declined", () => {});
  });

  /* These will be skipped for now
  //TODO: Figure out how to test for trace links on the actual graph
  describe("I cannot see declined trace links on the graph", () => {});
  describe("I can see un-reviewed trace links as dotted lines", () => {});
  */
  describe("I can un-review an approved or declined trace link", () => {
    it("Can un-review an approved trace link", () => {});

    it("Can un-review a declined trace link", () => {});
  });

  describe("I can sort trace links by name, type, and approval status", () => {
    it("Can sort by name", () => {});

    it("Can sort by type", () => {});

    it("Can sort by approval status", () => {});
  });

  describe("I can group trace links by name, type, and approval status", () => {
    it("Can group by name", () => {});

    it("Can group by type", () => {});

    it("Can group by approval status", () => {});
  });

  describe("I can see the counts of grouped trace links", () => {
    it("Can see the counts of grouped trace links", () => {});
  });
});
