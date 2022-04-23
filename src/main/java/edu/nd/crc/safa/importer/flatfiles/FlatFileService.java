package edu.nd.crc.safa.importer.flatfiles;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;

import edu.nd.crc.safa.config.ProjectVariables;
import edu.nd.crc.safa.importer.tracegenerator.TraceLinkGenerator;
import edu.nd.crc.safa.server.entities.api.ProjectCommit;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.api.TraceGenerationRequest;
import edu.nd.crc.safa.server.entities.app.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.app.TraceAppEntity;
import edu.nd.crc.safa.server.entities.db.ArtifactType;
import edu.nd.crc.safa.server.entities.db.CommitError;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.repositories.CommitErrorRepository;
import edu.nd.crc.safa.server.services.CommitService;
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

    private final CommitErrorRepository commitErrorRepository;
    private final CommitService commitService;

    private final ArtifactFileParser artifactFileParser;
    private final TraceFileParser traceFileParser;
    private final TraceLinkGenerator traceLinkGenerator;

    @Autowired
    public FlatFileService(CommitErrorRepository commitErrorRepository,
                           CommitService commitService,
                           ArtifactFileParser artifactFileParser,
                           TraceFileParser traceFileParser,
                           TraceLinkGenerator traceLinkGenerator) {
        this.commitErrorRepository = commitErrorRepository;
        this.artifactFileParser = artifactFileParser;
        this.traceFileParser = traceFileParser;
        this.commitService = commitService;
        this.traceLinkGenerator = traceLinkGenerator;
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
    public void constructProjectFromFlatFiles(ProjectVersion projectVersion,
                                              String pathToTIMFile) throws SafaError {
        try {
            // Parse TIM.json
            String TIMFileContent = new String(Files.readAllBytes(Paths.get(pathToTIMFile)));
            JSONObject timFileJson = FileUtilities.toLowerCase(new JSONObject(TIMFileContent));

            // Step - Parse artifacts, traces, and trace generation requests
            Pair<ProjectCommit, List<TraceGenerationRequest>> parseTIMResponse = parseTIMIntoCommit(
                projectVersion,
                timFileJson);
            ProjectCommit projectCommit = parseTIMResponse.getValue0();
            List<TraceGenerationRequest> traceGenerationRequests = parseTIMResponse.getValue1();

            // Step - Attempt to perform commit, saving errors on fail.
            ProjectCommit commitResponse = this.commitService.performCommit(projectCommit);
            this.commitErrorRepository.saveAll(commitResponse.getErrors());
            List<CommitError> savedErrors = this.commitErrorRepository.findByProjectVersion(projectVersion);
            // Step - Generate trace link requests (post-artifact construction if successful)
            Project project = projectVersion.getProject();
            List<TraceAppEntity> generatedLinks = new ArrayList<>();
            for (TraceGenerationRequest request : traceGenerationRequests) {
                ArtifactType sourceType = traceFileParser.findArtifactTypeFromTraceMatrixDefinition(project,
                    request.getSource());
                ArtifactType targetType = traceFileParser.findArtifactTypeFromTraceMatrixDefinition(project,
                    request.getTarget());

                List<TraceAppEntity> generatedLinkInRequest = traceLinkGenerator
                    .generateTraceLinksToFile(projectVersion, Pair.with(sourceType, targetType));
                generatedLinks.addAll(generatedLinkInRequest);
            }

            // Step - Commit generated trace links
            ProjectCommit generatedLinkCommit = new ProjectCommit(projectVersion, false);
            generatedLinkCommit.getTraces().setAdded(generatedLinks);
            //this.commitService.performCommit(generatedLinkCommit);
        } catch (IOException | JSONException e) {
            throw new SafaError("An error occurred while parsing TIM file.", e);
        }
    }

    private Pair<ProjectCommit, List<TraceGenerationRequest>> parseTIMIntoCommit(ProjectVersion projectVersion,
                                                                                 JSONObject timFileJson
    ) throws SafaError {
        ProjectCommit projectCommit = new ProjectCommit(projectVersion, false);
        JSONObject dataFilesJson = timFileJson.getJSONObject(ProjectVariables.DATAFILES_PARAM);
        List<ArtifactAppEntity> artifacts = artifactFileParser.parseArtifactFiles(projectVersion, dataFilesJson);
        Pair<List<TraceAppEntity>, List<TraceGenerationRequest>> traceResponse =
            traceFileParser.parseTraceFiles(projectVersion,
                timFileJson);
        List<TraceAppEntity> traces = traceResponse.getValue0();
        projectCommit.getArtifacts().setAdded(artifacts);
        projectCommit.getTraces().setAdded(traces);
        return new Pair<>(projectCommit, traceResponse.getValue1());
    }
}
