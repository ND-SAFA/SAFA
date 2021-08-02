package edu.nd.crc.safa.importer.flatfile.parser;

import java.io.FileReader;
import java.io.IOException;
import java.io.Reader;
import java.util.ArrayList;
import java.util.List;

import edu.nd.crc.safa.constants.ProjectPaths;
import edu.nd.crc.safa.database.entities.Artifact;
import edu.nd.crc.safa.database.entities.ArtifactBody;
import edu.nd.crc.safa.database.entities.ArtifactFile;
import edu.nd.crc.safa.database.entities.ArtifactType;
import edu.nd.crc.safa.database.entities.ParserError;
import edu.nd.crc.safa.database.entities.Project;
import edu.nd.crc.safa.database.entities.ProjectVersion;
import edu.nd.crc.safa.error.ServerError;

import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVParser;
import org.apache.commons.csv.CSVRecord;
import org.hibernate.Session;
import org.hibernate.SessionFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

/**
 * Responsible for parsing flat files including reading,
 * validating, and storing their data.
 */
@Component
public class ArtifactFileParser {

    SessionFactory sessionFactory;
    private final String ID_PARAM = "id";
    private final String SUMMARY_PARAM = "summary";
    private final String CONTENT_PARAM = "content";

    @Autowired
    public ArtifactFileParser(SessionFactory sessionFactory) {
        this.sessionFactory = sessionFactory;
    }


    public void parseArtifactFile(Project project,
                                  ProjectVersion projectVersion,
                                  ArtifactType artifactType,
                                  String fileName) throws ServerError {

        CSVParser fileParser;
        try {
            String pathToFile = ProjectPaths.getPathToProjectFlatFile(project.getProjectId().toString(), fileName);
            Reader in = new FileReader(pathToFile);

            CSVFormat fileFormat = CSVFormat.DEFAULT.builder().setIgnoreHeaderCase(true).build();
            fileParser = new CSVParser(in, fileFormat);
            if (!hasArtifactFileColumns(fileParser.getHeaderNames())) {
                String error = "Artifact file %s missing at least one required column: id, summary, content";
                throw new ServerError(String.format(error, fileName));
            }

            Session session = sessionFactory.openSession();
            ArtifactFile artifactFile = new ArtifactFile(project, artifactType, fileName);
            session.save(artifactFile);

            saveArtifactRecords(project, projectVersion, artifactType, fileParser);
        } catch (IOException e) {
            throw new ServerError("parsing artifact file", e);
        }
    }

    private void saveArtifactRecords(Project project,
                                     ProjectVersion projectVersion,
                                     ArtifactType artifactType,
                                     CSVParser parsedFile) throws ServerError {
        List<CSVRecord> artifactRecords;
        try {
            artifactRecords = parsedFile.getRecords();
        } catch (IOException e) {
            throw new ServerError("parsing artifact file", e);
        }

        for (CSVRecord artifactRecord : artifactRecords) {

            String artifactId = artifactRecord.get(ID_PARAM);
            String artifactSummary = artifactRecord.get(SUMMARY_PARAM);
            String artifactContent = artifactRecord.get(CONTENT_PARAM);

            Session session = sessionFactory.openSession();
            try {
                Artifact artifact = new Artifact(project, artifactType, artifactId);
                ArtifactBody artifactBody = new ArtifactBody(artifact,
                    projectVersion, artifactSummary, artifactContent);

                session.save(artifact);
                session.save(artifactBody);
            } catch (Exception e) {
                ParserError parserError = new ParserError(project,
                    artifactType.getName(),
                    parsedFile.getCurrentLineNumber(),
                    e.getMessage());
                session.save(parserError);
            } finally {
                session.close();
            }
        }
    }

    private boolean hasArtifactFileColumns(List<String> headerNames) {
        List<String> headerNamesLower = toLowerCase(headerNames);

        return headerNamesLower.contains(ID_PARAM)
            && headerNamesLower.contains(SUMMARY_PARAM)
            && headerNamesLower.contains(CONTENT_PARAM);
    }

    private List<String> toLowerCase(List<String> words) {
        List<String> result = new ArrayList<>();
        for (String word : words) {
            result.add(word.toLowerCase());
        }
        return result;
    }
}
