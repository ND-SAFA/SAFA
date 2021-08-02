package edu.nd.crc.safa.importer.flatfile.parser;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import edu.nd.crc.safa.database.entities.ArtifactType;
import edu.nd.crc.safa.database.entities.Project;
import edu.nd.crc.safa.error.ServerError;

import org.json.JSONObject;
import org.springframework.stereotype.Component;

@Component
public class TraceFileParser {

    public void parseTraceFile(Project project,
                               ArtifactType artifactType,
                               String fileName,
                               String fullPath,
                               String[] headers) throws ServerError {
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

    public void parseTraceMatrix(Project project, JSONObject obj) throws ServerError {
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
}
