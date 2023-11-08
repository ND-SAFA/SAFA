package edu.nd.crc.safa.features.organizations.services;

import static edu.nd.crc.safa.utilities.AssertUtils.assertNotNull;

import java.util.Collection;
import java.util.List;
import java.util.Optional;
import java.util.UUID;
import java.util.stream.Collectors;
import java.util.stream.Stream;

import edu.nd.crc.safa.features.memberships.entities.db.IEntityMembership;
import edu.nd.crc.safa.features.memberships.services.TeamMembershipService;
import edu.nd.crc.safa.features.organizations.entities.app.MembershipAppEntity;
import edu.nd.crc.safa.features.organizations.entities.app.TeamAppEntity;
import edu.nd.crc.safa.features.organizations.entities.db.Organization;
import edu.nd.crc.safa.features.organizations.entities.db.Team;
import edu.nd.crc.safa.features.organizations.entities.db.TeamRole;
import edu.nd.crc.safa.features.organizations.repositories.TeamRepository;
import edu.nd.crc.safa.features.permissions.entities.Permission;
import edu.nd.crc.safa.features.permissions.entities.TeamPermission;
import edu.nd.crc.safa.features.projects.entities.app.ProjectIdAppEntity;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.app.SafaItemNotFoundError;
import edu.nd.crc.safa.features.projects.services.ProjectService;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import lombok.Setter;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Lazy;
import org.springframework.stereotype.Service;

@Service
public class TeamService {
    @Setter(onMethod = @__({@Autowired, @Lazy}))
    private TeamRepository teamRepo;
    @Setter(onMethod = @__({@Autowired, @Lazy}))
    private OrganizationService orgService;
    @Setter(onMethod = @__({@Autowired, @Lazy}))
    private TeamMembershipService teamMembershipService;
    @Setter(onMethod = @__({@Autowired, @Lazy}))
    private ProjectService projectService;

    /**
     * Create a new team.
     *
     * @param name         The name of the team
     * @param organization The organization the team belongs to
     * @param fullOrgTeam  Whether the team is a full organization team
     * @param user         The user creating the team. This user will be given the admin role initially
     * @return The newly created team
     */
    public Team createNewTeam(String name, Organization organization, boolean fullOrgTeam, SafaUser user) {
        Team team = new Team(name, organization, fullOrgTeam);
        team = teamRepo.save(team);
        teamMembershipService.addUserRole(user, team, TeamRole.ADMIN);
        return team;
    }

    /**
     * Gets the team associated with the user's personal org
     *
     * @param user The user
     * @return The user's personal team
     */
    public Team getPersonalTeam(SafaUser user) {
        Organization personalOrg = orgService.getPersonalOrganization(user);
        return getFullOrganizationTeam(personalOrg);
    }

    /**
     * Gets the team that contains the entire organization
     *
     * @param organization The organization
     * @return The full organization team
     */
    public Team getFullOrganizationTeam(Organization organization) {
        UUID teamId = organization.getFullOrgTeamId();
        return teamRepo.findById(teamId).orElseThrow(() -> new SafaError("Organization does not have an org team"));
    }

    /**
     * Get all teams within an organization.
     *
     * @param organization The organization
     * @return The teams that are a part of the organization
     */
    public List<Team> getAllTeamsByOrganization(Organization organization) {
        return teamRepo.findByOrganization(organization);
    }

    /**
     * Convert a team to its front-end representation
     *
     * @param team        The team
     * @param currentUser The user making the request (so that we can properly show permissions)
     * @return The team front-end object
     */
    public TeamAppEntity getAppEntity(Team team, SafaUser currentUser) {
        List<IEntityMembership> teamMemberships = teamMembershipService.getMembershipsForEntity(team);

        List<MembershipAppEntity> teamMembershipAppEntities =
            teamMemberships
                .stream()
                .map(MembershipAppEntity::new)
                .collect(Collectors.toUnmodifiableList());

        List<ProjectIdAppEntity> projects = projectService.getIdAppEntities(
            projectService.getProjectsOwnedByTeam(team), currentUser);

        List<String> permissions = getUserPermissions(team, currentUser)
            .stream()
            .filter(permission -> permission instanceof TeamPermission)
            .map(Permission::getName)
            .collect(Collectors.toUnmodifiableList());

        return new TeamAppEntity(team, teamMembershipAppEntities, projects, permissions);
    }

    /**
     * Converts a collection of teams to front-end objects
     *
     * @param teams       The teams
     * @param currentUser The user making the request (so that we can properly show permissions)
     * @return The front-end representations of the teams
     */
    public List<TeamAppEntity> getAppEntities(Collection<Team> teams, SafaUser currentUser) {
        return teams.stream()
            .map(team -> getAppEntity(team, currentUser))
            .collect(Collectors.toUnmodifiableList());
    }

    /**
     * Get all permissions granted to the user via their membership(s) within the given team.
     *
     * @param team        The team the user is a part of. If the user is not actually a member of this team, the
     *                    function may still return some permissions based on if the user is a member of the
     *                    organization the team is a part of, but it will not grant the user any permissions they
     *                    should not have.
     * @param currentUser The user in question
     * @return A list of permissions the user has from the team
     */
    public List<Permission> getUserPermissions(Team team, SafaUser currentUser) {

        Stream<Permission> teamPermissions = teamMembershipService.getRolesForUser(currentUser, team)
            .stream()
            .flatMap(role -> role.getGrants().stream());

        Stream<Permission> orgPermissions = orgService.getUserPermissions(team.getOrganization(), currentUser).stream();

        return Stream.concat(teamPermissions, orgPermissions).collect(Collectors.toUnmodifiableList());
    }

    /**
     * Get a team by its team ID.
     *
     * @param teamId The ID of the team.
     * @return The team with the given ID, if it exists.
     * @throws SafaItemNotFoundError if the team is not found.
     */
    public Team getTeamById(UUID teamId) {
        return getTeamOptionalById(teamId)
            .orElseThrow(() -> new SafaItemNotFoundError("No team with the given ID found."));
    }

    /**
     * Get a team by its team ID.
     *
     * @param teamId The ID of the team.
     * @return The team with the given ID, if it exists.
     */
    public Optional<Team> getTeamOptionalById(UUID teamId) {
        return teamRepo.findById(teamId);
    }

    /**
     * Update a team entry in the database.
     *
     * @param team The new entry
     * @return The updated entry
     */
    public Team updateTeam(Team team) {
        assertNotNull(team.getId(), "Missing team ID");
        assertNotNull(team.getName(), "Missing team name.");
        assertNotNull(team.getOrganization(), "Missing team organization.");

        return teamRepo.save(team);
    }

    /**
     * Delete a team from the database.
     *
     * @param team The team to delete
     */
    public void deleteTeam(Team team) {
        teamRepo.delete(team);
    }
}
