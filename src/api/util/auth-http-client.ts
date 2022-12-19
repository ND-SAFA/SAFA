import { APIOptions } from "@/types";
import { logStore } from "@/hooks";
import { baseURL } from "@/api";
import { handleLogout } from "@/api/handlers";

/**
 * Executes an http request with the given parameters containing current
 * session token in request headers.
 *
 * @param relativeUrl - The URL relative to the BEND API endpoint.
 * @param options - Any options for this request, such as the method and any data.
 * @param setJsonContentType - If true, sets the content type of the request.
 * @param parseResponse - If true, the response will be parsed as JSON.
 * @param arrayBuffer - If true, the response will be parsed as an array buffer
 *
 * @return The request's response data.
 * @throws Any errors received from the request.
 */
export default async function authHttpClient<T>(
  relativeUrl: string,
  options: APIOptions,
  { setJsonContentType = true, parseResponse = true, arrayBuffer = false } = {}
): Promise<T> {
  const res = await fetch(`${baseURL}/${relativeUrl}`, {
    ...options,
    credentials: "include",
    headers: setJsonContentType
      ? {
          ...(options.headers || {}),
          "Content-Type": "application/json",
        }
      : options.headers,
  });

  if (arrayBuffer) {
    return (await res.arrayBuffer()) as unknown as T;
  }

  const content = await res.text();

  if (res.status === 403) {
    const message = "Session has timed out. Please log back in.";

    await handleLogout();

    logStore.onWarning(message);
    throw Error(message);
  } else if (res.status === 204 || content === "" || content === "created") {
    // TODO: is this legacy code even necessary?
    return {} as T;
  } else if (!parseResponse) {
    return content as unknown as T;
  }

  const data = JSON.parse(content);

  if (!res.ok) {
    logStore.onDevError(data.error);
    throw Error(data.error);
  } else {
    return data;
  }
}
