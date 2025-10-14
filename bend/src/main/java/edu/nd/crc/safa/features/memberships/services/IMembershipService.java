package edu.nd.crc.safa.features.memberships.services;

import java.util.List;
import java.util.Optional;
import java.util.UUID;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.memberships.entities.db.IEntityMembership;
import edu.nd.crc.safa.features.organizations.entities.db.IEntityWithMembership;
import edu.nd.crc.safa.features.organizations.entities.db.IRole;
import edu.nd.crc.safa.features.projects.entities.app.SafaItemNotFoundError;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

/**
 * This is an interface which represents a service that provides information about
 * user memberships within some entity. An entity is something like an organization
 * or team in which a user can have some number of memberships, each of which has
 * an associated role.
 */
public interface IMembershipService {

    /**
     * Applies a role to a user within an entity. If the user already has this
     * role in this entity, this function does nothing.
     *
     * @param user The user to get the new role
     * @param entity The entity the role applies to
     * @param role The role
     * @return The new entity membership, or the old one if it already existed
     */
    IEntityMembership addUserRole(SafaUser user, IEntityWithMembership entity, IRole role);

    /**
     * Removes a role from a user within an entity. If the user didn't already have this
     * role in this entity, this function does nothing.
     *
     * @param user The user to remove the role from
     * @param entity The entity the role applies to
     * @param role The role
     */
    void removeUserRole(SafaUser user, IEntityWithMembership entity, IRole role);

    /**
     * Get the list of roles the user has within the entity.
     *
     * @param user The user in question
     * @param entity The entity to check within
     * @return The roles the user has in that entity
     */
    List<IRole> getRolesForUser(SafaUser user, IEntityWithMembership entity);

    /**
     * Get all entities for a user.
     *
     * @param user The user
     * @return The teams the user is on
     */
    default List<IEntityWithMembership> getEntitiesForUser(SafaUser user) {
        return getMembershipsForUser(user)
            .stream()
            .map(IEntityMembership::getEntity)
            .collect(Collectors.toList());
    }

    /**
     * Get all membership objects associated with a user
     *
     * @param user The user
     * @return The memberships that user is in
     */
    List<IEntityMembership> getMembershipsForUser(SafaUser user);

    /**
     * Get all membership objects associated with an entity
     *
     * @param entity The entity
     * @return The memberships in that entity
     */
    List<IEntityMembership> getMembershipsForEntity(IEntityWithMembership entity);

    /**
     * Get all users within an entity
     *
     * @param entity The entity
     * @return The members of the entity
     */
    default List<SafaUser> getUsersInEntity(IEntityWithMembership entity) {
        return getMembershipsForEntity(entity)
            .stream()
            .map(IEntityMembership::getUser)
            .distinct()
            .collect(Collectors.toUnmodifiableList());
    }

    /**
     * Search for an entity membership by its ID.
     *
     * @param membershipId The ID of the membership
     * @return The membership, if it exists
     */
    Optional<IEntityMembership> getMembershipOptionalById(UUID membershipId);

    /**
     * Search for an entity membership by its ID. Throw an exception
     * if it's not found.
     *
     * @param membershipId The ID of the membership
     * @return The membership, if it exists
     * @throws SafaItemNotFoundError If the membership could not be found
     */
    default IEntityMembership getMembershipById(UUID membershipId) {
        return getMembershipOptionalById(membershipId)
            .orElseThrow(() -> new SafaItemNotFoundError("No membership found with the specified ID"));
    }
}
