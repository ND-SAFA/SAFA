package edu.nd.crc.safa.importer.flatfile.parser;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Iterator;

import edu.nd.crc.safa.database.entities.ArtifactFile;
import edu.nd.crc.safa.database.entities.ArtifactType;
import edu.nd.crc.safa.database.entities.Project;
import edu.nd.crc.safa.database.entities.ProjectVersion;
import edu.nd.crc.safa.error.ServerError;

import org.hibernate.Session;
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
     * @param project    the project identifier to be associated with the files specified.
     * @param pathToFile path to the TIM.json file in local storage (see ProjectPaths.java)
     * @throws ServerError any error occuring while parsing TIM.json or associated files.
     */
    public void parseTIMFile(Project project, String pathToFile) throws ServerError {
        try {
            String fileContent = new String(Files.readAllBytes(Paths.get(pathToFile)));
            JSONObject fileJson = toLowerCase(new JSONObject(fileContent));

            for (Iterator keyIterator = fileJson.keys(); keyIterator.hasNext(); ) {
                String fileKey = keyIterator.next().toString();
                if (fileKey.toLowerCase().equals(DATAFILES_PARAM)) {
                    parseDataFiles(project, fileJson.getJSONObject(DATAFILES_PARAM));
                } else {
                    traceFileParser.parseTraceMatrix(project, fileJson.getJSONObject(fileKey));
                }
            }
        } catch (IOException | JSONException e) {
            throw new ServerError("parsing TIM file", e);
        }
    }

    private void parseDataFiles(Project project,
                                JSONObject dataFilesIterator) throws JSONException, ServerError {
        for (Iterator keyIterator = dataFilesIterator.keys(); keyIterator.hasNext(); ) {
            String artifactTypeName = keyIterator.next().toString();
            String artifactFileName = dataFilesIterator
                .getJSONObject(artifactTypeName)
                .getString("file");

            Session session = sessionFactory.openSession();
            ArtifactType artifactType = new ArtifactType(project, artifactTypeName);
            session.save(artifactType);
            ArtifactFile newFile = new ArtifactFile(project, artifactType, artifactFileName);
            session.save(newFile);
            ProjectVersion firstProjectVersion = new ProjectVersion(project);
            session.save(firstProjectVersion);
            artifactFileParser.parseArtifactFile(project, firstProjectVersion, artifactType, artifactFileName);
        }
    }

    private static JSONObject toLowerCase(JSONObject jsonObject) throws JSONException {
        JSONObject result = new JSONObject();
        Iterator keys = jsonObject.keys();

        while (keys.hasNext()) {
            String key = keys.next().toString();
            result.put(key.toLowerCase(), jsonObject.get(key));
        }
        return result;
    }
}
