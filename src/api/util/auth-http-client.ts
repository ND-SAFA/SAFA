import { APIOptions } from "@/types";
import { isAPIError } from "@/util";
import { logModule, sessionModule } from "@/store";
import { baseURL } from "./endpoints";
import { logout } from "@/api/handlers";

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

    logModule.onDevError(error);

    throw Error(error);
  } else {
    options.headers = {
      ...options.headers,
      Authorization: token,
    };
  }

  const res = await fetch(URL, options);

  if (res.status === 403) {
    const message = "Session has timed out. Please log back in.";
    logModule.onWarning(message);
    await logout();
    throw Error(message);
  }

  if (res.status === 204) {
    // TODO: will be removed in the next PR containing the proper use of http codes.
    return {} as T;
  }
  const resContent = await res.text();

  if (resContent === "") {
    return {} as T;
  }

  const resJson = JSON.parse(resContent);

  if (!res.ok || isAPIError(resJson)) {
    logModule.onServerError(resJson.body);

    throw Error(resJson.body.message);
  } else {
    return resJson.body;
  }
}
