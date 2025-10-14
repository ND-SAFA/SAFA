package edu.nd.crc.safa.test.features.projects;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.List;
import java.util.Set;
import java.util.UUID;
import java.util.function.Function;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.memberships.services.TeamMembershipService;
import edu.nd.crc.safa.features.organizations.entities.db.Team;
import edu.nd.crc.safa.features.organizations.entities.db.TeamRole;
import edu.nd.crc.safa.features.organizations.services.TeamService;
import edu.nd.crc.safa.features.permissions.entities.Permission;
import edu.nd.crc.safa.features.permissions.entities.ProjectPermission;
import edu.nd.crc.safa.features.projects.controllers.ProjectController;
import edu.nd.crc.safa.features.projects.entities.app.ProjectIdAppEntity;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.projects.services.ProjectService;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.users.services.SafaUserService;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;
import edu.nd.crc.safa.test.services.requests.CommonProjectRequests;

import org.json.JSONArray;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;

public class TestProjectOwnershipTransfer extends ApplicationBaseTest {

    @Autowired
    private SafaUserService safaUserService;

    @Autowired
    private TeamService teamService;

    @Autowired
    private TeamMembershipService teamMembershipService;

    @Autowired
    private ProjectService projectService;

    private final String otherUserUsername = "test@test.test";
    private UUID projectId;

    @Test
    public void testTransferToTeam() throws Exception {
        transferShouldSucceed(this::createTransferDetailsForTeam);
    }

    @Test
    public void testTransferToOrganization() throws Exception {
        transferShouldSucceed(this::createTransferDetailsForOrganization);
    }

    @Test
    public void testTransferToUserEmail() throws Exception {
        transferShouldSucceed(this::createTransferDetailsForUserEmail);
    }

    @Test
    public void testTransferToUserId() throws Exception {
        transferShouldSucceed(this::createTransferDetailsForUserId);
    }

    private void transferShouldSucceed(Function<Team, ProjectController.TransferOwnershipDTO> transferDetailsProvider) {
        Project project = createProject();
        SafaUser otherUser = createOtherUser();
        Team otherUserTeam = teamService.getPersonalTeam(otherUser);
        giveCurrentUserRoleInTeam(otherUserTeam, TeamRole.ADMIN);

        ProjectController.TransferOwnershipDTO transferDetails = transferDetailsProvider.apply(otherUserTeam);

        ProjectIdAppEntity response = CommonProjectRequests.transferProjectOwnership(project, transferDetails);

        assertThat(response).isNotNull();
        assertThat(response.getProjectId()).isEqualTo(project.getId().toString());
        assertThat(response.getOwner()).isEqualTo(otherUserTeam.getId().toString());
    }

    @Test
    public void testMissingProjectMovePermission() {
        // We can get the move permission failure by transferring it once and then trying to do it again
        // after making ourselves a viewer. Since we don't own the project anymore we won't have permission to move it

        transferShouldSucceed(this::createTransferDetailsForTeam);

        assertThat(projectId).isNotNull();
        Project project = projectService.getProjectById(projectId);
        Team otherUserTeam = teamService.getPersonalTeam(getOtherUser());

        clearCurrentUserRolesInTeam(otherUserTeam);
        giveCurrentUserRoleInTeam(otherUserTeam, TeamRole.VIEWER);

        Team currentUserTeam = teamService.getPersonalTeam(getCurrentUser());
        ProjectController.TransferOwnershipDTO transferDetails = createTransferDetailsForTeam(currentUserTeam);

        JSONObject response = CommonProjectRequests.transferProjectOwnership(project, transferDetails, status().is4xxClientError());
        assertMissingPermissions(response);
    }

