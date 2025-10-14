package edu.nd.crc.safa.test.services.builders;

import java.util.HashMap;

import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.users.entities.IUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import lombok.AccessLevel;
import lombok.Data;
import lombok.Getter;
import lombok.Setter;

@Data
public class BuilderState {
    @Getter(AccessLevel.PRIVATE)
    @Setter(AccessLevel.PRIVATE)
    HashMap<String, Object> store = new HashMap<>();
    private ServiceProvider serviceProvider;
    private int port;

    public BuilderState save(String name, Object value) {
        if (value instanceof AndBuilder<?, ?>) {
            throw new SafaError("Cannot save a builder. Did you mean to save the inside result?");
        }
        if (value == null) {
            throw new SafaError(String.format("%s received null value.", name));
        }
        if (this.store.containsKey(name)) {
            throw new SafaError(String.format("%s already has a value, overriding is not allowed.", name));
        }
        this.store.put(name, value);
        return this;
    }

    public BuilderState update(String name, Object value) {
        if (!this.store.containsKey(name)) {
            throw new SafaError(String.format("%s does not contain a value."), name);
        }
        this.store.put(name, value);
        return this;
    }

    public String getString(String name) {
        return (String) get(name);
    }

    public Project getProject(String name) {
        return (Project) get(name);
    }

    public ProjectVersion getProjectVersion(String name) {
        return (ProjectVersion) get(name);
    }

    public IUser getIUser(String name) {
        return (IUser) get(name);
    }

    public EntityChangeMessage getMessage(String name) {
        return (EntityChangeMessage) get(name);
    }

    public Object get(String name) {
        Object result = this.store.get(name);
        if (result == null) {
            throw new SafaError(String.format("%s does not have a value.", name));
        }
        return result;
    }
}
