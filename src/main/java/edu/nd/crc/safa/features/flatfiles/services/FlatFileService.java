package edu.nd.crc.safa.features.flatfiles.services;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

import edu.nd.crc.safa.common.EntityParsingResult;
import edu.nd.crc.safa.common.ProjectEntities;
import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.config.ProjectVariables;
import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.commits.entities.app.ProjectCommit;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.errors.entities.db.CommitError;
import edu.nd.crc.safa.features.errors.repositories.CommitErrorRepository;
import edu.nd.crc.safa.features.flatfiles.parser.FlatFileParser;
import edu.nd.crc.safa.features.flatfiles.parser.TimFileParser;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.projects.entities.db.ProjectEntity;
import edu.nd.crc.safa.features.projects.services.ProjectRetrievalService;
import edu.nd.crc.safa.features.tgen.entities.TraceGenerationRequest;
import edu.nd.crc.safa.features.tgen.generator.TraceGenerationService;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.traces.entities.db.ApprovalStatus;
import edu.nd.crc.safa.features.versions.ProjectChanger;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
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
    private final TraceGenerationService traceGenerationService;
    private final FileUploadService fileUploadService;
    private final ProjectRetrievalService projectRetrievalService;

    /**
     * Responsible for creating a project from given flat files. This includes
     * parsing tim.json, creating artifacts, and their trace links.
     *
     * @param project         The project whose artifacts and trace links should be associated with
     * @param projectVersion  The version that the artifacts and errors will be associated with.
     * @param serviceProvider Provides persistent services for storing entity.
     * @param files           The flat files defining the project
     * @param asCompleteSet   Whether entities in flat files are complete set of entities in project version.
     * @return FlatFileResponse containing uploaded, parsed, and generated files.
     * @throws SafaError on any parsing error of tim.json, artifacts, or trace links
     */
    public ProjectAppEntity updateProjectFromFlatFiles(Project project,
                                                       ProjectVersion projectVersion,
                                                       ServiceProvider serviceProvider,
                                                       List<MultipartFile> files,
                                                       boolean asCompleteSet)
        throws SafaError, IOException {
        this.fileUploadService.uploadFilesToServer(project, files);
        JSONObject timFileContent = getTimFileContent(project);
        this.parseFlatFilesAndCommitEntities(projectVersion, serviceProvider, timFileContent, asCompleteSet);
        return this.projectRetrievalService.getProjectAppEntity(projectVersion);
    }

    /**
     * Constructs a project from the specification in TIM.json file.
     * Note, this route expects all files to be stored in local storage
     * before processing.
     *
     * @param projectVersion  The project version to be associated with the files specified.
     * @param serviceProvider Provides persistent service to application.
     * @param timFileJson     JSON definition of project extracted from tim.json file.
     * @param asCompleteSet   Whether to save entities in flat files as entire set of entities in project.
     * @throws SafaError any error occurring while parsing project.
     */
    public void parseFlatFilesAndCommitEntities(ProjectVersion projectVersion,
                                                ServiceProvider serviceProvider,
                                                JSONObject timFileJson,
                                                boolean asCompleteSet) throws SafaError {
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
            ProjectEntities projectEntities = new ProjectEntities(
                projectCommit.getArtifacts().getAdded(),
                projectCommit.getTraces().getAdded()
            );
            ProjectChanger projectChanger = new ProjectChanger(projectVersion, serviceProvider);
            if (asCompleteSet) {
                projectChanger.setEntitiesAsCompleteSet(projectEntities);
            } else {
                projectChanger.commit(projectCommit);
            }
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
                .filter(a -> a.getType().equalsIgnoreCase(sourceArtifactType))
                .collect(Collectors.toList());
            List<ArtifactAppEntity> targetArtifacts = artifacts
                .stream()
                .filter(a -> a.getType().equalsIgnoreCase(targetArtifactType))
                .collect(Collectors.toList());

            List<TraceAppEntity> generatedLinkInRequest = traceGenerationService
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
        String pathToFiles = ProjectPaths.Storage.projectUploadsPath(projectVersion.getProject(), false);
        TimFileParser timFileParser = new TimFileParser(timFileJson, pathToFiles);
        FlatFileParser flatFileParser = new FlatFileParser(timFileParser);
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
        String pathToTimFile = ProjectPaths.Storage.uploadedProjectFilePath(project, ProjectVariables.TIM_FILENAME);
        if (!Files.exists(Paths.get(pathToTimFile))) {
            throw new SafaError("TIM.json file was not uploaded for this project");
        }
        return FileUtilities.readJSONFile(pathToTimFile);
    }
}
