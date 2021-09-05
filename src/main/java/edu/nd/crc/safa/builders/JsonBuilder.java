package edu.nd.crc.safa.builders;

import java.util.ArrayList;
import java.util.Hashtable;
import java.util.List;

import org.json.JSONObject;
import org.springframework.stereotype.Component;

@Component
public class JsonBuilder extends BaseBuilder {

    Hashtable<String, JSONObject> projects;

    public JsonBuilder() {
        createEmptyData();
    }

    public void createEmptyData() {
        projects = new Hashtable<>();
    }

    public JsonBuilder withProject(String id, String name) {
        return withProject(id, name, new ArrayList<>(), new ArrayList<>());
    }

    public JsonBuilder withProject(String id,
                                   String name,
                                   List<JSONObject> artifacts,
                                   List<JSONObject> traces) {
        JSONObject project = new JSONObject();
        project.put("projectId", id);
        project.put("name", name);
        project.put("artifacts", artifacts);
        project.put("traces", traces);
        projects.put(name, project);
        return this;
    }

    public JsonBuilder withArtifact(String projectName,
                                    String name,
                                    String type,
                                    String body) {
        JSONObject project = this.projects.get(projectName);
        JSONObject artifact = new JSONObject();
        artifact.put("name", name);
        artifact.put("type", type);
        artifact.put("body", body);
        project.getJSONArray("artifacts").put(artifact);
        return this;
    }

    public JsonBuilder withTrace(String projectName, String source, String target) {
        JSONObject trace = new JSONObject();
        trace.put("source", source);
        trace.put("target", target);
        this.projects.get(projectName).getJSONArray("traces").put(trace);
        return this;
    }

    public JSONObject getProjectAndReturn(String projectName) {
        return this.projects.get(projectName);
    }
}
