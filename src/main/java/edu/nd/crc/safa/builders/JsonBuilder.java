package edu.nd.crc.safa.builders;

import java.util.ArrayList;
import java.util.Hashtable;
import java.util.List;

import edu.nd.crc.safa.server.entities.db.DocumentType;

import org.json.JSONArray;
import org.json.JSONObject;
import org.springframework.stereotype.Component;

/**
 * Provides an API for creating JSON types of application entities.
 */
@Component
public class JsonBuilder extends BaseBuilder {

    Hashtable<String, JSONObject> projects;
    Hashtable<String, JSONObject> projectVersions;

    public JsonBuilder() {
        createEmptyData();
    }

    public void createEmptyData() {
        projects = new Hashtable<>();
        projectVersions = new Hashtable<>();
    }

    public JSONObject withProjectAndReturn(String id, String name, String description) {
        withProject(id, name, description, new ArrayList<>(), new ArrayList<>());
        return this.projects.get(id);
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
        project.put("name", name);
        project.put("description", description);
        project.put("artifacts", artifacts);
        project.put("traces", traces);
        projects.put(name, project);
        return this;
    }

    public JsonBuilder withProjectVersion(String projectName,
                                          String versionId,
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

    public JSONObject getPayload(String projectName) {
        JSONObject project = this.projects.get(projectName);
        project.put("projectVersion", this.projectVersions.get(projectName));
        return project;
    }

    public JSONObject withArtifactAndReturn(String projectName,
                                            String artifactId,
                                            String name,
                                            String type,
                                            String body) {
        this.withArtifact(projectName, artifactId, name, type, body);
        JSONArray artifacts = this.projects.get(projectName).getJSONArray("artifacts");
        return (JSONObject) artifacts.get(artifacts.length() - 1);
    }

    public JsonBuilder withArtifact(String projectName,
                                    String artifactId,
                                    String name,
                                    String type,
                                    String body) {
        JSONObject project = this.projects.get(projectName);
        JSONObject artifact = new JSONObject();
        if (artifact != null) { // TODO: don't let this in production
            artifact.put("id", artifactId);
        }

        artifact.put("name", name);
        artifact.put("type", type);
        artifact.put("body", body);
        artifact.put("summary", "");
        project.getJSONArray("artifacts").put(artifact);
        return this;
    }

    public JSONObject withTraceAndReturn(String projectName, String source, String target) {
        this.withTrace(projectName, source, target);
        JSONArray traces = this.projects.get(projectName).getJSONArray("traces");
        return (JSONObject) traces.get(traces.length() - 1);
    }

    public JsonBuilder withTrace(String projectName, String sourceName, String targetName) {
        JSONObject trace = new JSONObject();

        trace.put("traceLinkId", "");
        trace.put("sourceName", sourceName);
        trace.put("targetName", targetName);

        this.projects.get(projectName).getJSONArray("traces").put(trace);
        return this;
    }

    public JSONObject createTrace(String sourceName, String targetName) {
        JSONObject trace = new JSONObject();
        trace.put("sourceName", sourceName);
        trace.put("targetName", targetName);
        return trace;
    }

    public JSONObject createDocument(String docName,
                                     String description,
                                     DocumentType documentType) {
        JSONObject docJson = new JSONObject();
        docJson.put("name", docName);
        docJson.put("description", description);
        docJson.put("type", documentType);
        return docJson;
    }
}
