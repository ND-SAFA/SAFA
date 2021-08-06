package edu.nd.crc.safa.services;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Iterator;
import java.util.List;
import javax.naming.OperationNotSupportedException;

import edu.nd.crc.safa.configuration.ProjectPaths;
import edu.nd.crc.safa.configuration.ProjectVariables;
import edu.nd.crc.safa.entities.ApplicationActivity;
import edu.nd.crc.safa.entities.ParserError;
import edu.nd.crc.safa.entities.Project;
import edu.nd.crc.safa.entities.ProjectVersion;
import edu.nd.crc.safa.entities.TraceType;
import edu.nd.crc.safa.flatfiles.FlatFileParser;
import edu.nd.crc.safa.flatfiles.TraceFileParser;
import edu.nd.crc.safa.flatfiles.TraceLinkGenerator;
import edu.nd.crc.safa.repositories.ArtifactRepository;
import edu.nd.crc.safa.repositories.ParserErrorRepository;
import edu.nd.crc.safa.repositories.ProjectVersionRepository;
import edu.nd.crc.safa.repositories.TraceLinkRepository;
import edu.nd.crc.safa.responses.FlatFileResponse;
import edu.nd.crc.safa.responses.ServerError;
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
    TraceLinkRepository traceLinkRepository;

    @Autowired
    public FlatFileService(FlatFileParser flatFileParser,
                           TraceLinkGenerator traceLinkGenerator,
                           ProjectVersionRepository projectVersionRepository,
                           ParserErrorRepository parserErrorRepository,
                           ArtifactRepository artifactRepository,
                           TraceLinkRepository traceLinkRepository) {
        this.traceLinkGenerator = traceLinkGenerator;
        this.flatFileParser = flatFileParser;
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
     * @return FlatFileResponse containing uploaded, parsed, and generated files.
     * @throws ServerError on any parsing error of tim.json, artifacts, or trace links
     */
    public FlatFileResponse parseFlatFiles(Project project, MultipartFile[] files) throws ServerError {
        List<String> uploadedFiles = this.uploadFlatFiles(project, Arrays.asList(files));
        ProjectVersion newProjectVersion = new ProjectVersion(project);
        this.projectVersionRepository.save(newProjectVersion);
        this.createProjectFromTIMFile(project, newProjectVersion);

        FlatFileResponse response = new FlatFileResponse();
        response.setUploadedFiles(uploadedFiles);
        //TODO: set generated files
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
            if (!traceMatrixKey.equalsIgnoreCase(ProjectVariables.DATAFILES_PARAM)) {
                boolean isGenerated = timJson.has("generateLinks") && timJson.getBoolean("generateLinks");
                if (isGenerated) {
                    this.traceFileParser.parseTraceMatrixDefinition(projectVersion,
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

    public File[] getUploadedFiles(Project project) {
        File directory = new File(ProjectPaths.getPathToUploadedFiles(project));
        File[] filesInDirectory = directory.listFiles();
        if (filesInDirectory == null) {
            return new File[]{};
        }
        return filesInDirectory;
    }

    public void getFileInfo() throws OperationNotSupportedException {
        //TODO: what kind of information is needed?
        throw new OperationNotSupportedException("getting file information is under construction");
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
        this.flatFileParser.parseProject(projectVersion, pathToFile);
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
