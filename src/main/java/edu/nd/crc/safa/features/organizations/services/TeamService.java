package edu.nd.crc.safa.features.organizations.services;

import java.util.Collection;
import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.memberships.entities.db.TeamMembership;
import edu.nd.crc.safa.features.memberships.services.TeamMembershipService;
import edu.nd.crc.safa.features.organizations.entities.app.MembershipAppEntity;
import edu.nd.crc.safa.features.organizations.entities.app.TeamAppEntity;
import edu.nd.crc.safa.features.organizations.entities.db.Organization;
import edu.nd.crc.safa.features.organizations.entities.db.Team;
import edu.nd.crc.safa.features.organizations.repositories.TeamRepository;
import edu.nd.crc.safa.features.permissions.entities.Permission;
import edu.nd.crc.safa.features.projects.entities.app.ProjectIdAppEntity;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.services.ProjectService;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import lombok.Setter;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Lazy;
import org.springframework.stereotype.Service;

@Service
public class TeamService {

    @Setter(onMethod = @__({@Autowired}))
    private TeamRepository teamRepo;

    @Setter(onMethod = @__({@Autowired, @Lazy}))
    private OrganizationService orgService;

    @Setter(onMethod = @__({@Autowired}))
    private TeamMembershipService teamMembershipService;

    @Setter(onMethod = @__({@Autowired}))
    private ProjectService projectService;

    /**
     * Create a new team.
     *
     * @param name The name of the team
     * @param organization The organization the team belongs to
     * @param fullOrgTeam Whether the team is a full organization team
     * @return The newly created team
     */
    public Team createNewTeam(String name, Organization organization, boolean fullOrgTeam) {
        Team team = new Team(name, organization, fullOrgTeam);
        return teamRepo.save(team);
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
     * @param team The team
     * @param currentUser The user making the request (so that we can properly show permissions)
     * @return The team front-end object
     */
    public TeamAppEntity getAppEntity(Team team, SafaUser currentUser) {
        List<TeamMembership> teamMemberships = teamMembershipService.getTeamMemberships(team);
        List<MembershipAppEntity> teamMembershipAppEntities =
            teamMemberships
                .stream()
                .map(MembershipAppEntity::new)
                .collect(Collectors.toUnmodifiableList());

        List<ProjectIdAppEntity> projects = projectService.getIdAppEntities(
            projectService.getProjectsOwnedByTeam(team), currentUser);

        List<String> permissions = getUserPermissions(teamMemberships, currentUser);

        return new TeamAppEntity(team, teamMembershipAppEntities, projects, permissions);
    }

    /**
     * Converts a collection of teams to front-end objects
     *
     * @param teams The teams
     * @param currentUser The user making the request (so that we can properly show permissions)
     * @return The front-end representations of the teams
     */
    public List<TeamAppEntity> getAppEntities(Collection<Team> teams, SafaUser currentUser) {
        return teams.stream()
            .map(team -> getAppEntity(team, currentUser))
            .collect(Collectors.toUnmodifiableList());
    }

    /**
     * Get all permissions granted to a user based on a list of team memberships. This function
     * just filters the list of memberships for ones that match the given user, extracts the corresponding roles,
     * and then returns the permissions associated with those roles.
     *
     * @param memberships The list of all memberships within a team
     * @param currentUser The user in question
     * @return All team-related permissions granted to the user
     */
    private List<String> getUserPermissions(List<TeamMembership> memberships, SafaUser currentUser) {
        return memberships.stream()
            .filter(membership -> membership.getUser().getUserId().equals(currentUser.getUserId()))
            .map(TeamMembership::getRole)
            .flatMap(role -> role.getGrants().stream())
            .map(Permission::getName)
            .collect(Collectors.toUnmodifiableList());
    }
}
