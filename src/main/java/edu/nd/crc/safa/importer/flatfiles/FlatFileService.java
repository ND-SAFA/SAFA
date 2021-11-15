package edu.nd.crc.safa.importer.flatfiles;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Iterator;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.config.ProjectVariables;
import edu.nd.crc.safa.server.entities.api.ServerError;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.utilities.FileUtilities;

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

    ArtifactFileParser artifactFileParser;
    TraceFileParser traceFileParser;

    @Autowired
    public FlatFileService(ArtifactFileParser artifactFileParser,
                           TraceFileParser traceFileParser) {
        this.artifactFileParser = artifactFileParser;
        this.traceFileParser = traceFileParser;
    }

    public void parseProjectFilesFromTIM(ProjectVersion projectVersion) throws ServerError {
        Project project = projectVersion.getProject();
        String pathToFile = ProjectPaths.getPathToFlatFile(project, ProjectVariables.TIM_FILENAME);
        if (!Files.exists(Paths.get(pathToFile))) {
            throw new ServerError("TIM.json file was not uploaded for this project");
        }
        this.parseProject(projectVersion, pathToFile);
    }

    /**
     * Constructs a project from the specification in TIM.json file.
     * Note, this route expects all files to be stored in local storage
     * before processing.
     *
     * @param projectVersion the project version to be associated with the files specified.
     * @param pathToTIMFile  path to the TIM.json file in local storage (see ProjectPaths.java)
     * @throws ServerError any error occurring while parsing TIM.json or associated files.
     */
    public void parseProject(ProjectVersion projectVersion,
                             String pathToTIMFile) throws ServerError {
        try {
            String TIMFileContent = new String(Files.readAllBytes(Paths.get(pathToTIMFile)));
            JSONObject timFileJson = FileUtilities.toLowerCase(new JSONObject(TIMFileContent));
            JSONObject dataFilesJson = timFileJson.getJSONObject(ProjectVariables.DATAFILES_PARAM);
            artifactFileParser.parseArtifactFiles(projectVersion, dataFilesJson);

            for (Iterator<String> keyIterator = timFileJson.keys(); keyIterator.hasNext(); ) {
                String traceMatrixKey = keyIterator.next();
                if (traceMatrixKey.equalsIgnoreCase(ProjectVariables.DATAFILES_PARAM)) {
                    continue;
                }
                traceFileParser.parseTraceMatrixDefinition(projectVersion,
                    timFileJson.getJSONObject(traceMatrixKey));
            }
        } catch (IOException | JSONException e) {
            throw new ServerError("An error occurred while parsing TIM file.", e);
        }
    }
}
