package unit.flatfile;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import java.io.IOException;
import java.util.List;

import edu.nd.crc.safa.builders.MultipartRequestService;
import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.config.ProjectVariables;
import edu.nd.crc.safa.flatfiles.entities.TimParser;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.utilities.FileUtilities;

import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import org.springframework.web.multipart.MultipartFile;
import unit.ApplicationBaseTest;

class TestTimParser extends ApplicationBaseTest {
    String projectName = "default-project";

    @Test
    void testDefaultProject() throws IOException {
        // Step - Upload files for project
        Project project = this.dbEntityBuilder.newProjectWithReturn(projectName);
        List<MultipartFile> files = MultipartRequestService.readDirectoryAsMultipartFiles(
            ProjectPaths.PATH_TO_DEFAULT_PROJECT,
            "files");
        this.fileService.uploadFilesToServer(project, files);

        // Step - Start processing for
        String pathToTimFile = ProjectPaths.getPathToFlatFile(project, ProjectVariables.TIM_FILENAME);
        JSONObject timJson = FileUtilities.readJSONFile(pathToTimFile);
        TimParser timParser = new TimParser(timJson, ProjectPaths.getPathToUploadedFiles(project, false));

        // VP - Assert that 4 artifact files and 6 trace files
        assertThat(timParser.getArtifactFiles().size()).isEqualTo(4);
        assertThat(timParser.getTraceFiles().size()).isEqualTo(6);
    }
}
