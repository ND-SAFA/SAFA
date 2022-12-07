import { ArtifactSchema, ProjectSchema, TraceLinkSchema } from "@/types";
import {
  ENABLED_FEATURES,
  EXAMPLE_ATTRIBUTE_LAYOUTS,
  EXAMPLE_ATTRIBUTES,
} from "@/util";
import { Endpoint, fillEndpoint, authHttpClient } from "@/api/util";

/**
 * Gets a specific version of a project.
 *
 * @param versionId - The project version ID to get.
 * @return The matching project.
 */
export async function getProjectVersion(
  versionId: string
): Promise<ProjectSchema> {
  const project = await authHttpClient<ProjectSchema>(
    fillEndpoint(Endpoint.projectVersion, { versionId }),
    { method: "GET" }
  );

  if (ENABLED_FEATURES.EXAMPLE_ATTRIBUTES) {
    project.attributes = EXAMPLE_ATTRIBUTES;
    project.attributeLayouts = EXAMPLE_ATTRIBUTE_LAYOUTS;
  }

  return project;
}

/**
 * Returns the list of artifacts in the given version.
 *
 * @param versionId - The version whose artifacts are returned.
 * @return The list of artifacts.
 */
export async function getArtifactsInVersion(
  versionId: string
): Promise<ArtifactSchema[]> {
  return authHttpClient<ArtifactSchema[]>(
    fillEndpoint(Endpoint.getArtifactsInVersion, { versionId }),
    { method: "GET" }
  );
}

/**
 * Returns the list of trace links in the given version.
 *
 * @param versionId - The version whose trace links are returned.
 * @return The list of trace links.
 */
export async function getTracesInVersion(
  versionId: string
): Promise<TraceLinkSchema[]> {
  return authHttpClient<TraceLinkSchema[]>(
    fillEndpoint(Endpoint.getTracesInVersion, { versionId }),
    { method: "GET" }
  );
}
