import { AttributePositionSchema } from "@/types";

/**
 * TODO: hook up properly to endpoints and stores.
 *
 * Updates an attribute layout.
 *
 * @param position - The attribute being updated.
 * @param newPosition - The new attribute position.
 */
export async function handleUpdateAttributeLayout(
  position: AttributePositionSchema,
  newPosition: Partial<AttributePositionSchema>
): Promise<void> {
  console.log(position, newPosition);

  if (newPosition.x) position.x = newPosition.x;
  if (newPosition.y) position.y = newPosition.y;
  if (newPosition.width) position.width = newPosition.width;
  if (newPosition.height) position.height = newPosition.height;
}
