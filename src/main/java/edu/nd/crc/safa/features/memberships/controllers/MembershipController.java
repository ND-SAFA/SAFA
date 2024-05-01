package edu.nd.crc.safa.features.memberships.controllers;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.authentication.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.memberships.entities.db.IEntityMembership;
import edu.nd.crc.safa.features.memberships.services.MembershipService;
import edu.nd.crc.safa.features.organizations.entities.app.MembershipAppEntity;
import edu.nd.crc.safa.features.organizations.entities.db.IRole;
import edu.nd.crc.safa.features.permissions.services.PermissionService;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.users.services.SafaUserService;
import edu.nd.crc.safa.utilities.exception.UserError;

import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class MembershipController extends BaseController {
    private final MembershipService membershipService;
    private final SafaUserService safaUserService;
    private final PermissionService permissionService;

    public MembershipController(ResourceBuilder resourceBuilder, ServiceProvider serviceProvider,
                                MembershipService membershipService, SafaUserService safaUserService,
                                PermissionService permissionService) {
        super(resourceBuilder, serviceProvider);
        this.membershipService = membershipService;
        this.safaUserService = safaUserService;
        this.permissionService = permissionService;
    }

    /**
     * Get all memberships by an entity's ID. An entity can be an organization, a team,
     * or a project.
     *
     * @param entityId The ID of the entity
     * @return All memberships within the entity, if it exists
     */
    @GetMapping(AppRoutes.Memberships.BY_ENTITY_ID)
    public List<MembershipAppEntity> getMembers(@PathVariable UUID entityId) {
        List<IEntityMembership> memberships = membershipService.getMembers(entityId, getCurrentUser());
        return toAppEntities(memberships);
    }

    /**
     * Create a new membership within an entity. An entity can be an organization, a team,
     * or a project.
     *
     * @param entityId      The ID of the entity
     * @param newMembership The definition of the new membership. Only the email and role fields are read
     * @return The newly created membership
     */
    @PostMapping(AppRoutes.Memberships.BY_ENTITY_ID)
    public MembershipAppEntity createNewMembership(
            @PathVariable UUID entityId,
            @RequestBody MembershipAppEntity newMembership
    ) throws UserError {
        SafaUser newMember = safaUserService.getUserByEmail(newMembership.getEmail());

        List<IRole> userRoles = membershipService.getUserRoles(newMember, entityId);
        if (userRoles.isEmpty() && !permissionService.isActiveSuperuser(getCurrentUser())) {
            throw new UserError("User is not yet a member of this entity and must be invited first.");
        }

        IEntityMembership membership =
                membershipService.createMembership(entityId, newMembership.getRole(), newMember, getCurrentUser());
        return new MembershipAppEntity(membership);
    }

    /**
     * Modify a user membership within an entity. An entity can be an organization, a team,
     * or a project. Note that due to how the back end handles roles, the modified
     * membership will actually be a new membership with a new ID.
     *
     * @param entityId     The ID of the entity
     * @param membershipId The ID of the membership to modify
     * @param membership   The modified membership definition. Only the role field is used
     * @return The new membership entity
     */
    @PutMapping(AppRoutes.Memberships.BY_ENTITY_ID_AND_MEMBERSHIP_ID)
    public MembershipAppEntity modifyMembership(
            @PathVariable UUID entityId,
            @PathVariable UUID membershipId,
            @RequestBody MembershipAppEntity membership
    ) {
        IEntityMembership updatedMembership =
                membershipService.updateMembership(entityId, membershipId, membership.getRole(), getCurrentUser());
        return new MembershipAppEntity(updatedMembership);
    }

    /**
     * Delete a membership within an entity. An entity can be an organization, a team,
     * or a project.
     *
     * @param entityId     The ID of the entity
     * @param membershipId The ID of the membership to delete
     */
    @DeleteMapping(AppRoutes.Memberships.BY_ENTITY_ID_AND_MEMBERSHIP_ID)
    public void deleteMembership(@PathVariable UUID entityId, @PathVariable UUID membershipId) {
        membershipService.deleteMembership(entityId, membershipId, getCurrentUser());
    }

    /**
     * Delete all roles for a user within a given entity. An entity can be an organization, a team,
     * or a project. Either userId or userEmail must be supplied. If both are supplied, userId takes
     * precedence.
     *
     * @param entityId  the ID of the entity
     * @param userId    The ID of the user
     * @param userEmail The email of the user
     */
    @DeleteMapping(AppRoutes.Memberships.BY_ENTITY_ID)
    public void deleteAllMembershipsForUser(
            @PathVariable UUID entityId,
            @RequestParam(required = false) UUID userId,
            @RequestParam(required = false) String userEmail
    ) {
        SafaUser member;
        if (userId != null) {
            member = getServiceProvider().getSafaUserService().getUserById(userId);
        } else if (userEmail != null) {
            member = getServiceProvider().getSafaUserService().getUserByEmail(userEmail);
        } else {
            throw new SafaError("Must supply either userId or userEmail");
        }

        membershipService.deleteAllUserMemberships(entityId, member, getCurrentUser());
    }

    /**
     * Convert a list of entity memberships into {@link MembershipAppEntity} objects
     *
     * @param memberships The entities to convert
     * @return The converted entities
     */
    private List<MembershipAppEntity> toAppEntities(List<? extends IEntityMembership> memberships) {
        return memberships.stream().map(MembershipAppEntity::new).toList();
    }

}
