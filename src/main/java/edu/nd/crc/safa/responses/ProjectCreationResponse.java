package edu.nd.crc.safa.responses;

public class ProjectCreationResponse {
    String[] filesReceived;

    public ProjectCreationResponse(String[] filesReceived) {
        this.filesReceived = filesReceived;
    }

    public void setFilesReceived(String[] filesReceived) {
        this.filesReceived = filesReceived;
    }

    public String[] getFilesReceived() {
        return this.filesReceived;
    }
}
