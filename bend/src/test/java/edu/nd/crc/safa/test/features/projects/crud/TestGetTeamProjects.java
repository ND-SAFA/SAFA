package edu.nd.crc.safa.test.features.projects.crud;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import java.util.List;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.organizations.entities.db.Organization;
import edu.nd.crc.safa.features.organizations.entities.db.Team;
import edu.nd.crc.safa.features.projects.entities.app.ProjectIdAppEntity;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;
import edu.nd.crc.safa.test.requests.SafaRequest;

import com.fasterxml.jackson.core.type.TypeReference;
import org.junit.jupiter.api.Test;

public class TestGetTeamProjects extends ApplicationBaseTest {

    @Test
    public void testGetTeamProjects() throws Exception {
        List<String> projects = List.of("project1", "project2", "project3");

        Organization organization = dbEntityBuilder.newOrganization("Org", "org");
        Team team = dbEntityBuilder.newTeam("team", organization);

        for (String projectName : projects) {
            dbEntityBuilder.newProject(projectName, team);
        }

        dbEntityBuilder.newProject("other project", getCurrentUser());

        List<ProjectIdAppEntity> projectDescriptors =
            SafaRequest.withRoute(AppRoutes.Projects.Membership.GET_TEAM_PROJECTS)
                .withTeamId(team.getId())
                .getAsType(new TypeReference<>(){});

        assertThat(projectDescriptors.size()).isEqualTo(3);

        for (String projectName : projects) {
            assertThat(projectDescriptors.stream().anyMatch(p -> p.getName().equals(projectName))).isTrue();
        }
    }
}
