import { SearchQuerySchema, SearchResultsSchema } from "@/types";
import { authHttpClient, Endpoint, fillEndpoint } from "@/api";

/**
 * Returns the search results within a project version for the given query.
 * @param versionId - The version to search within.
 * @param query - The query data defining what to search for.
 * @return The matching artifact ids.
 */
export function getProjectSearchQuery(
  versionId: string,
  query: SearchQuerySchema
): Promise<SearchResultsSchema> {
  return authHttpClient<SearchResultsSchema>(
    fillEndpoint(Endpoint.search, { versionId }),
    {
      method: "POST",
      body: JSON.stringify(query),
    }
  );
}
