package edu.nd.crc.safa.server.flatFiles.services;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

import edu.nd.crc.safa.common.EntityCreation;
import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.config.ProjectVariables;
import edu.nd.crc.safa.server.entities.api.ProjectCommit;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.api.TraceGenerationRequest;
import edu.nd.crc.safa.server.entities.app.project.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.app.project.ProjectAppEntity;
import edu.nd.crc.safa.server.entities.app.project.TraceAppEntity;
import edu.nd.crc.safa.server.entities.db.ApprovalStatus;
import edu.nd.crc.safa.server.entities.db.CommitError;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectEntity;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.flatFiles.entities.ArtifactFileParser;
import edu.nd.crc.safa.server.flatFiles.entities.TIMParser;
import edu.nd.crc.safa.server.repositories.CommitErrorRepository;
import edu.nd.crc.safa.server.services.EntityVersionService;
import edu.nd.crc.safa.server.services.retrieval.AppEntityRetrievalService;
import edu.nd.crc.safa.tgen.TraceLinkGenerator;

import lombok.AllArgsConstructor;
import org.javatuples.Pair;
import org.json.JSONException;
import org.json.JSONObject;
import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

/**
 * Responsible for parsing flat files including reading,
 * validating, and storing their data.
 */
@Service
@Scope("singleton")
@AllArgsConstructor
public class FlatFileService {

    private final CommitErrorRepository commitErrorRepository;
    private final EntityVersionService entityVersionService;
    private final ArtifactFileParser artifactFileParser;
    private final TraceLinkGenerator traceLinkGenerator;
    private final FileService fileService;
    private final AppEntityRetrievalService appEntityRetrievalService;

    /**
     * Responsible for creating a project from given flat files. This includes
     * parsing tim.json, creating artifacts, and their trace links.
     *
     * @param project        The project whose artifacts and trace links should be associated with
     * @param projectVersion The version that the artifacts and errors will be associated with.
     * @param files          the flat files defining the project
     * @return FlatFileResponse containing uploaded, parsed, and generated files.
     * @throws SafaError on any parsing error of tim.json, artifacts, or trace links
     */
    public ProjectAppEntity uploadAndCreateProjectFromFlatFiles(Project project,
                                                                ProjectVersion projectVersion,
                                                                MultipartFile[] files)
        throws SafaError {
        this.fileService.uploadFilesToServer(project, Arrays.asList(files));
        String pathToFile = ProjectPaths.getPathToFlatFile(project, ProjectVariables.TIM_FILENAME);
        if (!Files.exists(Paths.get(pathToFile))) {
            throw new SafaError("TIM.json file was not uploaded for this project");
        }
        this.constructProjectFromFlatFiles(projectVersion, pathToFile);
        return this.appEntityRetrievalService.retrieveProjectEntitiesAtProjectVersion(projectVersion);
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
            JSONObject timFileJson = new JSONObject(TIMFileContent);

            // Step - Parse artifacts, traces, and trace generation requests
            Pair<ProjectCommit, List<TraceGenerationRequest>> parseTIMResponse = parseTIMIntoCommit(
                projectVersion,
                timFileJson);

            // Step - Attempt to perform commit, saving errors on fail.
            ProjectCommit projectCommit = parseTIMResponse.getValue0();

            // Step - Generate trace link requests (post-artifact construction if successful)
            List<TraceGenerationRequest> traceGenerationRequests = parseTIMResponse.getValue1();
            List<TraceAppEntity> generatedLinks = generateTraceLinks(
                projectCommit.getArtifacts().getAdded(),
                traceGenerationRequests);
            generatedLinks = filterDuplicateGeneratedLinks(projectCommit.getTraces().getAdded(),
                generatedLinks);

            // Step - Commit generated trace links
            projectCommit.getTraces().getAdded().addAll(generatedLinks);

            // Step - Commit all project entities
            this.entityVersionService.setProjectEntitiesAtVersion(
                projectVersion,
                projectCommit.getArtifacts().getAdded(), // not other modifications on flat file upload
                projectCommit.getTraces().getAdded());
            this.commitErrorRepository.saveAll(projectCommit.getErrors());
        } catch (IOException | JSONException e) {
            throw new SafaError("An error occurred while parsing TIM file.", e);
        }
    }

    public List<TraceAppEntity> generateTraceLinks(List<ArtifactAppEntity> artifacts,
                                                   List<TraceGenerationRequest> traceGenerationRequests) {
        List<TraceAppEntity> generatedLinks = new ArrayList<>();

        for (TraceGenerationRequest request : traceGenerationRequests) {
            String sourceArtifactType = request.getSource();
            String targetArtifactType = request.getTarget();

            List<ArtifactAppEntity> sourceArtifacts = artifacts
                .stream()
                .filter(a -> a.type.equalsIgnoreCase(sourceArtifactType))
                .collect(Collectors.toList());
            List<ArtifactAppEntity> targetArtifacts = artifacts
                .stream()
                .filter(a -> a.type.equalsIgnoreCase(targetArtifactType))
                .collect(Collectors.toList());

            List<TraceAppEntity> generatedLinkInRequest = traceLinkGenerator
                .generateLinksBetweenArtifactAppEntities(sourceArtifacts, targetArtifacts);
            generatedLinks.addAll(generatedLinkInRequest);
        }
        return generatedLinks;
    }

    public List<TraceAppEntity> filterDuplicateGeneratedLinks(List<TraceAppEntity> manualLinks,
                                                              List<TraceAppEntity> generatedLinks) {
        String DELIMITER = "*";
        List<String> approvedLinks = manualLinks.stream()
            .filter(link -> link.approvalStatus.equals(ApprovalStatus.APPROVED))
            .map(link -> link.sourceName + DELIMITER + link.targetName)
            .collect(Collectors.toList());

        return generatedLinks
            .stream()
            .filter(t -> {
                String tId = t.sourceName + DELIMITER + t.targetName;
                return !approvedLinks.contains(tId);
            })
            .collect(Collectors.toList());
    }

    public Pair<ProjectCommit, List<TraceGenerationRequest>> parseTIMIntoCommit(ProjectVersion projectVersion,
                                                                                JSONObject timFileJson
    ) throws SafaError {
        // Step - Create project parser
        TIMParser TIMParser = new TIMParser(timFileJson);
        TIMParser.parse();

        // Step - parse artifacts then traces
        EntityCreation<ArtifactAppEntity, String> artifactCreationResponse =
            artifactFileParser.parseArtifactFiles(projectVersion,
                TIMParser);
        Pair<List<TraceAppEntity>, List<TraceGenerationRequest>> traceResponse =
            TIMParser.parseTraces(projectVersion);
        List<TraceAppEntity> traces = traceResponse.getValue0();

        // Step - Create project commit with parsed artifacts and traces
        ProjectCommit projectCommit = new ProjectCommit(projectVersion, false);
        projectCommit.getArtifacts().setAdded(artifactCreationResponse.getEntities());
        projectCommit.getTraces().setAdded(traces);

        List<CommitError> commitErrors =
            artifactCreationResponse
                .getErrors()
                .stream()
                .map(e -> new CommitError(projectVersion, e, ProjectEntity.ARTIFACTS))
                .collect(Collectors.toList());
        projectCommit.getErrors().addAll(commitErrors);

        return new Pair<>(projectCommit, traceResponse.getValue1());
    }
}
