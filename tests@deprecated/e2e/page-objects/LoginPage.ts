import {
  LoginPage,
  LoginPageCommands,
  LoginPageModel,
  LoginPageElements,
} from "../types";
import { buildPageModel } from "./BasePage";

export default buildPageModel<
  LoginPageCommands,
  LoginPageElements,
  LoginPageModel
>({
  url: "http://localhost:8080/",
  elements: {
    loginView: "#login-view",
    loginError: ".v-messages__message",
    accountDropdown: "#account-dropdown",
  },
  commands: {
    enterLogin(this: LoginPage, email: string, password: string): LoginPage {
      this.setInputText("Email", email).isButtonClickable(
        "Login",
        "Login: Login button is disabled without a valid password entered"
      );

      this.setInputText("Password", password).clickButton("Login");

      return this;
    },
    checkLoginSuccess(this: LoginPage): LoginPage {
      this.useCss().waitForElementVisible(
        "@accountDropdown",
        5000,
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
    checkLogout(this: LoginPage): LoginPage {
      this.click("@accountDropdown")
        .clickButton("Logout")
        .useCss()
        .waitForElementVisible(
          "@loginView",
          5000,
          undefined,
          true,
          undefined,
          "Login: The user is successfully logged out"
        );

      return this;
    },
  },
});
