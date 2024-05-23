package edu.nd.crc.safa.test.services.builders;

import edu.nd.crc.safa.features.attributes.entities.CustomAttributeType;
import edu.nd.crc.safa.features.attributes.entities.db.definitions.CustomAttribute;
import edu.nd.crc.safa.features.projects.entities.db.Project;

import lombok.Getter;

@Getter
public class CustomAttributeBuilder {
    private final CustomAttribute customAttribute;

    public CustomAttributeBuilder() {
        this.customAttribute = new CustomAttribute();
    }

    public CustomAttributeBuilder withType(CustomAttributeType type) {
        this.customAttribute.setType(type);
        return this;
    }

    public CustomAttributeBuilder withLabel(String label) {
        this.customAttribute.setLabel(label);
        return this;
    }

    public CustomAttributeBuilder withKeyName(String key) {
        this.customAttribute.setKeyname(key);
        return this;
    }

    public CustomAttributeBuilder withProject(Project project) {
        this.customAttribute.setProjectId(project.getId());
        return this;
    }
}
