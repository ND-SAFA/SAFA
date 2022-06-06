import { PageObjectModel, EnhancedPageObject } from "nightwatch";

export type LoginPage = EnhancedPageObject<
  {
    setInputText(inputLabel: string, inputValue: string): LoginPage;
    clickButton(buttonLabel: string): LoginPage;
    isButtonClickable(buttonLabel: string, testLabel: string): LoginPage;
    loginSession(email: string, password: string): LoginPage;
  },
  {
    loginView: string;
    profileImage: string;
  }
>;

const loginPage: PageObjectModel = {
  url: "http://localhost:8080/",
  elements: {
    loginView: "#login-view",
    profileImage: "#my-account",
  },
  commands: {
    /**
     * Sets the value of an input field.
     *
     * @param inputLabel - The label of the input being set.
     * @param inputValue - The value to set.
     */
    setInputText(
      this: LoginPage,
      inputLabel: string,
      inputValue: string
    ): LoginPage {
      const inputWrapperSelector = `//label[contains(text(),'${inputLabel}')]`;
      const inputSelector = `${inputWrapperSelector}/following-sibling::*[1]`;

      return this.useXpath()
        .moveToElement(inputWrapperSelector, 0, 0)
        .setValue(inputSelector, inputValue);
    },
    /**
     * Clicks a button.
     *
     * @param buttonLabel - The label of the button to click.
     */
    clickButton(this: LoginPage, buttonLabel: string): LoginPage {
      const buttonSelector = `(//span[contains(text(),'${buttonLabel}')])[last()]`;

      return this.useXpath()
        .moveToElement(buttonSelector, 0, 0)
        .click(buttonSelector);
    },
    /**
     * Checks if a button can be clicked
     *
     * @param buttonLabel - The label of the button to check.
     * @param testLabel - The label of the test checking whether the button is clickable.
     */
    isButtonClickable(
      this: LoginPage,
      buttonLabel: string,
      testLabel: string
    ): LoginPage {
      const buttonSelector = `//*[contains(text(),'${buttonLabel}')]/parent::button`;

      this.useXpath()
        .expect.element(buttonSelector)
        .to.have.attribute("disabled", testLabel)
        .match(/true\b/);

      return this;
    },
    /**
     * Logs in to a session.
     *
     * @param email - The email to use.
     * @param password - The password to use.
     */
    loginSession(this: LoginPage, email: string, password: string): LoginPage {
      this.setInputText("Email", email).isButtonClickable(
        "Login",
        "Login: Login button is disabled without a valid password entered"
      );

      return this.setInputText("Password", password)
        .clickButton("Login")
        .waitForElementVisible(
          "@profileImage",
          2000,
          undefined,
          true,
          undefined,
          "Login: The user is successfully logged in"
        );
    },
  },
};

export default loginPage;
