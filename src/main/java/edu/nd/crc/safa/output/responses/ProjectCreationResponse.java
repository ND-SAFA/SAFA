package edu.nd.crc.safa.output.responses;

import edu.nd.crc.safa.entities.Project;

public class ProjectCreationResponse {

    Project project;
    FlatFileResponse flatFileResponse;

    public ProjectCreationResponse(Project project, FlatFileResponse flatFileResponse) {
        this.project = project;
        this.flatFileResponse = flatFileResponse;
    }

    public Project getProject() {
        return this.project;
    }

    public void setProject(Project project) {
        this.project = project;
    }

    public void setFlatFileResponse(FlatFileResponse flatFileResponse) {
        this.flatFileResponse = flatFileResponse;
    }

    public FlatFileResponse getFlatFileResponse() {
        return this.flatFileResponse;
    }
}
