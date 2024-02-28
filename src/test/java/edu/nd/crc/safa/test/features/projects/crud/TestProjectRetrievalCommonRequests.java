package edu.nd.crc.safa.test.features.projects.crud;

import static org.assertj.core.api.Assertions.assertThat;
import static org.junit.jupiter.api.Assertions.fail;

import java.util.List;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.organizations.entities.app.MembershipAppEntity;
import edu.nd.crc.safa.features.organizations.entities.app.MembershipType;
import edu.nd.crc.safa.features.organizations.entities.db.Organization;
import edu.nd.crc.safa.features.organizations.entities.db.ProjectRole;
import edu.nd.crc.safa.features.organizations.entities.db.Team;
import edu.nd.crc.safa.features.organizations.entities.db.TeamRole;
import edu.nd.crc.safa.features.projects.entities.app.ProjectIdAppEntity;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;
import edu.nd.crc.safa.test.requests.SafaRequest;

import com.fasterxml.jackson.core.type.TypeReference;
import org.json.JSONArray;
import org.junit.jupiter.api.Test;

/**
 * Tests that projects defined in database are able to be retrieved by user.
 */
class TestProjectRetrievalCommonRequests extends ApplicationBaseTest {
    @Test
    void retrieveNoProjects() throws Exception {
        JSONArray response = SafaRequest
            .withRoute(AppRoutes.Projects.GET_PROJECTS)
            .getWithJsonArray();
        assertThat(response.length()).isZero();
    }

    /**
     * Tests that a user is able to retrieve all the projects they own.
     *
     * @throws Exception Throws exception if http fails when sending get request.
     */
    @Test
    void retrieveMultipleProjects() throws Exception {
        SafaUser otherUser = safaUserService.createUser("doesNotExist@gmail.com", "somePassword");

        dbEntityBuilder
            .newProject("firstProject")
            .newProject("secondProject")
            .newProject("other project", otherUser);
        JSONArray response = SafaRequest.withRoute(AppRoutes.Projects.GET_PROJECTS).getWithJsonArray();
        assertThat(response.length()).isEqualTo(2); // firstProject, secondProject
    }

    @Test
    void testRetrievedProjectMemberships() throws Exception {
        SafaUser otherUser = safaUserService.createUser("doesNotExist@gmail.com", "somePassword");
        Organization org = dbEntityBuilder.newOrganization("test org", "test desc");
        Team team = dbEntityBuilder.newTeam("test team", org);
        Project project = dbEntityBuilder.newProjectWithReturn("test project", team);

        dbEntityBuilder.createMembership(team, getCurrentUser(), TeamRole.ADMIN)
            .createMembership(project, otherUser, ProjectRole.VIEWER);

        List<ProjectIdAppEntity> projects =
            SafaRequest.withRoute(AppRoutes.Projects.GET_PROJECTS).getAsType(new TypeReference<>(){});
        assertThat(projects.size()).isEqualTo(1);

        ProjectIdAppEntity returnedProject = projects.get(0);
        List<MembershipAppEntity> memberships = returnedProject.getMembers();
        assertThat(memberships.size()).isEqualTo(2);

        for (MembershipAppEntity membership : memberships) {

            if (membership.getEmail().equals(getCurrentUser().getEmail())) {

                assertThat(membership.getEntityType()).isEqualTo(MembershipType.TEAM);
                assertThat(membership.getRole()).isEqualTo(TeamRole.ADMIN.name());
                assertThat(membership.getEntityId()).isEqualTo(team.getId());

            } else if (membership.getEmail().equals(otherUser.getEmail())) {

                assertThat(membership.getEntityType()).isEqualTo(MembershipType.PROJECT);
                assertThat(membership.getRole()).isEqualTo(ProjectRole.VIEWER.name());
                assertThat(membership.getEntityId()).isEqualTo(project.getId());

            } else {
                fail("Unknown member: " + membership.getEmail());
            }
        }
    }
}
