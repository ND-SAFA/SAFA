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
 * @param authenticate Whether the request is authenticated or not. If so then
 * the current session token is included in header.
 *
 * @return The request's response data.
 * @throws Any errors received from the request.
 */
export default async function httpClient<T>(
  relativeUrl: string,
  options: APIOptions,
  setJsonContentType = true,
  authenticate = true
): Promise<T> {
  return new Promise((resolve, reject) => {
    options = options || {};
    if (setJsonContentType) {
      options.headers = {
        "Content-Type": "application/json",
      };
    }

    const token = sessionModule.getToken;
    if (authenticate) {
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
      .then((res) => {
        if (res.headers.has("token")) {
          const token = res.headers.get("token");
          sessionModule.SET_TOKEN(token === null ? undefined : token);
        } else if (res.status === 403 || res.status === 401) {
          appModule.onError("User is not authorized to perform this action.");
        }
        console.log("RESPONSE----------------------", res);
        return res.json();
      })
      .then((responseJson: APIResponse<T>) => {
        if (isAPIError(responseJson)) {
          appModule.onServerError(responseJson.body);
          reject(responseJson.body.message);
        } else {
          resolve(responseJson.body);
        }
      })
      .catch((e) => {
        console.log("FAIL HERE-----------------------------");
        console.error(e);
        const errorMessage =
          "Could not connect to backend due to a connection error, please verify that server is running.";
        appModule.onError(errorMessage);
        reject(e);
      });
  });
}
