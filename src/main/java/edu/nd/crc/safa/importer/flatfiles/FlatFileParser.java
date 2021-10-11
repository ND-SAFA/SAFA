package edu.nd.crc.safa.importer.flatfiles;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Iterator;

import edu.nd.crc.safa.config.ProjectVariables;
import edu.nd.crc.safa.server.db.entities.sql.ProjectVersion;
import edu.nd.crc.safa.server.messages.ServerError;
import edu.nd.crc.safa.utilities.FileUtilities;

import org.json.JSONException;
import org.json.JSONObject;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

/**
 * Responsible for parsing flat files including reading,
 * validating, and storing their data.
 */
@Component
public class FlatFileParser {

    ArtifactFileParser artifactFileParser;
    TraceFileParser traceFileParser;

    @Autowired
    public FlatFileParser(ArtifactFileParser artifactFileParser,
                          TraceFileParser traceFileParser) {
        this.artifactFileParser = artifactFileParser;
        this.traceFileParser = traceFileParser;
    }

    /**
     * Constructs a project from the specification in TIM.json file.
     * Note, this methods expects all files to be stored in local storage
     * before processing.
     *
     * @param projectVersion the project version to be associated with the files specified.
     * @param pathToTIMFile  path to the TIM.json file in local storage (see ProjectPaths.java)
     * @throws ServerError any error occuring while parsing TIM.json or associated files.
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
            throw new ServerError("parsing TIM file", e);
        }
    }
}
