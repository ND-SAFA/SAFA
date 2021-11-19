import { APIOptions, APIResponse } from "@/types";
import { isAPIError } from "@/util";
import { appModule, sessionModule } from "@/store";
import { baseURL } from "@/api/endpoints/endpoints";

/**
 * Executes an http request with the given parameters containing current
 * session token in request headers.
 *
 * @param relativeUrl The URL relative to the BEND API endpoint.
 * @param options Any options for this request, such as the method and any data.
 * @param setJsonContentType If true, sets the content type of the request.
 *
 * @return The request's response data.
 * @throws Any errors received from the request.
 */
export default async function authHttpClient<T>(
  relativeUrl: string,
  options: APIOptions,
  setJsonContentType = true
): Promise<T> {
  return new Promise((resolve, reject) => {
    options = options || {};
    if (setJsonContentType) {
      options.headers = {
        "Content-Type": "application/json",
      };
    }

    const token = sessionModule.getToken;
    if (token === undefined) {
      const error = `${relativeUrl} is required token but non exists.`;
      appModule.onDevError(error);
      return reject(error);
    } else {
      options.headers = {
        ...options.headers,
        Authorization: token,
      };
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
