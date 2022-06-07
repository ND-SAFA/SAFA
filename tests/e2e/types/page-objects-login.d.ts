import { EnhancedPageObject, PageElements } from "nightwatch";
import { BasePageCommands, PageModel } from "./page-objects";

/**
 * Represents the commands on the login page object.
 */
export interface LoginPageCommands extends BasePageCommands {
  /**
   * Logs in to a session.
   *
   * @param email - The email to use.
   * @param password - The password to use.
   */
  loginSession(email: string, password: string): LoginPage;
  /**
   * Checks that the login succeeded.
   */
  checkLoginSuccess(): LoginPage;
  /**
   * Checks that the login failed.
   */
  checkLoginFailure(): LoginPage;
}

/**
 * Represents the elements on the login page object.
 */
export interface LoginPageElements extends PageElements {
  /**
   * Selector for the login window.
   */
  loginView: string;
  /**
   * Selector for the login error message.
   */
  loginError: string;
  /**
   * Selector for the profile image once logged in.
   */
  profileImage: string;
}

/**
 * Represents the login page model.
 */
export type LoginPageModel = PageModel<LoginPageCommands, LoginPageElements>;

/**
 * Represents the login page object.
 */
export type LoginPage = EnhancedPageObject<
  LoginPageCommands,
  LoginPageElements
>;
