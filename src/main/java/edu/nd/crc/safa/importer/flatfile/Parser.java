package edu.nd.crc.safa.importer.flatfile;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;

import edu.nd.crc.safa.error.ServerError;
import edu.nd.crc.safa.importer.MySQL;

import com.jsoniter.JsonIterator;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class Parser {
    MySQL sql;

    @Autowired
    public Parser(MySQL sql) {
        this.sql = sql;
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

    private void parseTriHeaderFile(String fileName, String fullPath, String[] headers) throws ServerError {
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

}
