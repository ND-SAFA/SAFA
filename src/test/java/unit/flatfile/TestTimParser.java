package unit.flatfile;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import java.io.IOException;
import java.util.List;
import java.util.Objects;
import java.util.stream.Collectors;

import edu.nd.crc.safa.builders.MultipartRequestService;
import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.config.ProjectVariables;
import edu.nd.crc.safa.features.flatfiles.entities.FlatFileParser;
import edu.nd.crc.safa.features.flatfiles.entities.csv.CsvTraceFile;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.projects.entities.db.Project;
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
        this.fileUploadService.uploadFilesToServer(project, files);

        // Step - Start processing for
        String pathToTimFile = ProjectPaths.getPathToFlatFile(project, ProjectVariables.TIM_FILENAME);
        JSONObject timJson = FileUtilities.readJSONFile(pathToTimFile);
        FlatFileParser flatFileParser = new FlatFileParser(timJson, ProjectPaths.getPathToUploadedFiles(project, false));

        // VP - Assert that 4 artifact files and 6 trace files
        assertThat(flatFileParser.getArtifactFiles().size()).isEqualTo(4);
        assertThat(flatFileParser.getTraceFiles().size()).isEqualTo(6);
    }

    @Test
    void testTraceFile() throws IOException {
        Project project = this.dbEntityBuilder.newProjectWithReturn(projectName);
        List<MultipartFile> files = MultipartRequestService.readDirectoryAsMultipartFiles(
            ProjectPaths.PATH_TO_DEFAULT_PROJECT,
            "files");
        this.fileUploadService.uploadFilesToServer(project, files);
        MultipartFile file =
            files
                .stream()
                .filter(f -> Objects.equals(f.getOriginalFilename(), "Design2Design.csv"))
                .collect(Collectors.toList())
                .get(0);

        CsvTraceFile traceFile = new CsvTraceFile(file);
        List<TraceAppEntity> traces = traceFile.getEntities();
        assertThat(traces.size()).isEqualTo(3);
    }
}
