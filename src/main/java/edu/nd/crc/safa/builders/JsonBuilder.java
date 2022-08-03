package edu.nd.crc.safa.builders;

import java.util.ArrayList;
import java.util.Hashtable;
import java.util.List;
import java.util.Map;

import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.app.documents.DocumentColumnDataType;
import edu.nd.crc.safa.server.entities.app.project.FTAType;
import edu.nd.crc.safa.server.entities.app.project.SafetyCaseType;
import edu.nd.crc.safa.server.entities.db.DocumentType;

import lombok.AccessLevel;
import lombok.NoArgsConstructor;
import org.json.JSONArray;
import org.json.JSONObject;
import org.springframework.stereotype.Component;

/**
 * Provides an API for creating JSON types of application entities.
 */
@Component
public class JsonBuilder extends BaseBuilder {
    Map<String, JSONObject> projects;
    Map<String, JSONObject> projectVersions;

    public JsonBuilder() {
        createEmptyData();
    }

    public void createEmptyData() {
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

    public JSONObject getProjectJson(String projectName) {
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
        JSONArray artifacts = this.projects.get(projectName).getJSONArray(Constants.ARTIFACTS);
        return (JSONObject) artifacts.get(artifacts.length() - 1);
    }

    public JsonBuilder withArtifact(String projectName,
                                    String artifactId,
                                    String name,
                                    String type,
                                    String body) {
        return withArtifact(projectName, artifactId, name, type, body, new Hashtable<>());
    }

    public JsonBuilder withArtifact(String projectName,
                                    String artifactId,
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
        artifact.put(Constants.DOCUMENT_TYPE, DocumentType.ARTIFACT_TREE.toString());
        artifact.put("customFields", customFields);
        project.getJSONArray(Constants.ARTIFACTS).put(artifact);
        return this;
    }

    public JsonBuilder withSafetyCaseArtifact(String projectName,
                                              String artifactName,
                                              String artifactType,
                                              String body,
                                              SafetyCaseType safetyCaseType
    ) {

        this.withArtifact(projectName, "", artifactName, artifactType, body);
        JSONObject artifact = this.getArtifact(projectName, artifactName);
        artifact.put("safetyCaseType", safetyCaseType.toString());
        artifact.put(Constants.DOCUMENT_TYPE, DocumentType.SAFETY_CASE.toString());
        return this;
    }

    public JsonBuilder withFTAArtifact(String projectName,
                                       String artifactName,
                                       String artifactType,
                                       String body,
                                       FTAType ftaType
    ) {

        this.withArtifact(projectName, "", artifactName, artifactType, body);
        JSONObject artifact = this.getArtifact(projectName, artifactName);
        artifact.put("logicType", ftaType.toString());
        artifact.put(Constants.DOCUMENT_TYPE, DocumentType.FTA.toString());
        return this;
    }

    public JsonBuilder withFMEAArtifact(String projectName,
                                        String artifactName,
                                        String artifactType,
                                        String body,
                                        JSONObject customFields
    ) {

        this.withArtifact(projectName, "", artifactName, artifactType, body);
        JSONObject artifact = this.getArtifact(projectName, artifactName);
        artifact.put("customFields", customFields);
        artifact.put(Constants.DOCUMENT_TYPE, DocumentType.FMEA.toString());
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
                                     String description,
                                     DocumentType documentType) {
        return createDocument(docName,
            description,
            documentType,
            new ArrayList<>());
    }

    public JSONObject createDocument(String docName,
                                     String description,
                                     DocumentType documentType,
                                     List<String> artifactIds) {
        JSONObject docJson = new JSONObject();
        docJson.put(Constants.NAME, docName);
        docJson.put("description", description);
        docJson.put("type", documentType.toString());
        docJson.put("artifactIds", artifactIds);

        return docJson;
    }

    public JSONObject createFMEADocument(String name, String description) {
        JSONObject fmeaJson = this.createDocument(name, description, DocumentType.FMEA);
        fmeaJson.put("columns", new ArrayList<>());
        return fmeaJson;
    }

    public JSONObject createDocumentColumn(String id, String name, DocumentColumnDataType dataType) {
        JSONObject columnJson = new JSONObject();
        columnJson.put("id", id);
        columnJson.put("name", name);
        columnJson.put("dataType", dataType);
        return columnJson;
    }

    public JSONObject getArtifact(String projectName, String artifactName) {
        JSONArray artifacts = this.projects.get(projectName).getJSONArray(Constants.ARTIFACTS);
        for (Object artifactObj : artifacts) {
            JSONObject artifact = (JSONObject) artifactObj;
            if (artifact.getString(Constants.NAME).equals(artifactName)) {
                return artifact;
            }
        }
        String error = String.format("Could not find artifact %s in project %s.", artifactName, projectName);
        throw new SafaError("Could not find artifact with name:" + error);
    }

    @NoArgsConstructor(access = AccessLevel.PRIVATE)
    static class Constants {
        private static final String ARTIFACTS = "artifacts";
        private static final String TRACES = "traces";
        private static final String NAME = "name";
        private static final String DOCUMENT_TYPE = "documentType";
    }
}
