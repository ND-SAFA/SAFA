package edu.nd.crc.safa.features.organizations.entities.db;

import java.util.UUID;

/**
 * An interface representing entities that can have memberships
 *
 * @see Organization
 * @see edu.nd.crc.safa.features.projects.entities.db.Project
 * @see Team
 */
public interface IEntityWithMembership {
    /**
     * Get the ID of the entity
     *
     * @return The entity's ID
     */
    UUID getId();
}
