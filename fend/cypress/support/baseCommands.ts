import "cypress-file-upload";

Cypress.Commands.add("expandViewport", (size) => {
  if (size === "l") {
    cy.viewport(1024 * 1.5, 768 * 1.2);
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

Cypress.Commands.add("inputText", (dataCy, inputValue, clear, last) => {
  const el = last
    ? cy.getCy(dataCy, "last")
    : cy.getCy(dataCy).filter(":visible");

  if (clear) {
    el.clear();
  }

  if (inputValue.length === 0) return;

  el.type(inputValue);
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
  cy.get(`[role="listbox"]`)
    .contains(optionName, { matchCase: false })
    .first()
    .click();
});

Cypress.Commands.add("uploadFiles", (dataCy, ...filePaths) => {
  cy.getCy(dataCy, "last").attachFile(filePaths);
});

Cypress.Commands.add("switchTab", (tabLabel) => {
  cy.get(".q-tabs").within(() => {
    cy.contains("div", tabLabel).click();
  });
});

Cypress.Commands.add("withinTableRows", (dataCy, fn, waitForLoad = true) => {
  cy.getCy(dataCy)
    .should("be.visible")
    .within(() => {
      if (waitForLoad) {
        cy.get(".q-linear-progress__model").should("not.exist");
      }

      fn(cy.get("tr"));
    });
});
