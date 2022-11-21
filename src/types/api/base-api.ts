/**
 * Defines the options for interacting with API endpoints.
 */
export interface APIOptions {
  headers?: Record<string, string>;
  method: APIMethods;
  body?: string | FormData;
}

type APIMethods = "GET" | "POST" | "PUT" | "DELETE";

/**
 * Defines a error response from the API.
 */
export interface APIError {
  /**
   * The error status.
   */
  status: number;
  /**
   * The body of the error.
   */
  body: APIErrorBody;
}

/**
 * Defines an API error.
 */
export interface APIErrorBody {
  /**
   * The error details.
   */
  details: string;
  /**
   * The error message.
   */
  message: string;
  /**
   * A list of stack traces.
   */
  errors: string[];
}

/**
 * Defines the callbacks for an io handler function.
 */
export interface IOHandlerCallback<Res = void> {
  /**
   * Called on success with the response data.
   * @param res - The successful response data.
   */
  onSuccess?: (res: Res) => void;
  /**
   * Called on error with the error details.
   * @param err - The returned error.
   */
  onError?: (err: Error) => void;
  /**
   * Called regardless of whether the action succeeds or fails once complete.
   */
  onComplete?: () => void;
}

/**
 * Represents a url parameter in the app's web address.
 */
export type URLParameter = string | (string | null)[] | undefined;
