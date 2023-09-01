package edu.nd.crc.safa.test.base;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.features.github.entities.db.GithubProject;
import edu.nd.crc.safa.features.installations.InstallationDTO;
import edu.nd.crc.safa.features.jira.entities.db.JiraProject;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.types.entities.db.ArtifactType;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

/**
 * Given a Safa project test all external installations are correctly retrieved
 */
public class TestInstallationsSearch extends ApplicationBaseTest {

    private static final String PROJECT_NAME = "test-project";

    @Test
    public void allInstallationsForProjectAreLoaded() {
        Project project = dbEntityBuilder.newProject(PROJECT_NAME).getProject(PROJECT_NAME);
        JiraProject jiraProject = this.createJiraProject(UUID.randomUUID(), 10002L, project);
        GithubProject githubProject = this.createGithubProject("owner", "repository", "branch", project);
        List<InstallationDTO> installationDTOList = this.serviceProvider
            .getProjectRepository()
            .findInstallationsByProjectId(project.getProjectId());

        Assertions.assertEquals(2, installationDTOList.size());
    }

    private JiraProject createJiraProject(UUID orgId, Long id, Project project) {
        JiraProject jiraProject = new JiraProject();
        jiraProject.setOrgId(orgId);
        jiraProject.setJiraProjectId(id);
        jiraProject.setProject(project);
        return this.serviceProvider.getJiraProjectRepository().save(jiraProject);
    }

    private GithubProject createGithubProject(String owner, String repository, String branch, Project project) {
        ArtifactType type = dbEntityBuilder.newTypeAndReturn(PROJECT_NAME, "test type");

        GithubProject githubProject = new GithubProject();

        githubProject.setOwner(owner);
        githubProject.setRepositoryName(repository);
        githubProject.setProject(project);
        githubProject.setBranch(branch);
        githubProject.setArtifactType(type);
        return this.serviceProvider.getGithubProjectRepository().save(githubProject);
    }
}
