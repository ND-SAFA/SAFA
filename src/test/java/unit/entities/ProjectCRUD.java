package unit.entities;

import static org.assertj.core.api.Assertions.assertThat;

import java.io.Serializable;

import edu.nd.crc.safa.entities.Project;

import org.junit.jupiter.api.Test;

/**
 * Responsible for testing CRUD operation on the Project entity
 */
public class ProjectCRUD extends EntityBaseTest {

    String TEST_PROJECT_NAME = "test_project";
    String ALT_PROJECT_NAME = "some_other_project";

    @Test
    public void createRetrieveUpdateDeleteProject() {
        //VP 1: Create Project
        Project project = new Project(TEST_PROJECT_NAME);
        Serializable id = projectRepository.save(project);

        //VP 2: Retrieve Project
        Project queryProject = projectRepository.findByProjectId(project.getProjectId());
        assertThat(queryProject).isNotNull();
        assertThat(queryProject.getName()).isEqualTo(TEST_PROJECT_NAME);

        //VP 3: Update Project
        project.setName(ALT_PROJECT_NAME);
        projectRepository.save(project);
        queryProject = projectRepository.findByProjectId(project.getProjectId());
        assertThat(queryProject.getName()).isEqualTo(ALT_PROJECT_NAME);

        //VP 4: Delete Project
        projectRepository.delete(project);
        queryProject = projectRepository.findByProjectId(project.getProjectId());
        assertThat(queryProject).isNull();
    }
}
