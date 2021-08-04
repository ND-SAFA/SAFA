package edu.nd.crc.safa.output.responses;

import java.util.ArrayList;
import java.util.List;

/**
 * Represents the 1-1 JSON object mapping as the response
 * to a Client after a file manipulation operation.
 */
public class FlatFileResponse {
    List<String> uploadedFiles;
    List<String> expectedFiles;
    List<String> generatedFiles;
    List<String> expectedGeneratedFiles;

    public FlatFileResponse() {
        this.uploadedFiles = new ArrayList<>();
        this.expectedFiles = new ArrayList<>();
        this.generatedFiles = new ArrayList<>();
        this.expectedGeneratedFiles = new ArrayList<>();
    }

    public FlatFileResponse(List<String> uFiles,
                            List<String> eFiles,
                            List<String> gFiles,
                            List<String> egFiles) {
        this.uploadedFiles = uFiles;
        this.expectedFiles = eFiles;
        this.generatedFiles = gFiles;
        this.expectedGeneratedFiles = egFiles;
    }

    public List<String> getUploadedFiles() {
        return this.uploadedFiles;
    }

    public void setUploadedFiles(List<String> newFiles) {
        this.uploadedFiles = newFiles;
    }

    public List<String> getExpectedFiles() {
        return this.expectedFiles;
    }

    public void setExpectedFiles(List<String> newFiles) {
        this.expectedFiles = newFiles;
    }

    public List<String> getGeneratedFiles() {
        return this.generatedFiles;
    }

    public void setGeneratedFiles(List<String> newFiles) {
        this.generatedFiles = newFiles;
    }

    public List<String> getExpectedGeneratedFiles() {
        return this.expectedGeneratedFiles;
    }

    public void setExpectedGeneratedFiles(List<String> newFiles) {
        this.expectedGeneratedFiles = newFiles;
    }

}
