package edu.nd.crc.safa.services;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.Base64;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import edu.nd.crc.safa.constants.ProjectPaths;
import edu.nd.crc.safa.constants.ProjectVariables;
import edu.nd.crc.safa.database.entities.Project;
import edu.nd.crc.safa.database.entities.ProjectVersion;
import edu.nd.crc.safa.database.repositories.ProjectVersionRepository;
import edu.nd.crc.safa.error.ServerError;
import edu.nd.crc.safa.flatfile.FlatFileParser;
import edu.nd.crc.safa.flatfile.OSHelper;
import edu.nd.crc.safa.flatfile.TraceLinkGenerator;
import edu.nd.crc.safa.importer.MySQL;
import edu.nd.crc.safa.responses.FlatFileResponse;
import edu.nd.crc.safa.responses.RawJson;

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
    TraceMatrixService traceMatrixService;
    TraceLinkGenerator generateFlatFile;
    TimArtifactService timArtifactService;
    ProjectVersionRepository projectVersionRepository;

    @Autowired
    public FlatFileService(FlatFileParser flatFileParser,
                           TraceMatrixService traceMatrixService,
                           TraceLinkGenerator generateFlatFile,
                           TimArtifactService timArtifactService,
                           ProjectVersionRepository projectVersionRepository) {
        this.generateFlatFile = generateFlatFile;
        this.traceMatrixService = traceMatrixService;
        this.flatFileParser = flatFileParser;
        this.timArtifactService = timArtifactService;
        this.projectVersionRepository = projectVersionRepository;
    }

    /**
     * Responsible for creating a project from given flat files. This includes
     * parsing tim.json, creating artifacts, and their trace links.
     *
     * @param project the project whose artifacts and trace links should be associated with
     * @param files   the flat files defining the project
     * @throws ServerError on any parsing error of tim.json, artifacts, or trace links
     */
    public FlatFileResponse createProjectFromFiles(Project project, MultipartFile[] files) throws ServerError {
        List<String> uploadedFiles = this.uploadFlatFiles(project, files);
        ProjectVersion newProjectVersion = new ProjectVersion();
        this.projectVersionRepository.save(newProjectVersion);
        this.createProjectFromTIMFile(project, newProjectVersion);

        FlatFileResponse response = new FlatFileResponse();
        response.setUploadedFiles(uploadedFiles);
        return response;
    }

    public Map<String, Object> getUploadedFile(String pID, String file) throws ServerError {
        try {
            Map<String, Object> result = new HashMap<>();
            String data = new String(Files.readAllBytes(Paths.get("/uploadedFlatfiles/" + file)));
            if (file.contains(".json")) {
                result.put("data", RawJson.from(data));
            } else {
                result.put("data", data);
            }
            result.put("success", true);
            return result;
        } catch (IOException e) {
            throw new ServerError("retrieve uploaded file", e);
        }
    }

    private List<String> uploadFlatFiles(Project project, MultipartFile[] files) throws ServerError {
        String pathToStorage = ProjectPaths.getPathToProjectFlatFiles(project);
        OSHelper.clearOrCreateDirectory(pathToStorage);

        List<String> uploadedFiles = new ArrayList<>();
        for (MultipartFile file : files) {
            try {
                String pathToFile = ProjectPaths.getPathToProjectFlatFile(project, file.getOriginalFilename());
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
        String pathToFile = ProjectPaths.getPathToProjectFlatFile(project, ProjectVariables.TIM_FILENAME);
        this.flatFileParser.parseProject(project, projectVersion, pathToFile);
        // TODO: return generated files
    }


    public String getUploadFilesErrorLog(String projectId) throws ServerError {
        String errorStr = sql.getUploadErrorLog();
        return errorStr;
    }

    public String clearUploadedFlatFiles(String projectId) throws ServerError {
        return sql.clearUploadedFlatfiles();
    }

    public String clearGeneratedFlatFiles(String projectId) throws ServerError {
        return sql.clearGeneratedFlatfiles();
    }

    public String generateLinks(String projectId) throws ServerError {
        return generateFlatFile.generateFiles();
    }

    public String getLinkTypes(String projectId) throws ServerError {
        return generateFlatFile.getLinkTypes();
    }

    public String getLinkErrorLog(String projectId) throws ServerError {
        return sql.getLinkErrors();
    }

    public String getUploadErrorLog() throws ServerError {
        try {
            Statement stmt = getConnection().createStatement();
            System.out.println("Upload Flatfile Error Log...");

            if (!(tableExists("artifact_error") && tableExists("trace_matrix_error"))) {
                System.out.println("Upload Flatfile Error Log: Empty...");
                return "";
            }

            ArrayList<Object> artifactHeader = new ArrayList<Object>();
            artifactHeader.add("\"FILE NAME\"");
            artifactHeader.add("\"ID\"");
            artifactHeader.add("\"LINE\"");
            artifactHeader.add("\"DESC\"");

            List<ArrayList<Object>> result = new ArrayList<ArrayList<Object>>();
            result.add(artifactHeader);

            String sqlArtifactError = "SELECT tablename, id, line, descr FROM artifact_error";
            ResultSet rsArtifactError = stmt.executeQuery(sqlArtifactError);

            while (rsArtifactError.next()) {
                ArrayList<Object> row = new ArrayList<Object>();
                row.add(String.format("\"%s\"", rsArtifactError.getString(2)));
                row.add(String.format("\"%s\"", rsArtifactError.getString(3)));
                row.add(rsArtifactError.getInt(4));
                row.add(rsArtifactError.getString(5));
                result.add(row);
            }

            ArrayList<Object> traceHeader = new ArrayList<Object>();
            traceHeader.add("\"FILE NAME\"");
            traceHeader.add("\"SOURCE ID\"");
            traceHeader.add("\"TARGET ID\"");
            traceHeader.add("\"LINE\"");
            traceHeader.add("\"DESC\"");
            result.add(traceHeader);

            String sqlTraceError = "SELECT tablename, source, target, line, descr FROM trace_matrix_error";
            ResultSet rsTraceError = stmt.executeQuery(sqlTraceError);

            while (rsTraceError.next()) {
                ArrayList<Object> row = new ArrayList<Object>();
                row.add(String.format("\"%s\"", rsTraceError.getString(2)));
                row.add(String.format("\"%s\"", rsTraceError.getString(3)));
                row.add(String.format("\"%s\"", rsTraceError.getString(4)));
                row.add(rsTraceError.getInt(5));
                row.add(String.format("\"%s\"", rsTraceError.getString(6)));
                result.add(row);
            }

            byte[] content = result.toString().getBytes();
            String returnStr = Base64.getEncoder().encodeToString(content);

            return returnStr;
        } catch (SQLException e) {
            throw new ServerError("retrieving upload error log", e);
        }
    }

    public String clearUploadedFlatfiles() throws ServerError {
        try (Statement stmt = getConnection().createStatement()) {
            if (tableExists("uploaded_and_generated_tables")) {
                String sqlUploadedFiles = "SELECT tablename\n"
                    + "FROM uploaded_and_generated_tables\n"
                    + "WHERE is_generated = 0;";

                ResultSet rs = stmt.executeQuery(sqlUploadedFiles);
                ArrayList<String> tables = new ArrayList<String>();

                while (rs.next()) {
                    tables.add(rs.getString(1));
                }

                if (tableExists("artifact_error")) {
                    stmt.executeUpdate("DROP TABLE artifact_error");
                }

                if (tableExists("trace_matrix_error")) {
                    stmt.executeUpdate("DROP TABLE trace_matrix_error");
                }

                if (tables.size() == 0) {
                    stmt.executeUpdate("DROP TABLE uploaded_and_generated_tables");
                    return "No generated files";
                }

                String deleteTables = tables.toString().replace("[", "").replace("]", "");
                String sqlDropTables = String.format("DROP TABLES %s;", deleteTables);
                stmt.executeUpdate(sqlDropTables);

                String sqlDeleteTables = "DELETE FROM uploaded_and_generated_tables WHERE is_generated = 0;";
                stmt.executeUpdate(sqlDeleteTables);

                return "Uploaded files have successfully been cleared";
            } else {
                return "No uploaded files";
            }
        } catch (SQLException e) {
            throw new ServerError("clear uploaded flat files", e);
        }
    }

    public String clearGeneratedFlatfiles() throws ServerError {
        try (Statement stmt = getConnection().createStatement()) {
            if (tableExists("uploaded_and_generated_tables")) {
                String sqlUploadedFiles = "SELECT tablename\n"
                    + "FROM uploaded_and_generated_tables\n"
                    + "WHERE is_generated = 1;";

                ResultSet rs = stmt.executeQuery(sqlUploadedFiles);
                ArrayList<String> tables = new ArrayList<String>();

                while (rs.next()) {
                    tables.add(rs.getString(1));
                }

                if (tables.size() == 0) {
                    stmt.executeUpdate("DROP TABLE uploaded_and_generated_tables");
                    return "No generated files";
                }

                String deleteTables = tables
                    .toString()
                    .replace("[", "")
                    .replace("]", "");
                String sqlDropTables = String.format("DROP TABLES %s;", deleteTables);
                stmt.executeUpdate(sqlDropTables);

                String sqlDeleteTables = "DELETE FROM uploaded_and_generated_tables WHERE is_generated = 1;";
                stmt.executeUpdate(sqlDeleteTables);

                return "Generated files have successfully been cleared";
            } else {
                return "No generated files";
            }
        } catch (SQLException e) {
            throw new ServerError("clearing generated flat files", e);
        }
    }

    public MySQL.FileInfo getFileInfo() throws ServerError {
        MySQL.FileInfo fileInfo = new MySQL.FileInfo();

        List<List<String>> artifact_rows = getTimArtifactData();

        for (List<String> artifact_row : artifact_rows) {
            String tablename = artifact_row.get(1);
            String filename = String.format("\"%s\"", artifact_row.get(2));

            fileInfo.expectedFiles.add(filename);

            if (tableExists(tablename)) {
                fileInfo.uploadedFiles.add(filename);
            }
        }

        List<List<String>> trace_rows = getTimTraceData();

        for (List<String> trace_row : trace_rows) {
            boolean generated = trace_row.get(3).equals("1");
            String tableName = trace_row.get(4);
            String filename = String.format("\"%s\"", trace_row.get(5));

            if (generated) {
                fileInfo.expectedGeneratedFiles.add(filename);

                if (tableExists(tableName)) {
                    fileInfo.generatedFiles.add(filename);
                }
            } else {
                fileInfo.expectedFiles.add(filename);

                if (tableExists(tableName)) {
                    fileInfo.uploadedFiles.add(filename);
                }
            }
        }

        return fileInfo;
    }
}
