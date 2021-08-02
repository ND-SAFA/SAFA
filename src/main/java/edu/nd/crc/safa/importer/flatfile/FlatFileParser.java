package edu.nd.crc.safa.importer.flatfile;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.io.Serializable;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;

import edu.nd.crc.safa.database.entities.ArtifactType;
import edu.nd.crc.safa.database.entities.Project;
import edu.nd.crc.safa.database.entities.TIMFile;
import edu.nd.crc.safa.error.ServerError;

import com.jsoniter.JsonIterator;
import org.hibernate.Session;
import org.hibernate.SessionFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class FlatFileParser {

    SessionFactory sessionFactory;
    private final String DATAFILES_PARAM = "datafiles";

    @Autowired
    public FlatFileParser(SessionFactory sessionFactory) {
        this.sessionFactory = sessionFactory;
    }

    public void parseTimFile(Project project, String pathToFile) throws ServerError {
        try {
            String fileContent = new String(Files.readAllBytes(Paths.get(pathToFile)));
            JsonIterator iterator = JsonIterator.parse(fileContent);

            for (String field = iterator.readObject(); field != null; field = iterator.readObject()) {
                if (field.toLowerCase().equals(DATAFILES_PARAM)) {
                    parseDataFiles(project, iterator);
                } else {
                    parseTraceMatrix(field, iterator);
                }
            }
        } catch (IOException e) {
            throw new ServerError("parsing TIM file", e);
        }
    }

    private void parseDataFiles(Project project, JsonIterator dataFilesIterator) throws ServerError {
        try {
            for (String artifactTypeName = dataFilesIterator.readObject();
                 artifactTypeName != null;
                 artifactTypeName = dataFilesIterator.readObject()) {

                dataFilesIterator.readObject();
                String artifactTypeFileKey = dataFilesIterator.readObject();
                if (!artifactTypeFileKey.toLowerCase().equals("file")) {
                    String error = String.format("Unexpected field [%s] in datafile type %s.",
                        artifactTypeFileKey,
                        artifactTypeName);
                    throw new ServerError(error);
                }
                String artifactFileName = dataFilesIterator.readString();

                Session session = sessionFactory.openSession();
                ArtifactType artifactType = new ArtifactType(project, artifactTypeName);
                Serializable artifactId = session.save(artifactType);
                TIMFile newFile = new TIMFile(project, artifactType, artifactFileName);
                session.save(newFile);
            }
        } catch (IOException e) {
            throw new ServerError("parsing tim.json file", e);
        }
    }

    public void parseRegularFile(String fileName, String fullPath) throws ServerError {
        try {
            BufferedReader uploadedFileReader = new BufferedReader(new FileReader(fullPath));
            String[] headers = uploadedFileReader.readLine().split(",");

            if (headers.length == 2) {
                parseBiHeaderFile(fileName, fullPath, headers);
            } else if (headers.length == 3) {
                parseTriHeaderFile(fileName, fullPath, headers);
            } else {
                throw new ServerError("unrecognized file type: " + fileName);
            }
        } catch (IOException e) {
            throw new ServerError("parse regular file", e);
        }
    }

    private void parseTriHeaderFile(Project project,
                                    String fileName,
                                    String fullPath,
                                    String[] headers) throws ServerError {
        boolean id = false;
        boolean summary = false;
        boolean content = false;
        List<String> cols = new ArrayList<>();

        for (String header : headers) {
            switch (header.toLowerCase()) {
                case "id":
                    id = true;
                    cols.add("id");
                    break;
                case "summary":
                    summary = true;
                    cols.add("summary");
                    break;
                case "content":
                    content = true;
                    cols.add("content");
                    break;
                default:
                    throw new IllegalStateException("Unexpected value: " + header.toLowerCase());
            }
        }

        if (id && summary && content) {
            String tableName = fileName.replaceAll("(?i)\\.csv", "").toLowerCase();
            String colHeader = cols
                .toString()
                .replace("[", "(")
                .replace("]", ")");
            sql.createArtifactTable(tableName, fullPath, colHeader);
            TIMFile(project, )
        }
    }

    private void parseBiHeaderFile(String fileName, String fullPath, String[] headers) throws ServerError {
        boolean source = false;
        boolean target = false;
        List<String> cols = new ArrayList<>();

        for (String header : headers) {
            if (header.toLowerCase().equals("source")) {
                source = true;
                cols.add("source");
            } else if (header.toLowerCase().equals("target")) {
                target = true;
                cols.add("target");
            }
        }

        if (source && target) {
            String tableName = fileName.replaceAll("(?i)\\.csv", "").toLowerCase();
            String colHeader = cols
                .toString()
                .replace("[", "(")
                .replace("]", ")");
            sql.createTraceMatrixTable(tableName, fullPath, colHeader);
        }
    }

    public void parseTraceMatrix(String traceName, JsonIterator iterator) throws ServerError {
        String filename = "";
        String source = "";
        String target = "";
        Boolean generated = false;

        try {
            for (String attr = iterator.readObject(); attr != null; attr = iterator.readObject()) {
                if (!attr.toLowerCase().matches("file|source|target|generatelinks")) {
                    throw new ServerError(String.format("LinkFile: %s Attribute: %s does not match expected: 'File', "
                        + "'Source', 'Target', or 'generateLinks'", traceName, attr));
                }

                if (attr.toLowerCase().equals("file")) {
                    filename = iterator.readString();
                }

                if (attr.toLowerCase().equals("source")) {
                    source = iterator.readString();
                }

                if (attr.toLowerCase().equals("target")) {
                    target = iterator.readString();
                }

                if (attr.toLowerCase().equals("generatelinks")) {
                    generated = iterator.readString().toLowerCase().equals("true") ? true : false;
                }
            }
        } catch (IOException e) {
            throw new ServerError("parsing trace matrix", e);
        }

        if (source.isEmpty()) {
            throw new ServerError(String.format("Missing attribute for: '%s'. Missing: 'Source' Required attributes "
                + "are 'File', 'Source', 'Target'", traceName));
        }

        if (target.isEmpty()) {
            throw new ServerError(String.format("Missing attribute for: '%s'. Missing: 'Target' Required attributes "
                + "are 'File', 'Source', 'Target'", traceName));
        }

        if (!generated && filename.isEmpty()) {
            throw new ServerError(String.format("Missing attribute for: '%s'. Missing: 'File' Required attributes are "
                + "'File', 'Source', 'Target'", traceName));
        }

        if (generated && !filename.isEmpty()) {
            throw new ServerError(String.format("Link: %s is a generated file and does not have a File attribute. "
                + "Please delete the link attribute 'File: %s' or remove 'generateLinks: True'.", traceName, filename));
        }

        if (generated) {
            String traceMatrixTableName = traceName.toLowerCase();
            sql.createUpdateTIMTraceMatrixTable(traceName, traceMatrixTableName, source, target, generated, traceName);
        } else {
            String traceMatrixTableName = filename.replaceAll("(?i)\\.csv", "").toLowerCase();
            sql.createUpdateTIMTraceMatrixTable(traceName, traceMatrixTableName, source, target, generated, filename);
        }
    }

    public void parseArtifactsInFiles(String tableName,
                                      String filePath,
                                      String colHeader) throws ServerError {
        try (Statement stmt = getConnection().createStatement()) {
            String intTableName = "intermediate_" + tableName;
            if (!tableExists("artifact_error")) {
                System.out.println("CREATING NEW ARTIFACT ERROR TABLE: artifact_error...");
                String sqlCreateErrorTable = "CREATE TABLE artifact_error (\n"
                    + "db_id INT AUTO_INCREMENT PRIMARY KEY,"
                    + "tablename VARCHAR(255),\n"
                    + "id VARCHAR(255),\n"
                    + "line INT,\n"
                    + "descr VARCHAR(255) NOT NULL"
                    + ");";
                stmt.executeUpdate(sqlCreateErrorTable);
                System.out.println("CREATED NEW ARTIFACT ERROR TABLE: artifact_error...");
            }

            createArtifactTableHelper(stmt, intTableName, tableName, filePath, colHeader);

            if (tableExists(tableName)) {
                String sqlTruncateArtifactTable = String.format("TRUNCATE TABLE %s", tableName);
                stmt.executeUpdate(sqlTruncateArtifactTable);
            } else {
                System.out.println("CREATING NEW ARTIFACT TABLE");
                String sqlCreateTable = String.format("CREATE TABLE %s (\n", tableName)
                    + "id VARCHAR(255) PRIMARY KEY,\n"
                    + "summary TEXT NOT NULL,\n"
                    + "content TEXT NOT NULL"
                    + ");";

                stmt.executeUpdate(sqlCreateTable);
                System.out.println("CREATED NEW ARTIFACT TABLE");
            }

            String sqlUpdateTable = String.format("INSERT INTO %s (id, summary, content)\n", tableName)
                + String.format("SELECT id, summary, content FROM %s\n", intTableName)
                + String.format("ON DUPLICATE KEY UPDATE id = %s.id;", tableName);

            stmt.executeUpdate(sqlUpdateTable);
            System.out.println("INSERTED DATA into ARTIFACT TABLE");


            stmt.executeUpdate(String.format("DROP TABLE %s", intTableName));
            System.out.println("DELETED INTERMEDIATE ARTIFACT TABLE");

            createTableList(tableName, false);
        } catch (SQLException e) {
            throw new ServerError("creating artifact table", e);
        }
    }

}
