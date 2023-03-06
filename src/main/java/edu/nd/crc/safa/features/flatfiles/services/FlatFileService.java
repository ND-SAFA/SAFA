package edu.nd.crc.safa.features.flatfiles.services;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;

import edu.nd.crc.safa.authentication.builders.ResourceBuilder;
import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.config.ProjectVariables;
import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.commits.entities.app.ProjectCommit;
import edu.nd.crc.safa.features.common.EntityParsingResult;
import edu.nd.crc.safa.features.common.ProjectEntities;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.errors.entities.db.CommitError;
import edu.nd.crc.safa.features.errors.repositories.CommitErrorRepository;
import edu.nd.crc.safa.features.flatfiles.parser.FlatFileParser;
import edu.nd.crc.safa.features.flatfiles.parser.TimFileParser;
import edu.nd.crc.safa.features.models.tgen.entities.TraceGenerationRequest;
import edu.nd.crc.safa.features.models.tgen.generator.TraceGenerationService;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.projects.entities.db.ProjectEntity;
import edu.nd.crc.safa.features.projects.services.ProjectRetrievalService;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.ProjectChanger;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.utilities.JsonFileUtilities;

import lombok.Setter;
import org.javatuples.Pair;
import org.json.JSONException;
import org.json.JSONObject;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Lazy;
import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

/**
 * Responsible for parsing flat files including reading,
 * validating, and storing their data.
 */
@Service
@Scope("singleton")
public class FlatFileService {

    private final ResourceBuilder resourceBuilder;
    private final CommitErrorRepository commitErrorRepository;
    private final TraceGenerationService traceGenerationService;
    private final FileUploadService fileUploadService;
    private final ProjectRetrievalService projectRetrievalService;

    @Setter(onMethod = @__({@Autowired, @Lazy}))
    private ServiceProvider serviceProvider;

    public FlatFileService(ResourceBuilder resourceBuilder, CommitErrorRepository commitErrorRepository,
                           TraceGenerationService traceGenerationService, FileUploadService fileUploadService,
                           ProjectRetrievalService projectRetrievalService) {
        this.resourceBuilder = resourceBuilder;
        this.commitErrorRepository = commitErrorRepository;
        this.traceGenerationService = traceGenerationService;
        this.fileUploadService = fileUploadService;
        this.projectRetrievalService = projectRetrievalService;
    }

    /**
     * Responsible for creating a project from given flat files. This includes
     * parsing tim.json, creating artifacts, and their trace links.
     *
     * @param projectVersion  The version that the artifacts and errors will be associated with.
     * @param files           The flat files defining the project
     * @param asCompleteSet   Whether entities in flat files are complete set of entities in project version.
     * @return FlatFileResponse containing uploaded, parsed, and generated files.
     * @throws SafaError on any parsing error of tim.json, artifacts, or trace links
     */
    public ProjectAppEntity updateProjectFromFlatFiles(ProjectVersion projectVersion,
                                                       List<MultipartFile> files,
                                                       boolean asCompleteSet)
        throws SafaError, IOException {

        Project project = projectVersion.getProject();
        this.fileUploadService.uploadFilesToServer(project, files);
        JSONObject timFileContent = getTimFileContent(project);
        this.parseFlatFilesAndCommitEntities(projectVersion, timFileContent, asCompleteSet);
        return this.projectRetrievalService.getProjectAppEntity(projectVersion);
    }

    /**
     * Responsible for creating a project from given flat files. This includes
     * parsing tim.json, creating artifacts, and their trace links.
     *
     * @param projectVersionId  The ID of the version that the artifacts and errors will be associated with.
     * @param user              The user performing the operation.
     * @param files             The flat files defining the project
     * @param asCompleteSet     Whether entities in flat files are complete set of entities in project version.
     * @return FlatFileResponse containing uploaded, parsed, and generated files.
     * @throws SafaError on any parsing error of tim.json, artifacts, or trace links
     */
    public ProjectAppEntity updateProjectFromFlatFiles(UUID projectVersionId,
                                                       SafaUser user,
                                                       List<MultipartFile> files,
                                                       boolean asCompleteSet)
            throws SafaError, IOException {

        ProjectVersion projectVersion = this.resourceBuilder.fetchVersion(projectVersionId).withEditVersionAs(user);
        return updateProjectFromFlatFiles(projectVersion, files, asCompleteSet);
    }

    /**
     * Constructs a project from the specification in TIM.json file.
     * Note, this route expects all files to be stored in local storage
     * before processing.
     *
     * @param projectVersion  The project version to be associated with the files specified.
     * @param timFileJson     JSON definition of project extracted from tim.json file.
     * @param asCompleteSet   Whether to save entities in flat files as entire set of entities in project.
     * @throws SafaError any error occurring while parsing project.
     */
    public void parseFlatFilesAndCommitEntities(ProjectVersion projectVersion,
                                                JSONObject timFileJson,
                                                boolean asCompleteSet) {
        try {
            // Step - Parse artifacts, traces, and trace generation requests
            Pair<ProjectCommit, TraceGenerationRequest> parseTIMResponse = parseTIMIntoCommit(
                projectVersion,
                timFileJson);

            // Step - Attempt to perform commit, saving errors on fail.
            ProjectCommit projectCommit = parseTIMResponse.getValue0();

            // Step - Generate trace link requests (post-artifact construction if successful)
            TraceGenerationRequest traceGenerationRequest = parseTIMResponse.getValue1();
            ProjectAppEntity projectAppEntity = new ProjectAppEntity(projectCommit);
            List<TraceAppEntity> generatedLinks = this.traceGenerationService.generateTraceLinks(
                traceGenerationRequest,
                projectAppEntity
            );
            generatedLinks = this.traceGenerationService.filterDuplicateGeneratedLinks(
                projectCommit.getTraces().getAdded(),
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
    public Pair<ProjectCommit, TraceGenerationRequest> parseTIMIntoCommit(
        ProjectVersion projectVersion,
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

        return new Pair<>(projectCommit, flatFileParser.getTraceGenerationRequest());
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
        return JsonFileUtilities.readJSONFile(pathToTimFile);
    }
}
