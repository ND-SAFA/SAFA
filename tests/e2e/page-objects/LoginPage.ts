import { PageObjectModel } from "nightwatch";
import { LoginPage } from "../types";

const loginPage: PageObjectModel = {
  url: "http://localhost:8081/",
  elements: {
    loginView: "#login-view",
    loginError: ".v-messages__message",
    profileImage: "#my-account",
  },
  commands: {
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
    clickButton(this: LoginPage, buttonLabel: string): LoginPage {
      const buttonSelector = `(//span[contains(text(),'${buttonLabel}')])[last()]`;

      return this.useXpath()
        .moveToElement(buttonSelector, 0, 0)
        .click(buttonSelector);
    },
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

      return this.setInputText("Password", password).clickButton("Login");
    },
    checkLoginSuccess(this: LoginPage): LoginPage {
      this.waitForElementVisible(
        "@profileImage",
        2000,
        undefined,
        true,
        undefined,
        "Login: The user is successfully logged in"
      );

      return this;
    },
    checkLoginFailure(this: LoginPage): LoginPage {
      this.useCss()
        .expect.element("@loginError")
        .text.to.contain("Invalid username or password");

      return this;
    },
  },
};

export default loginPage;
