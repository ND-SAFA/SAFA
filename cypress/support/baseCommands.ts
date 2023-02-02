import "cypress-file-upload";
import { DataCy } from "@/fixtures";

Cypress.Commands.add("expandViewport", (size) => {
  if (size === "l") {
    cy.viewport(1024 * 2, 768 * 2);
  } else {
    cy.viewport(1024, 768);
  }
});

Cypress.Commands.add("getCy", (dataCy, elementPosition, timeout) => {
  const elements = cy.get(`[data-cy="${dataCy}"]`, { timeout });

  if (elementPosition === "first") {
    return elements.first({ timeout });
  } else if (elementPosition === "last") {
    return elements.last({ timeout });
  } else {
    return elements;
  }
});

Cypress.Commands.add("doesExist", (dataCy) => {
  return cy.get("body").then((body) => {
    return body.find(`[data-cy="${dataCy}"]`).length > 0;
  });
});

Cypress.Commands.add("inputText", (dataCy, inputValue, clear) => {
  if (clear) {
    cy.getCy(dataCy).clear();
  }

  if (inputValue.length > 0) {
    cy.getCy(dataCy).type(inputValue);
  }
});

Cypress.Commands.add(
  "clickButton",
  (dataCy, elementPosition = "first", force = false) => {
    cy.getCy(dataCy, elementPosition).click({ force });
  }
);

Cypress.Commands.add("clickButtonWithName", (name) => {
  cy.contains(name, { matchCase: false }).last().click();
});

Cypress.Commands.add("clickSelectOption", (dataCy, optionName) => {
  cy.getCy(dataCy).parent().click();
  cy.get(".v-menu__content")
    .filter(":visible")
    .contains(optionName, { matchCase: false })
    .click();
  cy.get(".v-menu__content").should("not.be.visible");
});

Cypress.Commands.add("clickMenuOption", (optionName) => {
  cy.get(`[role="menu"]`)
    .contains(optionName, { matchCase: false })
    .first()
    .click();
});

Cypress.Commands.add("uploadFiles", (dataCy, ...filePaths) => {
  cy.getCy(dataCy, "last").attachFile(filePaths);
});

Cypress.Commands.add("switchTab", (tabLabel) => {
  cy.contains("div", tabLabel).click();
});

Cypress.Commands.add("closeModal", (dataCy) => {
  cy.getCy(dataCy).within(() => cy.clickButton(DataCy.modalCloseButton));
});

Cypress.Commands.add("withinTableRows", (dataCy, fn, waitForLoad = true) => {
  cy.getCy(dataCy)
    .should("be.visible")
    .within(() => {
      if (waitForLoad) {
        cy.get(".v-data-table__progress").should("not.exist");
      }

      fn(cy.get("tr"));
    });
});
