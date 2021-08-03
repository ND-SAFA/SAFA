package edu.nd.crc.safa.services;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

import javax.naming.OperationNotSupportedException;

import edu.nd.crc.safa.constants.ProjectPaths;
import edu.nd.crc.safa.constants.ProjectVariables;
import edu.nd.crc.safa.database.entities.ApplicationActivity;
import edu.nd.crc.safa.database.entities.ParserError;
import edu.nd.crc.safa.database.entities.Project;
import edu.nd.crc.safa.database.entities.ProjectVersion;
import edu.nd.crc.safa.database.entities.TraceType;
import edu.nd.crc.safa.database.repositories.ArtifactRepository;
import edu.nd.crc.safa.database.repositories.ParserErrorRepository;
import edu.nd.crc.safa.database.repositories.ProjectVersionRepository;
import edu.nd.crc.safa.database.repositories.TraceLinkRepository;
import edu.nd.crc.safa.flatfile.FlatFileParser;
import edu.nd.crc.safa.flatfile.TraceFileParser;
import edu.nd.crc.safa.flatfile.TraceLinkGenerator;
import edu.nd.crc.safa.importer.MySQL;
import edu.nd.crc.safa.server.error.ServerError;
import edu.nd.crc.safa.server.responses.FlatFileResponse;
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

    FlatFileParser flatFileParser;
    TraceLinkGenerator traceLinkGenerator;
    TraceFileParser traceFileParser;

    TraceMatrixService traceMatrixService;
    TimArtifactService timArtifactService;

    ProjectVersionRepository projectVersionRepository;
    ParserErrorRepository parserErrorRepository;
    ArtifactRepository artifactRepository;
    TraceLinkRepository traceLinkRepository;

    private final String SEPARATOR = "-------------------------------";


    @Autowired
    public FlatFileService(FlatFileParser flatFileParser,
                           TraceMatrixService traceMatrixService,
                           TraceLinkGenerator traceLinkGenerator,
                           TimArtifactService timArtifactService,
                           ProjectVersionRepository projectVersionRepository,
                           ParserErrorRepository parserErrorRepository,
                           ArtifactRepository artifactRepository,
                           TraceLinkRepository traceLinkRepository) {
        this.traceLinkGenerator = traceLinkGenerator;
        this.traceMatrixService = traceMatrixService;
        this.flatFileParser = flatFileParser;
        this.timArtifactService = timArtifactService;
        this.projectVersionRepository = projectVersionRepository;
        this.parserErrorRepository = parserErrorRepository;
        this.artifactRepository = artifactRepository;
        this.traceLinkRepository = traceLinkRepository;
    }

    /**
     * Responsible for creating a project from given flat files. This includes
     * parsing tim.json, creating artifacts, and their trace links.
     *
     * @param project the project whose artifacts and trace links should be associated with
     * @param files   the flat files defining the project
     * @throws ServerError on any parsing error of tim.json, artifacts, or trace links
     */
    public FlatFileResponse parseFlatFiles(Project project, MultipartFile[] files) throws ServerError {
        List<String> uploadedFiles = this.uploadFlatFiles(project, files);
        ProjectVersion newProjectVersion = new ProjectVersion();
        this.projectVersionRepository.save(newProjectVersion);
        this.createProjectFromTIMFile(project, newProjectVersion);

        FlatFileResponse response = new FlatFileResponse();
        response.setUploadedFiles(uploadedFiles);
        return response;
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
            if (!traceMatrixKey.toLowerCase().equals(ProjectVariables.DATAFILES_PARAM)) {
                boolean isGenerated = timJson.has("generateLinks") && timJson.getBoolean("generateLinks");
                if (isGenerated) {
                    this.traceFileParser.parseTraceMatrixJson(project, projectVersion,
                        timJson.getJSONObject(traceMatrixKey));
                }
            }
        }
    }

    public String getLinkErrorLog(Project project) throws ServerError {
        return "Trace Link Error Log" + SEPARATOR + "\n" + getErrorLog(project,
            ApplicationActivity.PARSING_TRACE_MATRIX);
    }

    /**
     * Returns list of parsing error for given project if it was created
     * through flat files.
     *
     * @param project the project whose upload errors are associated
     * @return formatted string containing all parsing errors
     */
    public String getUploadErrorLog(Project project) {
        return "TIM.json error log " + SEPARATOR + "\n"
            + getErrorLog(project, ApplicationActivity.PARSING_TIM)
            + "Artifact parsing error log" + SEPARATOR + "\n"
            + getErrorLog(project, ApplicationActivity.PARSING_TRACE_MATRIX);
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

    public MySQL.FileInfo getFileInfo() throws OperationNotSupportedException {
        //TODO: what kind of information is needed?
        throw new OperationNotSupportedException("getting file information is under construction");
    }

    private List<String> uploadFlatFiles(Project project, MultipartFile[] files) throws ServerError {
        String pathToStorage = ProjectPaths.getPathToStorage(project);
        OSHelper.clearOrCreateDirectory(pathToStorage);

        List<String> uploadedFiles = new ArrayList<>();
        for (MultipartFile file : files) {
            try {
                String pathToFile = ProjectPaths.getPathToFlatFile(project, file.getOriginalFilename());
                byte[] fileContent = file.getBytes();
                Files.write(Paths.get(pathToFile), fileContent);
                uploadedFiles.add(file.getOriginalFilename());
            } catch (IOException e) {
                throw new ServerError("Could not upload file: " + file.getOriginalFilename());
            }
        }
        return uploadedFiles;
    }

    private void createProjectFromTIMFile(Project project, ProjectVersion projectVersion) throws ServerError {
        String pathToFile = ProjectPaths.getPathToFlatFile(project, ProjectVariables.TIM_FILENAME);
        this.flatFileParser.parseProject(project, projectVersion, pathToFile);
        // TODO: return generated files
    }

    private String getErrorLog(Project project, ApplicationActivity activity) {
        List<ParserError> parserErrors = this.parserErrorRepository.findByProject(project);

        StringBuilder result = new StringBuilder();
        for (ParserError error : parserErrors) {
            if (error.getActivity() == activity) {
                result.append(error.toLogFormat());
            }
        }
        return result.toString();
    }
}
