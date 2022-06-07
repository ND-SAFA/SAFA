import { NightwatchBrowser } from "nightwatch";
import { LoginPage } from "../types";
import buildTests from "../buildTests";

export default buildTests<LoginPage>("LoginPage", (getPage) => ({
  "I cant log in with invalid credentials"(browser: NightwatchBrowser) {
    const page = getPage(browser);

    page
      .navigate()
      .waitForElementVisible("@loginView", 10000)
      .assert.titleEquals("SAFA", "Login: Page has loaded");

    page.loginSession("test@test.com", "123").checkLoginFailure();

    browser.end();
  },
}));
