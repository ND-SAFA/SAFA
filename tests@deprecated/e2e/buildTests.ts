import {
  NightwatchTests,
  NightwatchBrowser,
  EnhancedPageObject,
} from "nightwatch";

/**
 * Builds nightwatch tests for a specific page.
 *
 * @param pageName - The file name of the corresponding page object.
 * @param tests - A callback to create the tests.
 * @return The created nightwatch tests.
 */
export default function buildTests<T extends EnhancedPageObject>(
  pageName: "LoginPage" | string,
  tests: (getPage: (browser: NightwatchBrowser) => T) => NightwatchTests
): NightwatchTests {
  return tests((browser) => browser.page[pageName]() as T);
}
