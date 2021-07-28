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
    public void CRUDProject() {
        //VP 1: Create Project
        Project project = new Project();
        project.setName(TEST_PROJECT_NAME);
        Serializable id = session.save(project);


        //VP 2: Retrieve Project
        Project queryProject = session.find(Project.class, project.getProjectId());
        assertThat(queryProject).isNotNull();
        assertThat(queryProject.getName()).isEqualTo(TEST_PROJECT_NAME);

        //VP 3: Update Project
        project.setName(ALT_PROJECT_NAME);
        session.update(project);
        queryProject = session.find(Project.class, project.getProjectId());
        assertThat(queryProject.getName()).isEqualTo(ALT_PROJECT_NAME);

        //VP 4: Delete Project
        session.delete(project);
        queryProject = session.find(Project.class, project.getProjectId());
        assertThat(queryProject).isNull();
    }
}
