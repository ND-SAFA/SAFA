package edu.nd.crc.safa.features.organizations.services;

import java.util.Collection;
import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.memberships.entities.db.OrganizationMembership;
import edu.nd.crc.safa.features.memberships.services.OrganizationMembershipService;
import edu.nd.crc.safa.features.memberships.services.TeamMembershipService;
import edu.nd.crc.safa.features.organizations.entities.app.MembershipAppEntity;
import edu.nd.crc.safa.features.organizations.entities.app.OrganizationAppEntity;
import edu.nd.crc.safa.features.organizations.entities.app.TeamAppEntity;
import edu.nd.crc.safa.features.organizations.entities.db.Organization;
import edu.nd.crc.safa.features.organizations.entities.db.OrganizationRole;
import edu.nd.crc.safa.features.organizations.entities.db.Team;
import edu.nd.crc.safa.features.organizations.entities.db.TeamRole;
import edu.nd.crc.safa.features.organizations.repositories.OrganizationRepository;
import edu.nd.crc.safa.features.permissions.entities.OrganizationPermission;
import edu.nd.crc.safa.features.permissions.entities.Permission;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@AllArgsConstructor
public class OrganizationService {

    private final OrganizationRepository organizationRepo;
    private final TeamService teamService;
    private final TeamMembershipService teamMembershipService;
    private final OrganizationMembershipService organizationMembershipService;

    /**
     * Create a new organization. This will also create a new team for the organization.
     *
     * @param organization The new organization data structure.
     * @return The newly created organization
     */
    public Organization createNewOrganization(Organization organization) {
        if (organization.getId() != null) {
            throw new IllegalArgumentException("Cannot create a new organization with an ID");
        }

        organization = organizationRepo.save(organization);  // Save once so it gets an id

        Team orgTeam = teamService.createNewTeam(organization.getName(), organization, true);
        organization.setFullOrgTeamId(orgTeam.getId());
        organization = organizationRepo.save(organization);  // Save again to add the team ID

        teamMembershipService.addUserRole(organization.getOwner(), orgTeam, TeamRole.ADMIN);
        organizationMembershipService.addUserRole(organization.getOwner(), organization, OrganizationRole.ADMIN);

        return organization;
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
     * Converts an {@link Organization} to its front-end representation.
     *
     * @param organization The organization
     * @param currentUser The user making the request (so that we can properly show permissions)
     * @return The organization front-end object
     */
    public OrganizationAppEntity getAppEntity(Organization organization, SafaUser currentUser) {
        List<OrganizationMembership> memberships =
            organizationMembershipService.getAllMembershipsByOrganization(organization);

        List<MembershipAppEntity> membershipAppEntities =
            memberships
                .stream()
                .map(MembershipAppEntity::new)
                .collect(Collectors.toUnmodifiableList());

        List<String> permissions = getUserPermissions(organization, currentUser)
            .stream()
            .filter(permission -> permission instanceof OrganizationPermission)
            .map(Permission::getName)
            .collect(Collectors.toUnmodifiableList());

        List<TeamAppEntity> teams =
            teamService.getAppEntities(teamService.getAllTeamsByOrganization(organization), currentUser);

        return new OrganizationAppEntity(organization, membershipAppEntities, teams, permissions);
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
            .collect(Collectors.toUnmodifiableList());
    }

    /**
     * Get all permissions granted to the user via their membership(s) within the given organization.
     *
     * @param organization The organization the user is a part of.
     * @param currentUser The user in question
     * @return A list of permissions the user has from the organization
     */
    public List<Permission> getUserPermissions(Organization organization, SafaUser currentUser) {
        return organizationMembershipService.getUserRoles(currentUser, organization)
            .stream()
            .flatMap(role -> role.getGrants().stream())
            .collect(Collectors.toUnmodifiableList());
    }
}
