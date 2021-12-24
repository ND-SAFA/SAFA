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
 * Defines a response from the API.
 */
export interface APIResponse<T> {
  status: number;
  body: T;
}

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
