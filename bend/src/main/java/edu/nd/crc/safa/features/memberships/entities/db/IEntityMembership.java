package edu.nd.crc.safa.features.memberships.entities.db;

import java.util.UUID;

import edu.nd.crc.safa.features.organizations.entities.app.MembershipType;
import edu.nd.crc.safa.features.organizations.entities.db.IEntityWithMembership;
import edu.nd.crc.safa.features.organizations.entities.db.IRole;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

/**
 * This interface represents a generic membership in an organization,
 * a team, or a project.
 *
 * @see OrganizationMembership
 * @see TeamMembership
 * @see ProjectMembership
 */
public interface IEntityMembership {
    /**
     * Retrieve the ID of the membership
     *
     * @return The membership ID
     */
    UUID getId();

    /**
     * Retrieve the membership type
     *
     * @return The membership type
     */
    MembershipType getMembershipType();

    /**
     * Get the user involved in this membership
     *
     * @return The user
     */
    SafaUser getUser();

    /**
     * Get the entity associated with this membership
     *
     * @return The membership's entity
     */
    IEntityWithMembership getEntity();

    /**
     * Get the role for this membership
     *
     * @return The membership's role
     */
    IRole getRole();
}
