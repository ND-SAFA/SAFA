import { BasePage, BasePageCommands, BasePageModel, PageModel } from "../types";
import { PageElements } from "nightwatch";

const basePage: BasePageModel = {
  url: "http://localhost:8080/",
  elements: {},
  commands: {
    setInputText(
      this: BasePage,
      inputLabel: string,
      inputValue: string
    ): BasePage {
      const inputWrapperSelector = `//label[contains(text(),'${inputLabel}')]`;
      const inputSelector = `${inputWrapperSelector}/following-sibling::*[1]`;

      return this.useXpath()
        .moveToElement(inputWrapperSelector, 0, 0)
        .setValue(inputSelector, inputValue);
    },
    clickButton(this: BasePage, buttonLabel: string): BasePage {
      const buttonSelector = `(//span[contains(text(),'${buttonLabel}')])[last()]`;

      return this.useXpath()
        .moveToElement(buttonSelector, 0, 0)
        .click(buttonSelector);
    },
    isButtonClickable(
      this: BasePage,
      buttonLabel: string,
      testLabel: string
    ): BasePage {
      const buttonSelector = `//*[contains(text(),'${buttonLabel}')]/parent::button`;

      this.useXpath()
        .expect.element(buttonSelector)
        .to.have.attribute("disabled", testLabel)
        .match(/true\b/);

      return this;
    },

    waitForLoad(this: BasePage): BasePage {
      this.navigate().useCss().waitForElementVisible("#login-view", 5000);

      return this;
    },
    // TODO: find a safe way of injecting login credentials.
    authenticate(this: BasePage): BasePage {
      this.waitForLoad()
        .setInputText("Email", "tjnewman111@gmail.com")
        .setInputText("Password", "123")
        .clickButton("Login")
        .useCss()
        .waitForElementVisible(".mdi-account-circle", 5000);

      return this;
    },
  },
};

/**
 * Builds a page model that extends the base page model.
 * @param page - The page to build
 */
export function buildPageModel<
  C,
  E extends PageElements,
  T extends PageModel<C, E>
>(page: PageModel<Omit<C, keyof BasePageCommands>, E>): T {
  return {
    ...page,
    elements: {
      ...basePage.elements,
      ...page.elements,
    },
    commands: {
      ...basePage.commands,
      ...page.commands,
    },
  } as unknown as T;
}

export default basePage;
