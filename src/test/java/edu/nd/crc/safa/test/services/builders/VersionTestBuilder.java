package edu.nd.crc.safa.test.services.builders;

import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

public class VersionTestBuilder {
    private final ServiceProvider serviceProvider;
    private int revisionNumber = 1;

    public VersionTestBuilder(ServiceProvider serviceProvider) {
        this.serviceProvider = serviceProvider;
    }

    public ProjectVersion newVersion(Project project) {
        int MINOR_VERSION = 1;
        int MAJOR_VERSION = 1;
        return this.serviceProvider.getVersionService().createNewVersion(project,
            MAJOR_VERSION,
            MINOR_VERSION,
            this.revisionNumber++);
    }
}
