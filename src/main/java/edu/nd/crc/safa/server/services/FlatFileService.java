package edu.nd.crc.safa.server.services;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Iterator;
import java.util.List;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.config.ProjectVariables;
import edu.nd.crc.safa.db.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.db.entities.sql.Project;
import edu.nd.crc.safa.db.entities.sql.ProjectVersion;
import edu.nd.crc.safa.db.entities.sql.TraceType;
import edu.nd.crc.safa.db.repositories.ArtifactBodyRepository;
import edu.nd.crc.safa.db.repositories.ArtifactRepository;
import edu.nd.crc.safa.db.repositories.ParserErrorRepository;
import edu.nd.crc.safa.db.repositories.ProjectVersionRepository;
import edu.nd.crc.safa.db.repositories.TraceLinkRepository;
import edu.nd.crc.safa.importer.flatfiles.FlatFileParser;
import edu.nd.crc.safa.importer.flatfiles.TraceFileParser;
import edu.nd.crc.safa.importer.flatfiles.TraceLinkGenerator;
import edu.nd.crc.safa.server.responses.FlatFileResponse;
import edu.nd.crc.safa.server.responses.ProjectCreationResponse;
import edu.nd.crc.safa.server.responses.ProjectErrors;
import edu.nd.crc.safa.server.responses.ServerError;
import edu.nd.crc.safa.utilities.FileUtilities;
import edu.nd.crc.safa.utilities.OSHelper;

import org.json.JSONObject;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.FileSystemResource;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

/**
 * Responsible for exposing an API for uploading,
 * parsing, and deleting flat files.
 */
@Service
public class FlatFileService {

    private final String SEPARATOR = "-------------------------------";
    FlatFileParser flatFileParser;
    TraceLinkGenerator traceLinkGenerator;
    TraceFileParser traceFileParser;
    ProjectVersionRepository projectVersionRepository;
    ParserErrorRepository parserErrorRepository;
    ArtifactRepository artifactRepository;
    ArtifactBodyRepository artifactBodyRepository;
    TraceLinkRepository traceLinkRepository;

    ProjectService projectService;
    ParserErrorService parserErrorService;

    @Autowired
    public FlatFileService(FlatFileParser flatFileParser,
                           TraceLinkGenerator traceLinkGenerator,
                           ProjectVersionRepository projectVersionRepository,
                           ParserErrorRepository parserErrorRepository,
                           ArtifactRepository artifactRepository,
                           TraceLinkRepository traceLinkRepository,
                           ArtifactBodyRepository artifactBodyRepository,
                           ProjectService projectService,
                           ParserErrorService parserErrorService) {
        this.traceLinkGenerator = traceLinkGenerator;
        this.flatFileParser = flatFileParser;
        this.projectVersionRepository = projectVersionRepository;
        this.parserErrorRepository = parserErrorRepository;
        this.artifactRepository = artifactRepository;
        this.traceLinkRepository = traceLinkRepository;
        this.artifactBodyRepository = artifactBodyRepository;
        this.projectService = projectService;
        this.parserErrorService = parserErrorService;
    }

    /**
     * Responsible for creating a project from given flat files. This includes
     * parsing tim.json, creating artifacts, and their trace links.
     *
     * @param project the project whose artifacts and trace links should be associated with
     * @param files   the flat files defining the project
     * @return FlatFileResponse containing uploaded, parsed, and generated files.
     * @throws ServerError on any parsing error of tim.json, artifacts, or trace links
     */
    public ProjectCreationResponse createProjectFromFlatFiles(Project project, MultipartFile[] files)
        throws ServerError {
        // TODO: Move uploading into creation method
        List<String> uploadedFiles = this.uploadFlatFiles(project, Arrays.asList(files));

        ProjectVersion newProjectVersion = new ProjectVersion(project);
        this.projectVersionRepository.save(newProjectVersion);
        this.createProjectFromTIMFile(project, newProjectVersion);
        // TODO: Uncomment when in-memory works synchronizeService.projectPull(newProjectVersion);

        FlatFileResponse response = new FlatFileResponse();
        response.setUploadedFiles(uploadedFiles);

        ProjectAppEntity projectAppEntity =
            this.projectService.createApplicationEntity(newProjectVersion);
        ProjectErrors projectErrors = this.parserErrorService.collectionProjectErrors(newProjectVersion);
        return new ProjectCreationResponse(projectAppEntity, projectErrors);
    }

    public void generateLinks(Project project, ProjectVersion projectVersion) throws ServerError {
        String pathToTIMFile = ProjectPaths.getPathToFlatFile(project, ProjectVariables.TIM_FILENAME);
        String TIMFileContent;
        try {
            TIMFileContent = new String(Files.readAllBytes(Paths.get(pathToTIMFile)));
        } catch (IOException e) {
            throw new ServerError("Could not read TIM.json file.", e);
        }
        //TODO: Generalize with FlatFileParser.parseProject
        JSONObject timJson = FileUtilities.toLowerCase(new JSONObject(TIMFileContent));
        for (Iterator keyIterator = timJson.keys(); keyIterator.hasNext(); ) {
            String traceMatrixKey = keyIterator.next().toString();
            if (!traceMatrixKey.equalsIgnoreCase(ProjectVariables.DATAFILES_PARAM)) {
                boolean isGenerated = timJson.has("generateLinks") && timJson.getBoolean("generateLinks");
                if (isGenerated) {
                    this.traceFileParser.parseTraceMatrixDefinition(projectVersion,
                        timJson.getJSONObject(traceMatrixKey));
                }
            }
        }
    }

    public FileSystemResource getUploadedFile(Project project, String file) {
        return new FileSystemResource(new File(ProjectPaths.getPathToFlatFile(project, file)));
    }

    public void clearUploadedFiles(Project project) throws ServerError {
        OSHelper.clearOrCreateDirectory(ProjectPaths.getPathToUploadedFiles(project));
        this.artifactRepository.deleteAllByProject(project);
    }

    public void clearGeneratedFiles(Project project) throws ServerError {
        OSHelper.clearOrCreateDirectory(ProjectPaths.getPathToGeneratedFiles(project));
        this.traceLinkRepository.deleteAllByProjectAndTraceType(project, TraceType.GENERATED);
    }

    public List<String> uploadFlatFiles(Project project, List<MultipartFile> requestFiles) throws ServerError {
        String pathToStorage = ProjectPaths.getPathToStorage(project);
        OSHelper.clearOrCreateDirectory(pathToStorage);

        List<String> uploadedFiles = new ArrayList<>();
        for (MultipartFile requestFile : requestFiles) {
            try {
                String pathToFile = ProjectPaths.getPathToFlatFile(project, requestFile.getOriginalFilename());
                Path pathToUploadedFile = Paths.get(pathToFile);
                File newFile = new File(pathToUploadedFile.toString());
                newFile.getParentFile().mkdirs();
                newFile.createNewFile();
                requestFile.transferTo(newFile);
                uploadedFiles.add(requestFile.getOriginalFilename());

            } catch (IOException e) {
                throw new ServerError("Could not upload file: " + requestFile.getOriginalFilename(), e);
            }
        }
        return uploadedFiles;
    }

    private void createProjectFromTIMFile(Project project, ProjectVersion projectVersion) throws ServerError {
        String pathToFile = ProjectPaths.getPathToFlatFile(project, ProjectVariables.TIM_FILENAME);
        if (!Files.exists(Paths.get(pathToFile))) {
            throw new ServerError("TIM.json file was not uploaded for this project");
        }
        this.flatFileParser.parseProject(projectVersion, pathToFile);
        // TODO: return generated files
    }
}
