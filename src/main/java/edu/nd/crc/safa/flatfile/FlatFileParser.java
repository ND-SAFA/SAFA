package edu.nd.crc.safa.flatfile;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Iterator;

import edu.nd.crc.safa.constants.ProjectVariables;
import edu.nd.crc.safa.entities.Project;
import edu.nd.crc.safa.entities.ProjectVersion;
import edu.nd.crc.safa.output.error.ServerError;
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
     * @param project       the project identifier to be associated with the files specified.
     * @param pathToTIMFile path to the TIM.json file in local storage (see ProjectPaths.java)
     * @throws ServerError any error occuring while parsing TIM.json or associated files.
     */
    public void parseProject(Project project,
                             ProjectVersion projectVersion,
                             String pathToTIMFile) throws ServerError {
        try {
            String TIMFileContent = new String(Files.readAllBytes(Paths.get(pathToTIMFile)));
            JSONObject TIMFileJson = FileUtilities.toLowerCase(new JSONObject(TIMFileContent));

            artifactFileParser.parseArtifactFiles(project, TIMFileJson.getJSONObject(ProjectVariables.DATAFILES_PARAM));

            for (Iterator keyIterator = TIMFileJson.keys(); keyIterator.hasNext(); ) {
                String traceMatrixKey = keyIterator.next().toString();
                if (!traceMatrixKey.toLowerCase().equals(ProjectVariables.DATAFILES_PARAM)) {
                    traceFileParser.parseTraceMatrixJson(project,
                        projectVersion,
                        TIMFileJson.getJSONObject(traceMatrixKey));
                }
            }
        } catch (IOException | JSONException e) {
            throw new ServerError("parsing TIM file", e);
        }
    }
}
