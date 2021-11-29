package unit.db;

import static org.assertj.core.api.Assertions.assertThat;

import edu.nd.crc.safa.server.entities.db.Project;

import org.junit.jupiter.api.Test;
import unit.ApplicationBaseTest;

/**
 * Responsible for testing that projects can be created, modified, deleted,
 * and retrieved.
 */
public class TestProject extends ApplicationBaseTest {

    @Test
    public void createRetrieveUpdateDeleteProject() {
        String projectName = "test_project";
        String altProjectName = "some_other_project";

        // Step - Create Project
        dbEntityBuilder.newProject(user, projectName);
        Project project = dbEntityBuilder.getProject(projectName);

        // VP - Retrieve project and verify name
        Project queryProject = projectRepository.findByProjectId(project.getProjectId());
        assertThat(queryProject).isNotNull();
        assertThat(queryProject.getName()).isEqualTo(projectName);

        // VP - Update project name and verify change
        dbEntityBuilder.updateProjectName(projectName, altProjectName);
        queryProject = projectRepository.findByProjectId(project.getProjectId());
        assertThat(queryProject.getName()).isEqualTo(altProjectName);

        // VP - Delete Project and confirm cannot find
        projectRepository.delete(project);
        queryProject = projectRepository.findByProjectId(project.getProjectId());
        assertThat(queryProject).isNull();
    }
}
