package edu.nd.crc.safa.importer.flatfile;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Iterator;

import edu.nd.crc.safa.database.entities.Project;
import edu.nd.crc.safa.database.entities.ProjectVersion;
import edu.nd.crc.safa.error.ServerError;

import org.hibernate.SessionFactory;
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

    SessionFactory sessionFactory;
    ArtifactFileParser artifactFileParser;
    TraceFileParser traceFileParser;

    private final String DATAFILES_PARAM = "datafiles";

    @Autowired
    public FlatFileParser(SessionFactory sessionFactory,
                          ArtifactFileParser artifactFileParser,
                          TraceFileParser traceFileParser) {
        this.sessionFactory = sessionFactory;
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
            String fileContent = new String(Files.readAllBytes(Paths.get(pathToTIMFile)));
            JSONObject fileJson = FileUtilities.toLowerCase(new JSONObject(fileContent));

            artifactFileParser.parseArtifactFiles(project, fileJson.getJSONObject(DATAFILES_PARAM));

            for (Iterator keyIterator = fileJson.keys(); keyIterator.hasNext(); ) {
                String nextKey = keyIterator.next().toString();
                if (!nextKey.toLowerCase().equals(DATAFILES_PARAM)) {
                    traceFileParser.parseTraceMatrixJson(project,
                        projectVersion,
                        fileJson.getJSONObject(nextKey));
                }
            }
        } catch (IOException | JSONException e) {
            throw new ServerError("parsing TIM file", e);
        }
    }
}
