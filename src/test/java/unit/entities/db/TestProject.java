package unit.entities.db;

import static org.assertj.core.api.Assertions.assertThat;

import edu.nd.crc.safa.db.entities.sql.Project;

import org.junit.jupiter.api.Test;
import unit.EntityBaseTest;

/**
 * Responsible for testing that projects can be created, modified, deleted,
 * and retrieved.
 */
public class TestProject extends EntityBaseTest {

    @Test
    public void createRetrieveUpdateDeleteProject() {
        String projectName = "test_project";
        String altProjectName = "some_other_project";

        // Step - Create Project
        entityBuilder.newProject(projectName);
        Project project = entityBuilder.getProject(projectName);

        // VP - Retrieve project and verify name
        Project queryProject = projectRepository.findByProjectId(project.getProjectId());
        assertThat(queryProject).isNotNull();
        assertThat(queryProject.getName()).isEqualTo(projectName);

        // VP - Update project name and verify change
        entityBuilder.updateProjectName(projectName, altProjectName);
        queryProject = projectRepository.findByProjectId(project.getProjectId());
        assertThat(queryProject.getName()).isEqualTo(altProjectName);

        // VP - Delete Project and confirm cannot find
        projectRepository.delete(project);
        queryProject = projectRepository.findByProjectId(project.getProjectId());
        assertThat(queryProject).isNull();
    }
}
