import { APIOptions, APIResponse } from "@/types";
import { isAPIError } from "@/util";
import { appModule, sessionModule } from "@/store";
import { baseURL } from "@/api/endpoints/endpoints";

/**
 * Executes an http request with the given parameters.
 *
 * @param relativeUrl The URL relative to the BEND API endpoint.
 * @param options Any options for this request, such as the method and any data.
 * @param setJsonContentType If true, sets the content type of the request.
 * @param authenticated Whether the request should include the session token.
 *
 * @return The request's response data.
 * @throws Any errors received from the request.
 */
export default async function httpClient<T>(
  relativeUrl: string,
  options: APIOptions,
  setJsonContentType = true,
  authenticated = true
): Promise<T> {
  return new Promise((resolve, reject) => {
    options = options || {};
    if (setJsonContentType) {
      options.headers = {
        "Content-Type": "application/json",
      };
    }

    if (authenticated) {
      const token = sessionModule.getToken;
      if (token === undefined) {
        const error = `${relativeUrl} is required token but non exists.`;
        appModule.onDevError(error);
        reject(error);
      } else {
        options.headers = {
          ...options.headers,
          Authorization: token,
        };
      }
    }

    const URL = `${baseURL}/${relativeUrl}`;

    fetch(URL, options)
      .then((res) => res.json())
      .then((responseJson: APIResponse<T>) => {
        if (isAPIError(responseJson)) {
          appModule.onServerError(responseJson.body);
          reject(responseJson.body.message);
        } else {
          resolve(responseJson.body);
        }
      })
      .catch((e) => {
        const errorMessage =
          "Could not connect to backend due to a connection error, please verify that server is running.";
        appModule.onError(errorMessage);
        reject(e);
      });
  });
}
