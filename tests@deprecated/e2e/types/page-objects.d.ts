import { EnhancedPageObject, PageElements, PageObjectModel } from "nightwatch";

/**
 * Represents a generic page model.
 */
export interface PageModel<Commands, Elements extends PageElements>
  extends PageObjectModel {
  commands: Commands;
  elements: Elements;
}

/**
 * Represents the commands on the base page object.
 */
interface BasePageCommands {
  /**
   * Sets the value of an input field.
   *
   * @param inputLabel - The label of the input being set.
   * @param inputValue - The value to set.
   */
  setInputText(inputLabel: string, inputValue: string): BasePage;
  /**
   * Clicks a button.
   *
   * @param buttonLabel - The label of the button to click.
   */
  clickButton(buttonLabel: string): BasePage;
  /**
   * Checks if a button can be clicked.
   *
   * @param buttonLabel - The label of the button to check.
   * @param testLabel - The label of the test checking whether the button is clickable.
   */
  isButtonClickable(buttonLabel: string, testLabel: string): BasePage;

  /**
   * Waits for the login page to load.
   */
  waitForLoad(): BasePage;
  /**
   * Starts the app by waiting for load and logging in.
   */
  authenticate(): BasePage;
}

/**
 * Represents the base page model.
 */
export type BasePageModel = PageModel<BasePageCommands, Record<string, string>>;

/**
 * Represents the base page object.
 */
export type BasePage = EnhancedPageObject<
  BasePageCommands,
  Record<string, string>
>;
