import { APIOptions, APIResponse, isAPIError } from "@/types/api";
import { appModule } from "@/store";
import { baseURL } from "@/api/base-url";

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
          reject(new Error(responseJson.body.message));
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
