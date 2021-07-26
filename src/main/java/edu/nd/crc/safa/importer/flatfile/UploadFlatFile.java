package edu.nd.crc.safa.importer.flatfile;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Base64;
import java.util.List;

import edu.nd.crc.safa.error.ServerError;
import edu.nd.crc.safa.importer.MySQL;

import com.jsoniter.JsonIterator;
import com.jsoniter.spi.JsonException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;


@Component
public class UploadFlatFile {

    String pathToFlatFiles = System.getProperty("user.dir") + "/build/uploadedFlatFiles";

    private MySQL sql;

    @Autowired
    public UploadFlatFile(MySQL sql) {
        this.sql = sql;
    }

    public static class TimBackend {
        public List<List<String>> artifacts = new ArrayList<List<String>>();
        public List<List<String>> traces = new ArrayList<List<String>>();
    }

    public UploadFlatFileResponse uploadFiles(String projId, String jsonfiles) throws ServerError {
        createDirectory(pathToFlatFiles);

        JsonIterator iterator = JsonIterator.parse(jsonfiles);
        try {
            for (String filename = iterator.readObject(); filename != null; filename = iterator.readObject()) {
                String encodedData = iterator.readString();
                byte[] bytes = Base64.getDecoder().decode(encodedData);
                String fullPath = pathToFlatFiles + "/" + filename;
                Files.write(Paths.get(fullPath), bytes);

                if (filename.equals("tim.json")) {
                    sql.clearTimTables();
                    parseTimFile(fullPath);
                } else {
                    parseRegularFile(filename, fullPath);
                }
            }
        } catch (IOException e) {
            throw new ServerError("uploading files", e);
        } catch (JsonException e) {
            throw new ServerError("parsing json file", e);
        }

        sql.traceArtifactCheck();
        MySQL.FileInfo fileInfo = sql.getFileInfo();

        return new UploadFlatFileResponse(fileInfo.uploadedFiles,
            fileInfo.expectedFiles,
            fileInfo.generatedFiles,
            fileInfo.expectedGeneratedFiles
        );
    }

    public void parseTimFile(String fullPath) throws ServerError {
        try {
            String data = new String(Files.readAllBytes(Paths.get(fullPath)));
            JsonIterator iterator = JsonIterator.parse(data);

            for (String field = iterator.readObject(); field != null; field = iterator.readObject()) {
                if (field.toLowerCase().equals("datafiles")) {
                    for (String artifactName = iterator.readObject();
                         artifactName != null;
                         artifactName = iterator.readObject()) {
                        String fileName = "";

                        for (String field2 = iterator.readObject(); field2 != null; field2 = iterator.readObject()) {
                            if (!field2.toLowerCase().equals("file")) {
                                throw new ServerError(String.format("Artifact: %s. Expected File attribute. The File "
                                    + "attribute should appear as 'File': 'FileName'", artifactName));
                            }

                            fileName = iterator.readString();
                        }

                        if (fileName.isEmpty()) {
                            throw new ServerError(String.format("Did not provide a File for Artifact: %s. The File "
                                + "attribute should appear as 'File': 'FileName.csv'", artifactName));
                        }

                        String artifactTableName = fileName.replaceAll("(?i)\\.csv", "").toLowerCase();
                        sql.createTimArtifactsTable(artifactName, artifactTableName, fileName);
                    }
                } else {
                    parseTraceMatrix(field, iterator);
                }
            }
        } catch (IOException e) {
            throw new ServerError("parsing TIM file", e);
        }
    }

    public void parseRegularFile(String fileName, String fullPath) throws ServerError {
        try (BufferedReader uploadedFileReader = new BufferedReader(new FileReader(fullPath))) {
            String[] headers = uploadedFileReader.readLine().split(",");

            if (headers.length == 2) {
                Boolean source = false;
                Boolean target = false;
                List<String> cols = new ArrayList<String>();

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
            } else if (headers.length == 3) {
                Boolean id = false;
                Boolean summary = false;
                Boolean content = false;
                List<String> cols = new ArrayList<String>();

                for (String header : headers) {
                    if (header.toLowerCase().equals("id")) {
                        id = true;
                        cols.add("id");
                    } else if (header.toLowerCase().equals("summary")) {
                        summary = true;
                        cols.add("summary");
                    } else if (header.toLowerCase().equals("content")) {
                        content = true;
                        cols.add("content");
                    }
                }

                if (id && summary && content) {
                    String tableName = fileName.replaceAll("(?i)\\.csv", "").toLowerCase();
                    String colHeader = cols
                        .toString()
                        .replace("[", "(")
                        .replace("]", ")");
                    sql.createArtifactTable(tableName, fullPath, colHeader);
                }
            } else {
                throw new ServerError("unrecognized file type: " + fileName);
            }
        } catch (IOException e) {
            throw new ServerError("parse regular file", e);
        }
    }

