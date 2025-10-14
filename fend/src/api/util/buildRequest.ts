import { APIMethods } from "@/types";
import { LOGOUT_ERROR, LOGOUT_STATUS_CODE } from "@/util";
import { BASE_URL, Endpoint } from "@/api";

/**
 * Builds a request to the SAFA API.
 */
class RequestBuilder<
  ReturnType = void,
  QueryParam extends string = string,
  BodyType = void,
> {
  /**
   * The relative URL of the request.
   * @private
   */
  private readonly relativeUrl: string;
  /**
   * Any path variables to fill into the request URL.
   */
  private readonly pathVariables: Record<string, string>;
  /**
   * Any query variables to fill into the request URL query.
   */
  private readonly queryVariables: Record<string, string>;
  /**
   * Format the request data as JSON.
   * @private
   */
  private jsonBody = true;
  /**
   * Parse the response as JSON, an array buffer, or not at all.
   * @private
   */
  private responseType: "json" | "arraybuffer" | "none" = "json";
  /**
   * The request headers to include.
   * @private
   */
  private headers: Record<string, string> = {};

  constructor(
    endpoint: keyof typeof Endpoint,
    pathVariables?: Record<QueryParam, string>,
    queryVariables?: Record<string, string>
  ) {
    this.relativeUrl = Endpoint[endpoint];
    this.pathVariables = pathVariables || {};
    this.queryVariables = queryVariables || {};
  }

  /**
   * Builds a new request for the given endpoint.
   * @param endpoint - The endpoint to build a request for.
   * @param pathVariables - Any path variables to fill in.
   */
  static buildRequest<R = void, Q extends string = string, B = void>(
    endpoint: keyof typeof Endpoint,
    pathVariables?: Record<Q, string>,
    queryVariables?: Record<string, string>
  ): RequestBuilder<R, Q, B> {
    return new RequestBuilder<R, Q, B>(endpoint, pathVariables, queryVariables);
  }

  /**
   * Updates the request response type.
   * @param type - The response type to use.
   */
  withResponseType(type: "json" | "arraybuffer" | "none"): this {
    this.responseType = type;
    return this;
  }

  /**
   * Handles the body type as form data.
   */
  withFormData(): this {
    this.jsonBody = false;
    return this;
  }

  /**
   * Performs a request to the session endpoints.
   * @param req - The arguments to pass to the fetch function.
   * @param ignoreResponse - Whether to ignore the response.
   * @return The response data.
   */
  async sessionRequest(
    req: Parameters<typeof fetch>[1],
    ignoreResponse?: boolean
  ): Promise<ReturnType> {
    const response = await fetch(`${BASE_URL}/${this.relativeUrl}`, {
      ...req,
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      throw Error("Unable to find a session.");
    }

    return ignoreResponse ? undefined : response.json();
  }

  /**
   * Run a GET request to retrieve data.
   * @return The response data.
   */
  async get(): Promise<ReturnType> {
    return await this.request("GET");
  }

  /**
   * Run a POST request to create data.
   * @param body - The body of the request.
   * @return The response data.
   */
  async post(body: BodyType): Promise<ReturnType> {
    return await this.request("POST", body);
  }

  /**
   * Run a PUT request to update data.
   * @param body - The body of the request.
   * @return The response data.
   */
  async put(body: BodyType): Promise<ReturnType> {
    return await this.request("PUT", body);
  }

  /**
   * Run a DELETE request to remove data.
   * @param body - The body of the request.
   * @return The response data.
   */
  async delete(body?: BodyType): Promise<ReturnType> {
    return await this.request("DELETE", body);
  }

  /**
   * Performs an API request.
   * @param method - The method to use for the request.
   * @param body - The body of the request.
   * @return The response data.
   */
  private async request(
    method: APIMethods,
    body?: BodyType
  ): Promise<ReturnType> {
    let url = `${BASE_URL}/${this.relativeUrl}`;

    // Add path variables to the URL.
    Object.entries(this.pathVariables).forEach(([key, value]) => {
      url = url.replace(`:${key}`, value);
    });

    // Add query parameters to the URL.
    const query = new URLSearchParams(this.queryVariables);

    url = `${url}${query ? `?${query}` : ""}`;

    const res = await fetch(url, {
      credentials: "include",
      headers: this.jsonBody
        ? {
            ...(this.headers || {}),
            "Content-Type": "application/json",
          }
        : this.headers,
      method,
      body: this.jsonBody ? JSON.stringify(body) : (body as unknown as string),
    });

    if (this.responseType === "arraybuffer") {
      return (await res.arrayBuffer()) as unknown as ReturnType;
    }

    const content = await res.text();

    if (res.status === LOGOUT_STATUS_CODE && !url.includes("credentials")) {
      // Log out of the app if credentials expire, and not if integration credentials expire.
      throw Error(LOGOUT_ERROR);
    } else if (this.responseType !== "json") {
      return content as unknown as ReturnType;
    }

    const data = content ? JSON.parse(content) : undefined;

    if (!res.ok) {
      throw Error(data.error);
    } else {
      return data as ReturnType;
    }
  }
}

export default RequestBuilder.buildRequest;
