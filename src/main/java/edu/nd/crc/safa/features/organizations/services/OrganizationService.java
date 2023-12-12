package edu.nd.crc.safa.features.organizations.services;

import static edu.nd.crc.safa.utilities.AssertUtils.assertNotNull;
import static edu.nd.crc.safa.utilities.AssertUtils.assertNull;

import java.util.Collection;
import java.util.List;
import java.util.Optional;
import java.util.Set;
import java.util.UUID;

import edu.nd.crc.safa.features.billing.entities.MonthlyUsage;
import edu.nd.crc.safa.features.billing.entities.db.BillingInfo;
import edu.nd.crc.safa.features.billing.services.BillingService;
import edu.nd.crc.safa.features.memberships.entities.db.IEntityMembership;
import edu.nd.crc.safa.features.memberships.services.OrganizationMembershipService;
import edu.nd.crc.safa.features.organizations.entities.app.MembershipAppEntity;
import edu.nd.crc.safa.features.organizations.entities.app.OrganizationAppEntity;
import edu.nd.crc.safa.features.organizations.entities.app.TeamAppEntity;
import edu.nd.crc.safa.features.organizations.entities.db.Organization;
import edu.nd.crc.safa.features.organizations.entities.db.OrganizationRole;
import edu.nd.crc.safa.features.organizations.entities.db.Team;
import edu.nd.crc.safa.features.organizations.repositories.OrganizationRepository;
import edu.nd.crc.safa.features.permissions.entities.OrganizationPermission;
import edu.nd.crc.safa.features.permissions.entities.Permission;
import edu.nd.crc.safa.features.permissions.entities.TeamPermission;
import edu.nd.crc.safa.features.permissions.services.PermissionService;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.app.SafaItemNotFoundError;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@AllArgsConstructor
public class OrganizationService {

    private final OrganizationRepository organizationRepo;
    private final TeamService teamService;
    private final OrganizationMembershipService organizationMembershipService;
    private final PermissionService permissionService;
    private final BillingService billingService;

    /**
     * Create a new organization. This will also create a new team for the organization.
     *
     * @param organization The new organization data structure.
     * @return The newly created organization
     */
    public Organization createNewOrganization(Organization organization) {
        assertNull(organization.getId(), "Cannot create a new organization with a specified ID");
        assertRequiredFields(organization);

        organization = organizationRepo.save(organization);  // Save once so it gets an id

        Team orgTeam = teamService.createNewTeam(organization.getName(), organization, true, organization.getOwner());
        organization.setFullOrgTeamId(orgTeam.getId());
        organization = organizationRepo.save(organization);  // Save again to add the team ID

        organizationMembershipService.addUserRole(organization.getOwner(), organization, OrganizationRole.ADMIN);

        return organization;
    }

    /**
     * Update an organization entry in the database.
     *
     * @param organization The new entry
     * @return The updated entry
     */
    public Organization updateOrganization(Organization organization) {
        assertNotNull(organization.getId(), "Missing organization ID");
        assertRequiredFields(organization);

        return organizationRepo.save(organization);
    }

    /**
     * Assert that all fields that are necessary for the database are included.
     *
     * @param organization The object to check
     */
    private void assertRequiredFields(Organization organization) {
        assertNotNull(organization.getName(), "Missing organization name.");
        assertNotNull(organization.getDescription(), "Missing organization description");
        assertNotNull(organization.getOwner(), "Missing organization owner.");
        assertNotNull(organization.getPaymentTier(), "Missing organization payment tier");
    }

    /**
     * Gets the personal organization representing a given user
     *
     * @param user The user
     * @return The personal org for that user
     */
    public Organization getPersonalOrganization(SafaUser user) {
        UUID orgId = user.getPersonalOrgId();
        return organizationRepo.findById(orgId)
                .orElseThrow(() -> new SafaError("User does not have a personal organization"));
    }

    /**
     * Gets an organization by its ID.
     *
     * @param id Org ID
     * @return The org
     */
    public Organization getOrganizationById(UUID id) {
        return getOrganizationOptionalById(id)
            .orElseThrow(() -> new SafaItemNotFoundError("No organization with the given ID found"));
    }

    /**
     * Gets an organization by its ID. Returns an optional in case the org isn't found
     *
     * @param id Org ID
     * @return The org
     */
    public Optional<Organization> getOrganizationOptionalById(UUID id) {
        return organizationRepo.findById(id);
    }

    /**
     * Converts an {@link Organization} to its front-end representation.
     *
     * @param organization The organization
     * @param currentUser The user making the request (so that we can properly show permissions)
     * @return The organization front-end object
     */
    public OrganizationAppEntity getAppEntity(Organization organization, SafaUser currentUser) {
        List<IEntityMembership> memberships =
            organizationMembershipService.getMembershipsForEntity(organization);

        List<MembershipAppEntity> membershipAppEntities =
            memberships
                .stream()
                .map(MembershipAppEntity::new)
                .toList();

        List<String> permissions = getUserPermissions(organization, currentUser)
            .stream()
            .filter(permission -> permission instanceof OrganizationPermission)
            .map(Permission::getName)
            .toList();

        List<Team> teams = teamService.getAllTeamsByOrganization(organization)
            .stream()
            .filter(team ->
                permissionService.hasAnyPermission(
                    Set.of(OrganizationPermission.VIEW_TEAMS, TeamPermission.VIEW),
                    team,
                    currentUser
                )
            )
            .toList();


        List<TeamAppEntity> teamAppEntities = teamService.getAppEntities(teams, currentUser);

        BillingInfo billingInfo = billingService.getBillingInfoForOrg(organization);
        MonthlyUsage monthlyUsage = billingService.getMonthlyUsageForOrg(organization);

        return new OrganizationAppEntity(organization, membershipAppEntities, teamAppEntities,
            permissions, billingInfo, monthlyUsage);
    }

    /**
     * Converts a collection of organizations to front-end objects.
     *
     * @param organizations The organizations.
     * @param currentUser The user making the request (so that we can properly show permissions)
     * @return The front-end representations of the given objects.
     */
    public List<OrganizationAppEntity> getAppEntities(Collection<Organization> organizations, SafaUser currentUser) {
        return organizations.stream()
            .map(org -> getAppEntity(org, currentUser))
            .toList();
    }

    /**
     * Get all permissions granted to the user via their membership(s) within the given organization.
     *
     * @param organization The organization the user is a part of.
     * @param currentUser The user in question
     * @return A list of permissions the user has from the organization
     */
    public List<Permission> getUserPermissions(Organization organization, SafaUser currentUser) {
        return organizationMembershipService.getRolesForUser(currentUser, organization)
            .stream()
            .flatMap(role -> role.getGrants().stream())
            .toList();
    }

    /**
     * Delete an organization.
     *
     * @param organization The org to delete.
     */
    public void deleteOrganization(Organization organization) {
        organizationRepo.delete(organization);
    }
}
