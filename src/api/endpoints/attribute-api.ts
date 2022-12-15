import { AttributeLayoutSchema, AttributeSchema } from "@/types";
import { ENABLED_FEATURES } from "@/util";
import { authHttpClient, Endpoint, fillEndpoint } from "@/api";

/**
 * Creates a new artifact custom attribute.
 *
 * @param projectId - The project to create the attribute on.
 * @param attribute - The attribute to create.
 * @return The created attribute.
 */
export async function createAttribute(
  projectId: string,
  attribute: AttributeSchema
): Promise<AttributeSchema> {
  if (ENABLED_FEATURES.EXAMPLE_ATTRIBUTES) {
    return attribute;
  }
  return authHttpClient<AttributeSchema>(
    fillEndpoint(Endpoint.createAttribute, {
      projectId,
    }),
    {
      method: "POST",
      body: JSON.stringify(attribute),
    }
  );
}

/**
 * Edits an artifact custom attribute.
 *
 * @param projectId - The project to edit the attribute on.
 * @param attribute - The attribute to edit.
 * @return The edited attribute.
 */
export async function editAttribute(
  projectId: string,
  attribute: AttributeSchema
): Promise<AttributeSchema> {
  if (ENABLED_FEATURES.EXAMPLE_ATTRIBUTES) {
    return attribute;
  }
  return authHttpClient<AttributeSchema>(
    fillEndpoint(Endpoint.editAttribute, {
      projectId,
      key: attribute.key,
    }),
    {
      method: "PUT",
      body: JSON.stringify(attribute),
    }
  );
}

/**
 * Deletes an artifact custom attribute.
 *
 * @param projectId - The project to delete the attribute on.
 * @param attribute - The attribute to delete.
 */
export async function deleteAttribute(
  projectId: string,
  attribute: AttributeSchema
): Promise<void> {
  if (ENABLED_FEATURES.EXAMPLE_ATTRIBUTES) {
    return;
  }
  return authHttpClient<void>(
    fillEndpoint(Endpoint.editAttribute, {
      projectId,
      key: attribute.key,
    }),
    {
      method: "DELETE",
    }
  );
}

/**
 * Creates a new artifact attribute layout.
 *
 * @param projectId - The project to create the attribute layout on.
 * @param layout - The attribute layout to create.
 * @return The created attribute layout.
 */
export async function createAttributeLayout(
  projectId: string,
  layout: AttributeLayoutSchema
): Promise<AttributeLayoutSchema> {
  if (ENABLED_FEATURES.EXAMPLE_ATTRIBUTES) {
    return layout;
  }
  return authHttpClient<AttributeLayoutSchema>(
    fillEndpoint(Endpoint.createAttributeLayout, {
      projectId,
    }),
    {
      method: "POST",
      body: JSON.stringify(layout),
    }
  );
}

/**
 * Edits an artifact attribute layout.
 *
 * @param projectId - The project to edit the attribute layout on.
 * @param layout - The attribute layout to edit.
 * @return The edited attribute layout.
 */
export async function editAttributeLayout(
  projectId: string,
  layout: AttributeLayoutSchema
): Promise<AttributeLayoutSchema> {
  if (ENABLED_FEATURES.EXAMPLE_ATTRIBUTES) {
    return layout;
  }
  return authHttpClient<AttributeLayoutSchema>(
    fillEndpoint(Endpoint.editAttribute, {
      projectId,
      id: layout.id,
    }),
    {
      method: "PUT",
      body: JSON.stringify(layout),
    }
  );
}

/**
 * Deletes an artifact attribute layout.
 *
 * @param projectId - The project to delete the attribute layout on.
 * @param layout - The attribute layout to delete.
 */
export async function deleteAttributeLayout(
  projectId: string,
  layout: AttributeLayoutSchema
): Promise<void> {
  if (ENABLED_FEATURES.EXAMPLE_ATTRIBUTES) {
    return;
  }
  return authHttpClient<void>(
    fillEndpoint(Endpoint.editAttribute, {
      projectId,
      id: layout.id,
    }),
    {
      method: "DELETE",
    }
  );
}
