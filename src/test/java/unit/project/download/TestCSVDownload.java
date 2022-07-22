package unit.project.download;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import java.io.File;
import java.util.List;

import edu.nd.crc.safa.builders.requests.SafaRequest;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;

import org.junit.jupiter.api.Disabled;
import org.junit.jupiter.api.Test;
import unit.ApplicationBaseTest;

class TestCSVDownload extends ApplicationBaseTest {

    @Test
    @Disabled("Current under development")
    void downloadDefaultProject() throws Exception {
        String projectName = "default-project";
        ProjectVersion projectVersion = createDefaultProject(projectName);
        List<File> projectFiles = new SafaRequest(AppRoutes.Projects.FlatFiles.downloadFlatFiles)
            .withVersion(projectVersion)
            .getWithFilesInZip();

        assertThat(projectFiles.size()).isPositive();
    }
}
