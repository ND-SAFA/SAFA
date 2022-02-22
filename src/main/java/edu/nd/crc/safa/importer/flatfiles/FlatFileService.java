package edu.nd.crc.safa.importer.flatfiles;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.config.ProjectVariables;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.app.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.app.TraceAppEntity;
import edu.nd.crc.safa.server.entities.db.CommitError;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.repositories.CommitErrorRepository;
import edu.nd.crc.safa.server.services.EntityVersionService;
import edu.nd.crc.safa.utilities.FileUtilities;

import org.javatuples.Pair;
import org.json.JSONException;
import org.json.JSONObject;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

/**
 * Responsible for parsing flat files including reading,
 * validating, and storing their data.
 */
@Service
public class FlatFileService {

    private final ArtifactFileParser artifactFileParser;
    private final TraceFileParser traceFileParser;
    private final EntityVersionService entityVersionService;
    private final CommitErrorRepository commitErrorRepository;

    @Autowired
    public FlatFileService(ArtifactFileParser artifactFileParser,
                           TraceFileParser traceFileParser,
                           EntityVersionService entityVersionService,
                           CommitErrorRepository commitErrorRepository) {
        this.artifactFileParser = artifactFileParser;
        this.traceFileParser = traceFileParser;
        this.entityVersionService = entityVersionService;
        this.commitErrorRepository = commitErrorRepository;
    }

    public void parseProjectFilesFromTIM(ProjectVersion projectVersion) throws SafaError {
        Project project = projectVersion.getProject();
        String pathToFile = ProjectPaths.getPathToFlatFile(project, ProjectVariables.TIM_FILENAME);
        if (!Files.exists(Paths.get(pathToFile))) {
            throw new SafaError("TIM.json file was not uploaded for this project");
        }
        this.parseProject(projectVersion, pathToFile);
    }

    /**
     * Constructs a project from the specification in TIM.json file.
     * Note, this route expects all files to be stored in local storage
     * before processing.
     *
     * @param projectVersion the project version to be associated with the files specified.
     * @param pathToTIMFile  path to the TIM.json file in local storage (see ProjectPaths.java)
     * @throws SafaError any error occurring while parsing TIM.json or associated files.
     */
    public void parseProject(ProjectVersion projectVersion,
                             String pathToTIMFile) throws SafaError {
        try {
            // Parse TIM.json
            String TIMFileContent = new String(Files.readAllBytes(Paths.get(pathToTIMFile)));
            JSONObject timFileJson = FileUtilities.toLowerCase(new JSONObject(TIMFileContent));

            parseValidateSaveArtifacts(projectVersion, timFileJson);
            parseValidateSaveTraces(projectVersion, timFileJson);
        } catch (IOException | JSONException e) {
            throw new SafaError("An error occurred while parsing TIM file.", e);
        }
    }

    private void parseValidateSaveTraces(ProjectVersion projectVersion, JSONObject timFileJson) throws SafaError {
        List<TraceAppEntity> traces = traceFileParser.parseTraceFiles(projectVersion, timFileJson);
        this.entityVersionService.commitVersionTraces(projectVersion, traces);
    }

    private void parseValidateSaveArtifacts(ProjectVersion projectVersion, JSONObject timFileJson) throws SafaError {
        JSONObject dataFilesJson = timFileJson.getJSONObject(ProjectVariables.DATAFILES_PARAM);
        List<ArtifactAppEntity> artifacts = artifactFileParser.parseArtifactFiles(projectVersion, dataFilesJson);

        Pair<List<ArtifactAppEntity>, List<CommitError>> validationResponse = artifactFileParser
            .validateArtifacts(projectVersion, artifacts);
        List<CommitError> errors = new ArrayList<>(validationResponse.getValue1());
        this.commitErrorRepository.saveAll(errors);
        this.entityVersionService.commitVersionArtifacts(projectVersion,
            validationResponse.getValue0());
    }
}