    @Test
    public void testMissingProjectViewPermission() {
        // We can get the move permission failure by transferring it once and then trying to do it again
        // after making ourselves not admin. Since we don't own the project anymore and have no role in the team
        // we won't have permission to view the project at all

        transferShouldSucceed(this::createTransferDetailsForTeam);

        assertThat(projectId).isNotNull();
        Project project = projectService.getProjectById(projectId);
        Team otherUserTeam = teamService.getPersonalTeam(getOtherUser());

        clearCurrentUserRolesInTeam(otherUserTeam);

        Team currentUserTeam = teamService.getPersonalTeam(getCurrentUser());
        ProjectController.TransferOwnershipDTO transferDetails = createTransferDetailsForTeam(currentUserTeam);

        JSONObject response = CommonProjectRequests.transferProjectOwnership(project, transferDetails, status().is4xxClientError());
        assertMissingPermissions(response);
    }

    private void assertMissingPermissions(JSONObject missingPermissionResponse) {
        Set<Permission> permissions = Set.of(ProjectPermission.MOVE, ProjectPermission.VIEW);

        assertThat(missingPermissionResponse).isNotNull();
        assertThat(missingPermissionResponse.has("permissions")).isTrue();

        JSONArray missingPermissions = missingPermissionResponse.getJSONArray("permissions");
        List<Object> missingPermissionsList = missingPermissions.toList();
        assertThat(missingPermissionsList.size()).isEqualTo(permissions.size());

        Set<String> missingPermissionsSet = missingPermissionsList.stream().map(Object::toString).collect(Collectors.toSet());
        Set<String> expectedMissingPermissionsSet = permissions.stream().map(Permission::getName).collect(Collectors.toSet());
        assertThat(missingPermissionsSet).isEqualTo(expectedMissingPermissionsSet);
    }

    private Project createProject() {
        Project project = creationService.createProjectWithNewVersion("Test project").getProject();
        this.projectId = project.getProjectId();
        return project;
    }

    private void giveCurrentUserRoleInTeam(Team otherUserTeam, TeamRole teamRole) {
        teamMembershipService.addUserRole(getCurrentUser(), otherUserTeam, teamRole);
    }

    private void clearCurrentUserRolesInTeam(Team otherUserTeam) {
        teamMembershipService.getRolesForUser(getCurrentUser(), otherUserTeam)
            .forEach(role -> teamMembershipService.removeUserRole(getCurrentUser(), otherUserTeam, role));
    }

    private SafaUser createOtherUser() {
        return safaUserService.createUser(otherUserUsername, "test password");
    }

    private SafaUser getOtherUser() {
        return safaUserService.getUserByEmail(otherUserUsername);
    }

    private ProjectController.TransferOwnershipDTO createTransferDetailsForTeam(Team otherUserTeam) {
        ProjectController.TransferOwnershipDTO transferDetails = new ProjectController.TransferOwnershipDTO();
        transferDetails.setOwner(otherUserTeam.getId().toString());
        transferDetails.setOwnerType(ProjectController.OwnerType.TEAM);
        return transferDetails;
    }

    private ProjectController.TransferOwnershipDTO createTransferDetailsForOrganization(Team otherUserTeam) {
        ProjectController.TransferOwnershipDTO transferDetails = new ProjectController.TransferOwnershipDTO();
        transferDetails.setOwner(otherUserTeam.getOrganization().getId().toString());
        transferDetails.setOwnerType(ProjectController.OwnerType.ORGANIZATION);
        return transferDetails;
    }

    private ProjectController.TransferOwnershipDTO createTransferDetailsForUserEmail(Team otherUserTeam) {
        ProjectController.TransferOwnershipDTO transferDetails = new ProjectController.TransferOwnershipDTO();
        transferDetails.setOwner(otherUserTeam.getOrganization().getOwner().getEmail());
        transferDetails.setOwnerType(ProjectController.OwnerType.USER_EMAIL);
        return transferDetails;
    }

    private ProjectController.TransferOwnershipDTO createTransferDetailsForUserId(Team otherUserTeam) {
        ProjectController.TransferOwnershipDTO transferDetails = new ProjectController.TransferOwnershipDTO();
        transferDetails.setOwner(otherUserTeam.getOrganization().getOwner().getUserId().toString());
        transferDetails.setOwnerType(ProjectController.OwnerType.USER_ID);
        return transferDetails;
    }
}
