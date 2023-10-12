package edu.nd.crc.safa.features.memberships.entities.db;

import java.util.UUID;

import edu.nd.crc.safa.features.organizations.entities.app.MembershipType;

/**
 * This interface represents a generic membership in an organization,
 * a team, or a project.
 *
 * @see OrganizationMembership
 * @see TeamMembership
 * @see ProjectMembership
 */
public interface EntityMembership {
    /**
     * Retrieve the ID of the membership
     *
     * @return The membership ID
     */
    UUID getId();

    /**
     * Retrieve the email of the user represented by the membership
     *
     * @return The user's email
     */
    String getEmail();

    /**
     * Retrieve the membership role as a string. This is used
     * to send the role to the front end. Note that one user
     * can have many memberships in a given entity, representing
     * multiple roles.
     *
     * @return The string representation of this membership's role
     * @see edu.nd.crc.safa.features.organizations.entities.db.OrganizationRole
     * @see edu.nd.crc.safa.features.organizations.entities.db.TeamRole
     * @see edu.nd.crc.safa.features.organizations.entities.db.ProjectRole
     */
    String getRoleAsString();

    /**
     * Retrieve the membership type
     *
     * @return The membership type
     */
    MembershipType getMembershipType();

    /**
     * Retrieve the ID of the entity the membership belongs to.
     * For example if this is an organization membership, this function
     * returns the ID of the organization.
     *
     * @return The entity ID
     */
    UUID getEntityId();
}
