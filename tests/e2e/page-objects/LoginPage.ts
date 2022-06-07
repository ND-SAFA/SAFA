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
    profileImage: "#my-account",
  },
  commands: {
    loginSession(this: LoginPage, email: string, password: string): LoginPage {
      this.setInputText("Email", email).isButtonClickable(
        "Login",
        "Login: Login button is disabled without a valid password entered"
      );

      this.setInputText("Password", password).clickButton("Login");

      return this;
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
});
