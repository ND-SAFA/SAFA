package edu.nd.crc.safa.responses;

import org.springframework.web.multipart.MultipartFile;

public class ProjectCreationResponse {
    String[] filesReceived;


    public ProjectCreationResponse() {
    }

    public ProjectCreationResponse(String[] filesReceived) {
        setFilesReceived(filesReceived);
    }

    public void setFilesReceived(String[] filesReceived) {
        this.filesReceived = filesReceived;
    }

    public void setFilesReceived(MultipartFile[] requestFiles) {
        this.filesReceived = new String[requestFiles.length];

        for (int i = 0; i < requestFiles.length; i++) {
            this.filesReceived[i] = requestFiles[i].getOriginalFilename();
        }
    }

    public String[] getFilesReceived() {
        return this.filesReceived;
    }
}
