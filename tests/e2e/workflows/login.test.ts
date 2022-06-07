import { NightwatchBrowser } from "nightwatch";
import { LoginPage } from "../types";
import buildTests from "../buildTests";

/**
 * Represents all tests to login pages.
 *
 * TODO: find a safe way of injecting login credentials.
 */
export default buildTests<LoginPage>("LoginPage", (getPage) => ({
  "I cant log in with invalid credentials"(browser: NightwatchBrowser) {
    const page = getPage(browser);

    page.waitForLoad();
    page.enterLogin("test@test.com", "123").checkLoginFailure();

    browser.end();
  },
  "I can log in"(browser: NightwatchBrowser) {
    const page = getPage(browser);

    page.waitForLoad();
    page.enterLogin("tjnewman111@gmail.com", "123").checkLoginSuccess();

    browser.end();
  },
  "I can log out"(browser: NightwatchBrowser) {
    const page = getPage(browser);

    page.authenticate();
    page.checkLogout();

    browser.end();
  },
}));
