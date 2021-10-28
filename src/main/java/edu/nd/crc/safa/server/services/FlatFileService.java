package edu.nd.crc.safa.server.services;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.config.ProjectVariables;
import edu.nd.crc.safa.importer.flatfiles.FlatFileParser;
import edu.nd.crc.safa.importer.flatfiles.TraceLinkGenerator;
import edu.nd.crc.safa.server.db.entities.sql.Project;
import edu.nd.crc.safa.server.db.entities.sql.ProjectVersion;
import edu.nd.crc.safa.server.db.repositories.ArtifactBodyRepository;
import edu.nd.crc.safa.server.db.repositories.ArtifactRepository;
import edu.nd.crc.safa.server.db.repositories.ParserErrorRepository;
import edu.nd.crc.safa.server.db.repositories.ProjectVersionRepository;
import edu.nd.crc.safa.server.db.repositories.TraceLinkRepository;
import edu.nd.crc.safa.server.messages.ProjectCreationResponse;
import edu.nd.crc.safa.server.messages.ServerError;
import edu.nd.crc.safa.utilities.OSHelper;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

/**
 * Responsible for exposing an API for uploading,
 * parsing, and deleting flat files.
 */
@Service
public class FlatFileService {

    FlatFileParser flatFileParser;
    TraceLinkGenerator traceLinkGenerator;
    ProjectVersionRepository projectVersionRepository;
    ParserErrorRepository parserErrorRepository;
    ArtifactRepository artifactRepository;
    ArtifactBodyRepository artifactBodyRepository;
    TraceLinkRepository traceLinkRepository;

    ProjectService projectService;
    ParserErrorService parserErrorService;
    WarningService warningService;

    @Autowired
    public FlatFileService(FlatFileParser flatFileParser,
                           TraceLinkGenerator traceLinkGenerator,
                           ProjectVersionRepository projectVersionRepository,
                           ParserErrorRepository parserErrorRepository,
                           ArtifactRepository artifactRepository,
                           TraceLinkRepository traceLinkRepository,
                           ArtifactBodyRepository artifactBodyRepository,
                           ProjectService projectService,
                           ParserErrorService parserErrorService,
                           WarningService warningService) {
        this.traceLinkGenerator = traceLinkGenerator;
        this.flatFileParser = flatFileParser;
        this.projectVersionRepository = projectVersionRepository;
        this.parserErrorRepository = parserErrorRepository;
        this.artifactRepository = artifactRepository;
        this.traceLinkRepository = traceLinkRepository;
        this.artifactBodyRepository = artifactBodyRepository;
        this.projectService = projectService;
        this.parserErrorService = parserErrorService;
        this.warningService = warningService;
    }

    /**
     * Responsible for creating a project from given flat files. This includes
     * parsing tim.json, creating artifacts, and their trace links.
     *
     * @param project        the project whose artifacts and trace links should be associated with
     * @param projectVersion - the version that the artifacts and errors will be associated with.
     * @param files          the flat files defining the project
     * @return FlatFileResponse containing uploaded, parsed, and generated files.
     * @throws ServerError on any parsing error of tim.json, artifacts, or trace links
     */
    public ProjectCreationResponse parseAndUploadFlatFiles(Project project,
                                                           ProjectVersion projectVersion,
                                                           MultipartFile[] files)
        throws ServerError {
        this.uploadFlatFiles(project, Arrays.asList(files));
        this.parseProjectFilesFromTIM(project, projectVersion);
        return this.projectService.retrieveAndCreateProjectResponse(projectVersion);
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
                File parentFile = newFile.getParentFile();
                parentFile.mkdirs();
                newFile.createNewFile();
                requestFile.transferTo(newFile);
                uploadedFiles.add(requestFile.getOriginalFilename());

            } catch (IOException e) {
                String error = String.format("Could not upload file: %s", requestFile.getOriginalFilename());
                throw new ServerError(error, e);
            }
        }
        return uploadedFiles;
    }

    private void parseProjectFilesFromTIM(Project project, ProjectVersion projectVersion) throws ServerError {
        String pathToFile = ProjectPaths.getPathToFlatFile(project, ProjectVariables.TIM_FILENAME);
        if (!Files.exists(Paths.get(pathToFile))) {
            throw new ServerError("TIM.json file was not uploaded for this project");
        }
        this.flatFileParser.parseProject(projectVersion, pathToFile);
    }
}
