package edu.nd.crc.safa.flatfiles.services;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

import edu.nd.crc.safa.common.EntityParsingResult;
import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.config.ProjectVariables;
import edu.nd.crc.safa.flatfiles.entities.FlatFileParser;
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
import edu.nd.crc.safa.server.repositories.CommitErrorRepository;
import edu.nd.crc.safa.server.services.EntityVersionService;
import edu.nd.crc.safa.server.services.retrieval.AppEntityRetrievalService;
import edu.nd.crc.safa.tgen.TraceLinkGenerator;
import edu.nd.crc.safa.utilities.FileUtilities;

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
    private static final String DELIMITER = "*";

    private final CommitErrorRepository commitErrorRepository;
    private final EntityVersionService entityVersionService;
    private final TraceLinkGenerator traceLinkGenerator;
    private final FileUploadService fileUploadService;
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
    public ProjectAppEntity createProjectFromFlatFiles(Project project,
                                                       ProjectVersion projectVersion,
                                                       MultipartFile[] files)
        throws SafaError, IOException {
        this.fileUploadService.uploadFilesToServer(project, Arrays.asList(files));
        JSONObject timFileContent = getTimFileContent(project);
        this.parseFlatFilesAndCommitEntities(projectVersion, timFileContent);
        return this.appEntityRetrievalService.retrieveProjectAppEntityAtProjectVersion(projectVersion);
    }

    /**
     * Constructs a project from the specification in TIM.json file.
     * Note, this route expects all files to be stored in local storage
     * before processing.
     *
     * @param projectVersion the project version to be associated with the files specified.
     * @param timFileJson    JSON definition of project extracted from tim.json file.
     * @throws SafaError any error occurring while parsing project.
     */
    public void parseFlatFilesAndCommitEntities(ProjectVersion projectVersion,
                                                JSONObject timFileJson) throws SafaError {
        try {
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
        List<String> approvedLinks = manualLinks.stream()
            .filter(link -> link.getApprovalStatus().equals(ApprovalStatus.APPROVED))
            .map(link -> link.getSourceName() + DELIMITER + link.getTargetName())
            .collect(Collectors.toList());

        return generatedLinks
            .stream()
            .filter(t -> {
                String tId = t.getSourceName() + DELIMITER + t.getTargetName();
                return !approvedLinks.contains(tId);
            })
            .collect(Collectors.toList());
    }

    /**
     * Creates commit with all parsed artifacts, traces, and trace generation requests in specified tim.json.
     *
     * @param projectVersion The version where the commit will be made.
     * @param timFileJson    The project specification file.
     * @return Pair of ProjectCommit containing entities and list of trace generation requests.
     * @throws SafaError   Throws error is a critical error has occurred. Current reasons are:
     *                     - syntax error or unknown reference in the tim.json.
     * @throws IOException Throws IOException if an errors occurs while reading files in tim.json.
     */
    public Pair<ProjectCommit, List<TraceGenerationRequest>> parseTIMIntoCommit(ProjectVersion projectVersion,
                                                                                JSONObject timFileJson
    ) throws SafaError, IOException {
        // Step - Create project parser
        String pathToFiles = ProjectPaths.getPathToUploadedFiles(projectVersion.getProject(), false);
        FlatFileParser flatFileParser = new FlatFileParser(timFileJson, pathToFiles);
        ProjectCommit projectCommit = new ProjectCommit(projectVersion, false);

        // Step - parse artifacts
        EntityParsingResult<ArtifactAppEntity, String> artifactCreationResponse = flatFileParser.parseArtifacts();
        List<ArtifactAppEntity> artifactsAdded = artifactCreationResponse.getEntities();
        projectCommit.getArtifacts().setAdded(artifactCreationResponse.getEntities());
        addErrorsToCommit(projectCommit,
            artifactCreationResponse.getErrors(),
            projectVersion,
            ProjectEntity.ARTIFACTS);

        // Step - parse traces
        EntityParsingResult<TraceAppEntity, String> traceCreationResponse = flatFileParser.parseTraces(artifactsAdded);
        projectCommit.getTraces().setAdded(traceCreationResponse.getEntities());
        addErrorsToCommit(projectCommit,
            traceCreationResponse.getErrors(),
            projectVersion,
            ProjectEntity.TRACES);

        return new Pair<>(projectCommit, flatFileParser.getTraceGenerationRequests());
    }

    private void addErrorsToCommit(ProjectCommit projectCommit,
                                   List<String> errors,
                                   ProjectVersion projectVersion,
                                   ProjectEntity projectEntity) {
        List<CommitError> commitErrors =
            errors
                .stream()
                .map(e -> new CommitError(projectVersion, e, projectEntity))
                .collect(Collectors.toList());
        projectCommit.getErrors().addAll(commitErrors);
    }

    private JSONObject getTimFileContent(Project project) throws IOException {
        String pathToTimFile = ProjectPaths.getPathToFlatFile(project, ProjectVariables.TIM_FILENAME);
        if (!Files.exists(Paths.get(pathToTimFile))) {
            throw new SafaError("TIM.json file was not uploaded for this project");
        }
        return FileUtilities.readJSONFile(pathToTimFile);
    }
}
