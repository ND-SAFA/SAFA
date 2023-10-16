package edu.nd.crc.safa.test.services.builders;

import java.util.ArrayList;
import java.util.Hashtable;
import java.util.List;
import java.util.Map;
import java.util.UUID;

import edu.nd.crc.safa.features.projects.entities.app.SafaError;

import lombok.AccessLevel;
import lombok.NoArgsConstructor;
import org.json.JSONArray;
import org.json.JSONObject;
import org.springframework.stereotype.Component;

/**
 * Provides an API for creating JSON types of application entities.
 */
@Component
public class JsonBuilder extends AbstractBuilder {
    Map<String, JSONObject> projects;
    Map<String, JSONObject> projectVersions;

    public JsonBuilder() {
        initializeData();
    }

    public void initializeData() {
        projects = new Hashtable<>();
        projectVersions = new Hashtable<>();
    }

    public JsonBuilder withProject(String id, String name, String description) {
        return withProject(id, name, description, new ArrayList<>(), new ArrayList<>());
    }

    public JsonBuilder withProject(String projectId,
                                   String name,
                                   String description,
                                   List<JSONObject> artifacts,
                                   List<JSONObject> traces) {
        JSONObject project = new JSONObject();
        project.put("projectId", projectId);
        project.put(Constants.NAME, name);
        project.put("description", description);
        project.put(Constants.ARTIFACTS, artifacts);
        project.put(Constants.TRACES, traces);
        projects.put(name, project);
        return this;
    }

    public JsonBuilder withProjectVersion(String projectName,
                                          UUID versionId,
                                          int majorVersion,
                                          int minorVersion,
                                          int revision) {
        JSONObject projectVersion = new JSONObject();
        projectVersion.put("versionId", versionId);
        projectVersion.put("majorVersion", majorVersion);
        projectVersion.put("minorVersion", minorVersion);
        projectVersion.put("revision", revision);
        this.projectVersions.put(projectName, projectVersion);
        return this;
    }

    public JSONObject getProjectJson(String projectName) {
        JSONObject project = this.projects.get(projectName);
        project.put("projectVersion", this.projectVersions.get(projectName));
        return project;
    }

    public JSONObject withArtifactAndReturn(String projectName,
                                            UUID artifactId,
                                            String name,
                                            String type,
                                            String body) {
        this.withArtifact(projectName, artifactId, name, type, body);
        JSONArray artifacts = this.projects.get(projectName).getJSONArray(Constants.ARTIFACTS);
        return (JSONObject) artifacts.get(artifacts.length() - 1);
    }

    public JsonBuilder withArtifact(String projectName,
                                    UUID artifactId,
                                    String name,
                                    String type,
                                    String body) {
        return withArtifact(projectName, artifactId, name, type, body, new Hashtable<>());
    }

    public JsonBuilder withArtifact(String projectName,
                                    UUID artifactId,
                                    String name,
                                    String type,
                                    String body,
                                    Map<String, String> customFields) {
        JSONObject project = this.projects.get(projectName);
        JSONObject artifact = new JSONObject();

        artifact.put("id", artifactId);
        artifact.put("name", name);
        artifact.put("type", type);
        artifact.put("body", body);
        artifact.put("summary", "");
        artifact.put("documentIds", new ArrayList<>());
        artifact.put("attributes", customFields);
        project.getJSONArray(Constants.ARTIFACTS).put(artifact);
        return this;
    }

    public JSONObject withTraceAndReturn(String projectName, String source, String target) {
        this.withTrace(projectName, source, target);
        JSONArray traces = this.projects.get(projectName).getJSONArray(Constants.TRACES);
        return (JSONObject) traces.get(traces.length() - 1);
    }

    public JsonBuilder withTrace(String projectName, String sourceName, String targetName) {
        JSONObject trace = new JSONObject();

        trace.put("traceLinkId", "");
        trace.put("sourceName", sourceName);
        trace.put("targetName", targetName);

        this.projects.get(projectName).getJSONArray(Constants.TRACES).put(trace);
        return this;
    }

    public JSONObject createTrace(String sourceName, String targetName) {
        JSONObject trace = new JSONObject();
        trace.put("sourceName", sourceName);
        trace.put("targetName", targetName);
        trace.put("score", 1);
        return trace;
    }

    public JSONObject createDocument(String docName,
                                     String description) {
        return createDocument(docName,
            description,
            new ArrayList<>());
    }

    public JSONObject createDocument(String docName,
                                     String description,
                                     List<UUID> artifactIds) {
        JSONObject docJson = new JSONObject();
        docJson.put(Constants.NAME, docName);
        docJson.put("description", description);
        docJson.put("artifactIds", artifactIds);

        return docJson;
    }

    public JSONObject getArtifact(String projectName, String artifactName) {
        JSONArray artifacts = this.projects.get(projectName).getJSONArray(Constants.ARTIFACTS);
        for (Object artifactObj : artifacts) {
            JSONObject artifact = (JSONObject) artifactObj;
            if (artifact.getString(Constants.NAME).equals(artifactName)) {
                return artifact;
            }
        }
        throw new SafaError("Could not find artifact %s in project %s.", artifactName, projectName);
    }

    @NoArgsConstructor(access = AccessLevel.PRIVATE)
    static class Constants {
        private static final String ARTIFACTS = "artifacts";
        private static final String TRACES = "traces";
        private static final String NAME = "name";
    }
}
