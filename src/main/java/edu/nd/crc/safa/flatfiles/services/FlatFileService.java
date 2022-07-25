package edu.nd.crc.safa.flatfiles.services;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Hashtable;
import java.util.List;
import java.util.Map;
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
    private final TraceLinkGenerator traceLinkGenerator;
    private final FileService fileService;
    private final AppEntityRetrievalService appEntityRetrievalService;
    private final FileCreatorService fileCreatorService;

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
        throws SafaError {
        this.fileService.uploadFilesToServer(project, Arrays.asList(files));
        String pathToTimFile = ProjectPaths.getPathToFlatFile(project, ProjectVariables.TIM_FILENAME);
        if (!Files.exists(Paths.get(pathToTimFile))) {
            throw new SafaError("TIM.json file was not uploaded for this project");
        }
        this.parseFlatFilesAndCommitEntities(projectVersion, pathToTimFile);
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
    public void parseFlatFilesAndCommitEntities(ProjectVersion projectVersion,
                                                String pathToTIMFile) throws SafaError {
        try {
            // Parse TIM.json
            String timFileContent = new String(Files.readAllBytes(Paths.get(pathToTIMFile)));
            JSONObject timFileJson = new JSONObject(timFileContent);

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

    public List<File> downloadProjectFiles(ProjectVersion projectVersion) throws IOException {
        Project project = projectVersion.getProject();
        ProjectAppEntity projectAppEntity =
            this.appEntityRetrievalService.retrieveProjectAppEntityAtProjectVersion(projectVersion);
        Map<String, ArtifactAppEntity> name2artifact = new HashMap<>();
        Map<String, List<ArtifactAppEntity>> type2Artifacts = new HashMap<>();
        Map<String, Map<String, List<TraceAppEntity>>> type2Traces = new HashMap<>();
        List<File> projectFiles = new ArrayList<>();

        for (ArtifactAppEntity artifact : projectAppEntity.artifacts) {
            String artifactType = artifact.type;
            if (type2Artifacts.containsKey(artifactType)) {
                type2Artifacts.get(artifactType).add(artifact);
            } else {
                List<ArtifactAppEntity> artifacts = new ArrayList<>();
                artifacts.add(artifact);
                type2Artifacts.put(artifactType, artifacts);
            }
            name2artifact.put(artifact.name, artifact);
        }

        for (String artifactType : type2Artifacts.keySet()) {
            String fileName = String.format("%s.csv", artifactType);
            String pathToFile = ProjectPaths.getPathToProjectFile(project, fileName);

            File artifactFile = new File(pathToFile);
            List<ArtifactAppEntity> artifacts = type2Artifacts.get(artifactType);
            fileCreatorService.writeArtifactsToFile(pathToFile, artifacts);

            projectFiles.add(artifactFile);
        }

        for (TraceAppEntity trace : projectAppEntity.traces) {
            String sourceType = name2artifact.get(trace.sourceName).type;
            String targetType = name2artifact.get(trace.targetName).type;

            if (type2Traces.containsKey(sourceType)) {
                if (type2Traces.containsKey(targetType)) {
                    type2Traces.get(sourceType).get(targetType).add(trace);
                } else {
                    Map<String, List<TraceAppEntity>> sourceTypeTraces = type2Traces.get(sourceType);
                    sourceTypeTraces.put(targetType, new ArrayList<>(List.of(trace)));
                }
            } else {
                Map<String, List<TraceAppEntity>> sourceTypeTraces = new Hashtable<>();
                sourceTypeTraces.put(targetType, new ArrayList<>(List.of(trace)));
                type2Traces.put(sourceType, sourceTypeTraces);
            }
        }

        for (String sourceType : type2Traces.keySet()) {
            for (String targetType : type2Traces.get(sourceType).keySet()) {
                String fileName = String.format("%s2%s.csv", sourceType, targetType);
                String pathToFile = ProjectPaths.getPathToProjectFile(project, fileName);
                File traceFile = new File(pathToFile);
                List<TraceAppEntity> traces = type2Traces.get(sourceType).get(targetType);
                fileCreatorService.writeTracesToFile(pathToFile, traces);

                projectFiles.add(traceFile);
            }
        }

        // TODO: Write tim.json
        return projectFiles;
    }
}
