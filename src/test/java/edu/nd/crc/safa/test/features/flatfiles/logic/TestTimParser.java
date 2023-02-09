package edu.nd.crc.safa.test.features.flatfiles.logic;

import static org.assertj.core.api.Assertions.assertThat;

import java.io.IOException;
import java.util.List;
import java.util.Objects;
import java.util.stream.Collectors;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.config.ProjectVariables;
import edu.nd.crc.safa.features.flatfiles.parser.FlatFileParser;
import edu.nd.crc.safa.features.flatfiles.parser.TimFileParser;
import edu.nd.crc.safa.features.flatfiles.parser.formats.csv.CsvTraceFile;
import edu.nd.crc.safa.features.flatfiles.services.MultipartRequestService;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;
import edu.nd.crc.safa.utilities.JsonFileUtilities;

import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import org.springframework.web.multipart.MultipartFile;

class TestTimParser extends ApplicationBaseTest {
    String projectName = "default-project";

    @Test
    void testDefaultProject() throws IOException {
        // Step - Upload files for project
        Project project = this.dbEntityBuilder.newProjectWithReturn(projectName);
        List<MultipartFile> files = MultipartRequestService.readDirectoryAsMultipartFiles(
            ProjectPaths.Resources.Tests.DefaultProject.V1,
            "files");
        this.fileUploadService.uploadFilesToServer(project, files);

        // Step - Start processing for
        String pathToTimFile = ProjectPaths.Storage.uploadedProjectFilePath(project, ProjectVariables.TIM_FILENAME);
        JSONObject timJson = JsonFileUtilities.readJSONFile(pathToTimFile);
        TimFileParser timFileParser = new TimFileParser(timJson, ProjectPaths.Storage.projectUploadsPath(project,
            false));
        FlatFileParser flatFileParser = new FlatFileParser(timFileParser);

        // VP - Assert that 4 artifact files and 6 trace files
        assertThat(flatFileParser.getArtifactFiles()).hasSize(4);
        assertThat(flatFileParser.getTraceFiles()).hasSize(6);
    }

    @Test
    void testTraceFile() throws IOException {
        Project project = this.dbEntityBuilder.newProjectWithReturn(projectName);
        List<MultipartFile> files = MultipartRequestService.readDirectoryAsMultipartFiles(
            ProjectPaths.Resources.Tests.DefaultProject.V1,
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
        assertThat(traces).hasSize(3);
    }
}
