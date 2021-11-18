import { APIOptions, APIResponse } from "@/types";
import { isAPIError } from "@/util";
import { appModule } from "@/store";
import { baseURL } from "@/api/endpoints/endpoints";

/**
 * Executes an http request with the given parameters.
 *
 * @param relativeUrl - The URL relative to the BEND API endpoint.
 * @param options - Any options for this request, such as the method and any data.
 * @param setContentType - If true, sets the content type of the request.
 *
 * @return The request's response data.
 * @throws Any errors received from the request.
 */
export default async function httpClient<T>(
  relativeUrl: string,
  options: APIOptions,
  setContentType = true
): Promise<T> {
  return new Promise((resolve, reject) => {
    options = options || {};
    if (setContentType) {
      options.headers = {
        "Content-Type": "application/json",
      };
    }

    const URL = `${baseURL}/${relativeUrl}`;

    fetch(URL, options)
      .then((a) => a.json())
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
