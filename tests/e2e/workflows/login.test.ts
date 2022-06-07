import { NightwatchTests, NightwatchBrowser } from "nightwatch";
import { LoginPage } from "../types";

const loginTests: NightwatchTests = {
  "I cant log in with invalid credentials"(browser: NightwatchBrowser) {
    const page: LoginPage = browser.page.LoginPage();

    page
      .navigate()
      .waitForElementVisible("@loginView", 10000)
      .assert.titleEquals("SAFA", "Login: Page has loaded");

    page.loginSession("test@test.com", "123").checkLoginFailure();

    browser.end();
  },
};

export default loginTests;
