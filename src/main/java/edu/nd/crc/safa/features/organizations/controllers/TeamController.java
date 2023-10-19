package edu.nd.crc.safa.features.organizations.controllers;

import static edu.nd.crc.safa.utilities.AssertUtils.assertEqual;
import static edu.nd.crc.safa.utilities.AssertUtils.assertNotNull;

import java.util.List;
import java.util.Set;
import java.util.UUID;
import java.util.stream.Collectors;

import edu.nd.crc.safa.authentication.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.organizations.entities.app.TeamAppEntity;
import edu.nd.crc.safa.features.organizations.entities.db.Organization;
import edu.nd.crc.safa.features.organizations.entities.db.Team;
import edu.nd.crc.safa.features.organizations.services.OrganizationService;
import edu.nd.crc.safa.features.organizations.services.TeamService;
import edu.nd.crc.safa.features.permissions.entities.OrganizationPermission;
import edu.nd.crc.safa.features.permissions.entities.TeamPermission;
import edu.nd.crc.safa.features.permissions.services.PermissionService;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class TeamController extends BaseController {

    private final OrganizationService organizationService;
    private final TeamService teamService;
    private final PermissionService permissionService;

    public TeamController(ResourceBuilder resourceBuilder, ServiceProvider serviceProvider,
                          OrganizationService organizationService, TeamService teamService,
                          PermissionService permissionService) {
        super(resourceBuilder, serviceProvider);
        this.organizationService = organizationService;
        this.teamService = teamService;
        this.permissionService = permissionService;
    }

    /**
     * Get all teams within an organization.
     *
     * @param orgId The ID of the organization the teams are in.
     * @return The list of teams within the org.
     */
    @GetMapping(AppRoutes.Organizations.Teams.ROOT)
    public List<TeamAppEntity> getOrganizationTeams(@PathVariable UUID orgId) {
        SafaUser user = getCurrentUser();
        Organization organization = organizationService.getOrganizationById(orgId);
        List<Team> orgTeams = teamService.getAllTeamsByOrganization(organization)
            .stream()
            .filter(team ->
                permissionService.hasAnyPermission(
                    Set.of(OrganizationPermission.VIEW_TEAMS, TeamPermission.VIEW),
                    team,
                    user
                )
            )
            .collect(Collectors.toUnmodifiableList());

        return teamService.getAppEntities(orgTeams, getCurrentUser());
    }

    /**
     * Get the team that represents the entire organization. This team exists so
     * that, from a user perspective, it is possible to have a project owned by/shared with
     * and entire organization, while still only allowing projects to be owned by/shared with
     * teams.
     *
     * @param orgId The ID of the organization in question
     * @return The organization's full-org team
     */
    @GetMapping(AppRoutes.Organizations.Teams.SELF)
    public TeamAppEntity getFullOrgTeam(@PathVariable UUID orgId) {
        SafaUser user = getCurrentUser();
        Organization organization = organizationService.getOrganizationById(orgId);
        Team orgTeam = teamService.getFullOrganizationTeam(organization);
        permissionService.requireAnyPermission(
            Set.of(OrganizationPermission.VIEW_TEAMS, TeamPermission.VIEW), orgTeam, user);
        return teamService.getAppEntity(orgTeam, user);
    }

    /**
     * Get a team by its team ID.
     *
     * @param orgId The ID of the org the team is in
     * @param teamId The ID of the team
     * @return The team, if it is found
     */
    @GetMapping(AppRoutes.Organizations.Teams.BY_ID)
    public TeamAppEntity getTeam(@PathVariable UUID orgId, @PathVariable UUID teamId) {
        SafaUser user = getCurrentUser();
        Team team = teamService.getTeamById(teamId);
        assertEqual(team.getOrganization().getId(), orgId, "No team with the specified ID found under this org");
        permissionService.requireAnyPermission(
            Set.of(OrganizationPermission.VIEW_TEAMS, TeamPermission.VIEW), team, user);
        return teamService.getAppEntity(team, getCurrentUser());
    }

    /**
     * Create a new team within the organization with the given ID.
     *
     * @param orgId The ID of the organization that will contain the team.
     * @param teamAppEntity The definition of the team to create. Only the name is read.
     * @return The newly created team.
     */
    @PostMapping(AppRoutes.Organizations.Teams.ROOT)
    public TeamAppEntity createTeam(@PathVariable UUID orgId, @RequestBody TeamAppEntity teamAppEntity) {
        SafaUser user = getCurrentUser();
        Organization organization = getResourceBuilder()
            .fetchOrganization(orgId)
            .withPermission(OrganizationPermission.CREATE_TEAMS, user)
            .get();
        assertNotNull(teamAppEntity.getName(), "Missing team name.");
        Team newTeam = teamService.createNewTeam(teamAppEntity.getName(), organization, false, user);
        return teamService.getAppEntity(newTeam, user);
    }

    /**
     * Modify values within a team. Only the name of the team can be changed.
     *
     * @param orgId The ID of the org the team is in
     * @param teamId The ID of the team to modify
     * @param teamAppEntity The new values to set on the team
     * @return The updated team entity
     */
    @PutMapping(AppRoutes.Organizations.Teams.BY_ID)
    public TeamAppEntity modifyTeam(@PathVariable UUID orgId, @PathVariable UUID teamId,
                                    @RequestBody TeamAppEntity teamAppEntity) {
        Team team = getResourceBuilder()
            .fetchTeam(teamId)
            .withPermission(TeamPermission.EDIT, getCurrentUser())
            .get();
        assertEqual(team.getOrganization().getId(), orgId, "No team with the specified ID found under this org");
        team.setFromAppEntity(teamAppEntity);
        team = teamService.updateTeam(team);
        return teamService.getAppEntity(team, getCurrentUser());
    }

    /**
     * Delete a team.
     *
     * @param orgId The ID of the org the team is in
     * @param teamId The ID of the team to delete
     */
    @DeleteMapping(AppRoutes.Organizations.Teams.BY_ID)
    public void deleteTeam(@PathVariable UUID orgId, @PathVariable UUID teamId) {
        Team team = teamService.getTeamById(teamId);
        assertEqual(team.getOrganization().getId(), orgId, "No team with the specified ID found under this org");

        permissionService.requireAnyPermission(
            Set.of(OrganizationPermission.DELETE_TEAMS, TeamPermission.DELETE),
            team,
            getCurrentUser()
        );

        teamService.deleteTeam(team);
    }
}
