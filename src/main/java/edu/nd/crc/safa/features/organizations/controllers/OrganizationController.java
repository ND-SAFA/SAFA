package edu.nd.crc.safa.features.organizations.controllers;

import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;

import edu.nd.crc.safa.authentication.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.memberships.entities.db.OrganizationMembership;
import edu.nd.crc.safa.features.memberships.services.OrganizationMembershipService;
import edu.nd.crc.safa.features.organizations.entities.app.OrganizationAppEntity;
import edu.nd.crc.safa.features.organizations.entities.db.Organization;
import edu.nd.crc.safa.features.organizations.entities.db.PaymentTier;
import edu.nd.crc.safa.features.organizations.services.OrganizationService;
import edu.nd.crc.safa.features.permissions.entities.OrganizationPermission;
import edu.nd.crc.safa.features.permissions.services.PermissionService;
import edu.nd.crc.safa.features.projects.entities.app.SafaItemNotFoundError;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class OrganizationController extends BaseController {

    private final OrganizationService organizationService;
    private final OrganizationMembershipService organizationMembershipService;
    private final PermissionService permissionService;

    public OrganizationController(ResourceBuilder resourceBuilder, ServiceProvider serviceProvider,
                                  OrganizationService organizationService,
                                  OrganizationMembershipService organizationMembershipService,
                                  PermissionService permissionService) {
        super(resourceBuilder, serviceProvider);
        this.organizationService = organizationService;
        this.organizationMembershipService = organizationMembershipService;
        this.permissionService = permissionService;
    }

    /**
     * Get all organizations for a given user.
     *
     * @return A list of organizations the user is a part of.
     */
    @GetMapping(AppRoutes.Organizations.ROOT)
    public List<OrganizationAppEntity> getUserOrganizations() {
        SafaUser user = getCurrentUser();

        List<OrganizationMembership> orgMemberships =
            organizationMembershipService.getOrganizationMembershipsForUser(user);

        return orgMemberships.stream()
            .map(OrganizationMembership::getOrganization)
            .filter(org -> permissionService.hasPermission(OrganizationPermission.VIEW, org, user))
            .map(org -> organizationService.getAppEntity(org, user))
            .collect(Collectors.toUnmodifiableList());
    }

    /**
     * Get an organization by its ID.
     *
     * @param orgId The ID of the organization
     * @return The organization if it is found.
     * @throws SafaItemNotFoundError If no organization with the given ID is found.
     */
    @GetMapping(AppRoutes.Organizations.BY_ID)
    public OrganizationAppEntity getOrganization(@PathVariable UUID orgId) {
        SafaUser user = getCurrentUser();
        Organization org = getResourceBuilder()
            .fetchOrganization(orgId)
            .withPermission(OrganizationPermission.VIEW, user)
            .get();
        return organizationService.getAppEntity(org, user);
    }

    /**
     * Get the current user's personal organization.
     *
     * @return The personal organization of the current user.
     */
    @GetMapping(AppRoutes.Organizations.SELF)
    public OrganizationAppEntity getPersonalOrganization() {
        SafaUser user = getCurrentUser();
        // No permission check because users can always see their own personal org
        return organizationService.getAppEntity(organizationService.getPersonalOrganization(user), user);
    }

    /**
     * Create a new organization. The organization will be set to the "free" tier and will be owned by the
     * current authenticated user.
     *
     * @param newOrgEntity The definition of the new organization. Only the name and description fields are read.
     * @return The newly created organization.
     */
    @PostMapping(AppRoutes.Organizations.ROOT)
    public OrganizationAppEntity createNewOrganization(@RequestBody OrganizationAppEntity newOrgEntity) {
        SafaUser user = getCurrentUser();
        permissionService.requireActiveSuperuser(user);
        Organization orgDefinition = new Organization(newOrgEntity.getName(), newOrgEntity.getDescription(),
            user, PaymentTier.AS_NEEDED, false);
        Organization newOrg = organizationService.createNewOrganization(orgDefinition);
        return organizationService.getAppEntity(newOrg, user);
    }

    /**
     * Modify an organization.
     *
     * @param orgId The ID of the organization to modify.
     * @param orgEntity The definition of the fields to change. Only the name and description fields are read, and
     *                  if any field is not provided the value of that field will not be modified.
     * @return The updated organization
     */
    @PutMapping(AppRoutes.Organizations.BY_ID)
    public OrganizationAppEntity updateOrganization(@PathVariable UUID orgId,
                                                    @RequestBody OrganizationAppEntity orgEntity) {
        SafaUser user = getCurrentUser();
        Organization currentOrg = getResourceBuilder()
            .fetchOrganization(orgId)
            .withPermission(OrganizationPermission.EDIT, user)
            .get();
        currentOrg.setFromAppEntity(orgEntity);
        return organizationService.getAppEntity(organizationService.updateOrganization(currentOrg), user);
    }

    /**
     * Delete an organization.
     *
     * @param orgId The ID of the organization to delete.
     */
    @DeleteMapping(AppRoutes.Organizations.BY_ID)
    public void deleteOrganization(@PathVariable UUID orgId) {
        SafaUser user = getCurrentUser();
        Organization org = getResourceBuilder()
            .fetchOrganization(orgId)
            .withPermission(OrganizationPermission.DELETE, user)
            .get();
        organizationService.deleteOrganization(org);
    }
}
