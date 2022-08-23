import { APIOptions } from "@/types";
import { logStore } from "@/hooks";
import { baseURL } from "@/api";
import { handleLogout } from "@/api/handlers";
import { sessionStore } from "@/hooks";

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
  const token = sessionStore.getToken;
  const URL = `${baseURL}/${relativeUrl}`;

  if (setJsonContentType) {
    options.headers = {
      "Content-Type": "application/json",
    };
  }

  if (token === undefined) {
    const error = `${relativeUrl} requires token.`;

    logStore.onDevError(error);

    throw Error(error);
  } else {
    options.headers = {
      ...options.headers,
      Authorization: token,
    };
  }

  const fetchResponse = await fetch(URL, options);

  let message;
  let resContent;
  switch (fetchResponse.status) {
    case 403:
      message = "Session has timed out. Please log back in.";
      logStore.onWarning(message);
      await handleLogout();
      throw Error(message);
    case 204:
      return {} as T;
    default:
      resContent = await fetchResponse.text();
      if (resContent === "" || resContent === "created") {
        return {} as T;
      }
  }

  const resJson = JSON.parse(resContent);

  if (!fetchResponse.ok) {
    logStore.onServerError(resJson);

    throw Error(resJson.error);
  } else {
    return resJson;
  }
}
