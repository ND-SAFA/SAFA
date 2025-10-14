package edu.nd.crc.safa.test.features.projects.crud;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import java.util.UUID;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.organizations.entities.db.Organization;
import edu.nd.crc.safa.features.organizations.entities.db.Team;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.projects.services.ProjectService;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;
import edu.nd.crc.safa.test.requests.SafaRequest;

import com.fasterxml.jackson.core.type.TypeReference;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;

public class TestProjectCreation extends ApplicationBaseTest {

    private static final String PROJECT_NAME = "Test Project Name";

    private UUID teamId;
    private UUID orgId;
    private ProjectAppEntity projectDefinition;

    @Autowired
    private ProjectService projectService;

    @BeforeEach
    public void setUpProjectDefinition() {
        Organization newOrg = dbEntityBuilder.newOrganization("org name", "org desc");
        Team newTeam = dbEntityBuilder.newTeam("team name", newOrg);

        teamId = newTeam.getId();
        orgId = newOrg.getId();

        projectDefinition = new ProjectAppEntity();
        projectDefinition.setName(PROJECT_NAME);
    }

    @Test
    public void testCreateProjectWithTeamId() throws Exception {
        projectDefinition.setTeamId(teamId);

        ProjectAppEntity createdProject =
            SafaRequest.withRoute(AppRoutes.Projects.CREATE_OR_UPDATE_PROJECT_META)
                .postAndParseResponse(projectDefinition, new TypeReference<>() {
                });

        assertThat(createdProject.getId()).isNotNull();

        Project project = projectService.getProjectById(createdProject.getId());
        assertThat(project.getOwningTeam().getId()).isEqualTo(teamId);
    }

    @Test
    public void testCreateProjectWithOrgId() throws Exception {
        projectDefinition.setOrgId(orgId);

        ProjectAppEntity createdProject =
            SafaRequest.withRoute(AppRoutes.Projects.CREATE_OR_UPDATE_PROJECT_META)
                .postAndParseResponse(projectDefinition, new TypeReference<>() {
                });

        assertThat(createdProject.getId()).isNotNull();

        Project project = projectService.getProjectById(createdProject.getId());
        Organization org = project.getOwningTeam().getOrganization();

        assertThat(org.getId()).isEqualTo(orgId);
        assertThat(project.getOwningTeam().getId()).isEqualTo(org.getFullOrgTeamId());
    }

    @Test
    public void testCreateProjectWithNoId() throws Exception {
        ProjectAppEntity createdProject =
            SafaRequest.withRoute(AppRoutes.Projects.CREATE_OR_UPDATE_PROJECT_META)
                .postAndParseResponse(projectDefinition, new TypeReference<>() {
                });

        assertThat(createdProject.getId()).isNotNull();

        Project project = projectService.getProjectById(createdProject.getId());
        assertThat(project.getOwningTeam().getOrganization().getId()).isEqualTo(getCurrentUser().getPersonalOrgId());
    }
}
