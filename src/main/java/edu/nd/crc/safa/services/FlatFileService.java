package edu.nd.crc.safa.services;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.HashMap;
import java.util.Map;

import edu.nd.crc.safa.error.ServerError;
import edu.nd.crc.safa.importer.MySQL;
import edu.nd.crc.safa.importer.flatfile.FlatFileResponse;
import edu.nd.crc.safa.importer.flatfile.Generator;
import edu.nd.crc.safa.importer.flatfile.UploadFlatFile;

import com.fasterxml.jackson.annotation.JsonRawValue;
import com.fasterxml.jackson.annotation.JsonValue;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class FlatFileService {

    MySQL sql;
    UploadFlatFile uploadFlatfile;
    Generator generateFlatfile;

    @Autowired
    public FlatFileService(MySQL sql, UploadFlatFile uploadFlatfile, Generator generateFlatfile) {
        this.sql = sql;
        this.uploadFlatfile = uploadFlatfile;
        this.generateFlatfile = generateFlatfile;
    }

    public FlatFileResponse uploadFile(String projectId, String encodedStr) throws ServerError {
        return uploadFlatfile.uploadFiles(projectId, encodedStr);
    }

    public static class RawJson {
        private String payload;

        public RawJson(String payload) {
            this.payload = payload;
        }

        public static RawJson from(String payload) {
            return new RawJson(payload);
        }

        @JsonValue
        @JsonRawValue
        public String getPayload() {
            return this.payload;
        }
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
        return generateFlatfile.generateFiles();
    }

    public String getLinkTypes(String projectId) throws ServerError {
        return generateFlatfile.getLinkTypes();
    }

    public String getLinkErrorLog(String projectId) throws ServerError {
        return sql.getLinkErrors();
    }
}
