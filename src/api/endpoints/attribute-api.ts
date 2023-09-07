import { AttributeLayoutSchema, AttributeSchema } from "@/types";
import { buildRequest } from "@/api";

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
  return buildRequest<AttributeSchema, "projectId", AttributeSchema>(
    "createAttribute"
  )
    .withParam("projectId", projectId)
    .post(attribute);
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
  return buildRequest<AttributeSchema, "projectId" | "key", AttributeSchema>(
    "editAttribute"
  )
    .withParam("projectId", projectId)
    .withParam("key", attribute.key)
    .put(attribute);
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
  return buildRequest<void, "projectId" | "key">("editAttribute")
    .withParam("projectId", projectId)
    .withParam("key", attribute.key)
    .delete();
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
  return buildRequest<
    AttributeLayoutSchema,
    "projectId",
    AttributeLayoutSchema
  >("createAttributeLayout")
    .withParam("projectId", projectId)
    .post(layout);
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
  return buildRequest<
    AttributeLayoutSchema,
    "id" | "projectId",
    AttributeLayoutSchema
  >("editAttributeLayout")
    .withParam("projectId", projectId)
    .withParam("id", layout.id)
    .put(layout);
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
  return buildRequest<void, "id" | "projectId">("editAttributeLayout")
    .withParam("projectId", projectId)
    .withParam("id", layout.id)
    .delete();
}
