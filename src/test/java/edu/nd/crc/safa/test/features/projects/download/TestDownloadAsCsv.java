package edu.nd.crc.safa.test.features.projects.download;

import static org.assertj.core.api.Assertions.assertThat;

import java.io.File;
import java.util.List;

import edu.nd.crc.safa.authentication.AuthorizationSetter;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.flatfiles.services.DataFileBuilder;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;
import edu.nd.crc.safa.test.requests.SafaRequest;

import org.javatuples.Pair;
import org.junit.jupiter.api.Test;

/**
 * Tests that a project's flat files is able to be downloaded as zip file.
 */
class TestDownloadAsCsv extends ApplicationBaseTest {

    @Test
    void downloadDefaultProject() throws Exception {
        Pair<ProjectVersion, ProjectVersion> response = creationService.createDualVersions(projectName, true);
        ProjectVersion projectVersion = response.getValue0();
        AuthorizationSetter.setSessionAuthorization(currentUserName, serviceProvider);
        ProjectAppEntity projectAppEntity = this.serviceProvider
            .getProjectRetrievalService().getProjectAppEntity(projectVersion);
        List<File> projectFiles = new SafaRequest(AppRoutes.FlatFiles.DOWNLOAD_FLAT_FILES)
            .withVersion(projectVersion)
            .withFileType(DataFileBuilder.AcceptedFileTypes.JSON)
            .getWithFilesInZip();

        assertThat(projectFiles).isNotEmpty();
    }
}