    public void parseTraceMatrix(String tracename, JsonIterator iterator) throws ServerError {
        String filename = "";
        String source = "";
        String target = "";
        Boolean generated = false;

        try {
            for (String attr = iterator.readObject(); attr != null; attr = iterator.readObject()) {
                if (!attr.toLowerCase().matches("file|source|target|generatelinks")) {
                    throw new ServerError(String.format("LinkFile: %s Attribute: %s does not match expected: 'File', "
                        + "'Source', 'Target', or 'generateLinks'", tracename, attr));
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
                + "are 'File', 'Source', 'Target'", tracename));
        }

        if (target.isEmpty()) {
            throw new ServerError(String.format("Missing attribute for: '%s'. Missing: 'Target' Required attributes "
                + "are 'File', 'Source', 'Target'", tracename));
        }

        if (!generated && filename.isEmpty()) {
            throw new ServerError(String.format("Missing attribute for: '%s'. Missing: 'File' Required attributes are "
                + "'File', 'Source', 'Target'", tracename));
        }

        if (generated && !filename.isEmpty()) {
            throw new ServerError(String.format("Link: %s is a generated file and does not have a File attribute. "
                + "Please delete the link attribute 'File: %s' or remove 'generateLinks: True'.", tracename, filename));
        }

        if (generated) {
            String traceMatrixTableName = tracename.toLowerCase();
            sql.createUpdateTIMTraceMatrixTable(tracename, traceMatrixTableName, source, target, generated, tracename);
        } else {
            String traceMatrixTableName = filename.replaceAll("(?i)\\.csv", "").toLowerCase();
            sql.createUpdateTIMTraceMatrixTable(tracename, traceMatrixTableName, source, target, generated, filename);
        }
    }

    public static File createDirectory(String pathToDir) throws ServerError {
        File myDir = new File(pathToDir);

        try {
            System.out.println("PATH: " + myDir.getCanonicalPath());
        } catch (IOException e) {
            e.printStackTrace();
        }


        if (!myDir.exists()) {
            if (!myDir.mkdirs()) {
                throw new ServerError(String.format("Error creating folder: Path: %s", pathToDir));
            }
        }

        if (!myDir.isDirectory()) {
            if (!myDir.delete()) {
                throw new ServerError(String.format("Error deleting file: Path: %s", pathToDir));
            }
            if (!myDir.mkdirs()) {
                throw new ServerError(String.format("Error creating folder: Path: %s", pathToDir));
            }
        }

        return myDir;
    }

    public static void deleteDirectory(String dir) throws ServerError {
        File myDir = new File(dir);

        if (myDir.isDirectory()) {
            deleteDirectoryHelper(myDir);
        }
    }

    public static boolean deleteDirectoryHelper(File dir) throws ServerError {
        File[] files = dir.listFiles();
        if (files != null) {
            for (File file : files) {
                deleteDirectoryHelper(file);
            }
        }
        return dir.delete();
    }

    public TimBackend getTimFile() throws ServerError {
        TimBackend timBackend = new TimBackend();

        List<List<String>> artifact_rows = sql.getTimArtifactData();
        for (List<String> artifact_row : artifact_rows) {
            List<String> artifacts = new ArrayList<String>();

            String artifact = String.format("\"%s\"", artifact_row.get(0));
            String filename = String.format("\"%s\"", artifact_row.get(2));

            artifacts.add(artifact);
            artifacts.add(filename);
            timBackend.artifacts.add(artifacts);
        }

        List<List<String>> trace_rows = sql.getTimTraceData();
        for (List<String> trace_row : trace_rows) {
            List<String> traces = new ArrayList<String>();

            String trace = String.format("\"%s\"", trace_row.get(0));
            String source = String.format("\"%s\"", trace_row.get(1));
            String target = String.format("\"%s\"", trace_row.get(2));
            String filename = String.format("\"%s\"", trace_row.get(5));

            if (trace_rows.get(3).equals('1')) {
                filename = String.format("\"generateLinks\"");
            }

            traces.add(trace);
            traces.add(source);
            traces.add(target);
            traces.add(filename);

            timBackend.traces.add(traces);
        }

        return timBackend;
    }
}
