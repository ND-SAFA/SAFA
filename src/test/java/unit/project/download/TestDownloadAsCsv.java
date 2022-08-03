package unit.project.download;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import java.io.File;
import java.util.List;

import edu.nd.crc.safa.builders.requests.SafaRequest;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.flatfiles.services.DataFileBuilder;
import edu.nd.crc.safa.server.entities.app.project.ProjectAppEntity;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;

import org.javatuples.Pair;
import org.junit.jupiter.api.Test;
import unit.ApplicationBaseTest;

class TestDownloadAsCsv extends ApplicationBaseTest {

    @Test
    void downloadDefaultProject() throws Exception {
        String projectName = "default-project";
        Pair<ProjectVersion, ProjectVersion> response = createDualVersions(projectName, true);
        ProjectVersion projectVersion = response.getValue0();
        setAuthorization();
        ProjectAppEntity projectAppEntity =
            this.appEntityRetrievalService.retrieveProjectAppEntityAtProjectVersion(projectVersion);
        List<File> projectFiles = new SafaRequest(AppRoutes.Projects.FlatFiles.downloadFlatFiles)
            .withVersion(projectVersion)
            .withFileType(DataFileBuilder.AcceptedFileTypes.JSON)
            .getWithFilesInZip();

        assertThat(projectFiles.size()).isPositive();
    }
}
