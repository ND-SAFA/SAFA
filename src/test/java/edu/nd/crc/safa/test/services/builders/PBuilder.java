package edu.nd.crc.safa.test.services.builders;

import edu.nd.crc.safa.features.projects.entities.db.Project;

import lombok.Getter;

public class PBuilder {
    private final String defaultName = "project-name";
    private final String defaultDescription = "project-description";
    @Getter
    private Project project;


    public PBuilder() {
        this.project = new Project();
        this.project.setLastEdited();
    }

    public PBuilder defaultValues() {
        return this.withName(defaultName)
            .withDescription(defaultDescription);
    }

    public PBuilder withName(String name) {
        this.project.setName(name);
        return this;
    }

    public PBuilder withDescription(String description) {
        this.project.setDescription(description);
        return this;
    }

    public PBuilder withDummyDescription() {
        String description = String.format("%s-%s", this.project.getName(), "description");
        this.project.setDescription(description);
        return this;
    }
}
