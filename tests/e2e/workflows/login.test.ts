import { NightwatchTests, NightwatchBrowser } from "nightwatch";
import { LoginPage } from "../page-objects";

const loginTests: NightwatchTests = {
  "I can log in"(browser: NightwatchBrowser) {
    const page: LoginPage = browser.page.LoginPage();

    page
      .navigate()
      .waitForElementVisible("@loginView", 1000)
      .assert.titleEquals("SAFA", "Login: Page has loaded");

    page
      .loginSession("test@test.com", "123")
      .waitForElementVisible(
        "@profileImage",
        1000,
        undefined,
        true,
        undefined,
        "Login: Successfully logged in"
      );

    browser.end();
  },
};

export default loginTests;
