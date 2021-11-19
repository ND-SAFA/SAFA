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
  const token = sessionModule.getToken;
  const URL = `${baseURL}/${relativeUrl}`;

  if (setJsonContentType) {
    options.headers = {
      "Content-Type": "application/json",
    };
  }

  if (token === undefined) {
    const error = `${relativeUrl} requires token.`;
    appModule.onDevError(error);
    throw Error(error);
  } else {
    options.headers = {
      ...options.headers,
      Authorization: token,
    };
  }

  const res = await fetch(URL, options);
  const resContent = await res.json();

  if (!res.ok || isAPIError(resContent)) {
    appModule.onServerError(resContent.body);

    throw Error(resContent.body.message);
  } else {
    return resContent.body;
  }
}
