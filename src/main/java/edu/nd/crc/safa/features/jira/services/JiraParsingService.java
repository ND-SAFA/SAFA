package edu.nd.crc.safa.features.jira.services;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Objects;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.common.ProjectEntities;
import edu.nd.crc.safa.features.jira.entities.app.JiraIssueDTO;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;

import org.springframework.stereotype.Service;

/**
 * Responsible for parsing JIRA issues.
 */
@Service
public class JiraParsingService {

    public ProjectEntities parseProjectEntitiesFromIssues(List<JiraIssueDTO> issues) {
        List<ArtifactAppEntity> artifacts = new ArrayList<>();
        List<TraceAppEntity> traces = new ArrayList<>();
        List<String> parsedIssues = new ArrayList<>();

        for (JiraIssueDTO issue : issues) {

            String name = parseIssue(issue, artifacts, parsedIssues);
            if (name == null) {
                continue;
            }
            issue.getFields().getIssueLinks().forEach(i -> {
                parseIssue(i.getInwardIssue(), artifacts, parsedIssues);
            });
            issue.getFields().getIssueLinks().forEach(i -> {
                parseIssue(i.getOutwardIssue(), artifacts, parsedIssues);
            });

            for (JiraIssueDTO.JiraIssueFields.JiraIssueLink link : issue.getFields().getIssueLinks()) {
                JiraIssueDTO targetArtifact = link.getOutwardIssue();
                if (targetArtifact != null) {
                    String targetName = link.getOutwardIssue().getKey();

                    TraceAppEntity trace = new TraceAppEntity()
                        .asManualTrace()
                        .betweenArtifacts(name, targetName);
                    traces.add(trace);
                }
            }
        }

        return new ProjectEntities(artifacts, traces);
    }

    private String parseIssue(JiraIssueDTO issue,
                              List<ArtifactAppEntity> artifacts,
                              List<String> processed) {
        if (issue == null) {
            return null;
        }
        String name = issue.getKey();

        if (processed.contains(name)) {
            return null;
        }

        String type = issue.getFields().getIssueType().getName();
        String summary = issue.getFields().getSummary();
        String description = getIssueDescription(issue);

        ArtifactAppEntity artifactAppEntity = new ArtifactAppEntity(
            null,
            type,
            name,
            summary,
            description,
            new HashMap<>()
        );

        artifacts.add(artifactAppEntity);
        processed.add(name);
        return name;
    }

    /**
     * Concatenates all issue contents into string delimited by newlines.
     *
     * @param issue The issue whose content is returned.
     * @return String representing delimited content.
     */
    private String getIssueDescription(JiraIssueDTO issue) {
        StringBuilder contentString = new StringBuilder();

        if (Objects.isNull(issue.getFields())) {
            return "";
        }
        if (Objects.isNull(issue.getFields().getDescription())) {
            return "";
        }

        JiraIssueDTO.JiraIssueFields.JiraDescription jiraDescription = issue.getFields().getDescription();

        for (var content : jiraDescription.getContent()) {
            for (var contentContent : content.getContent()) {
                contentString.append(contentContent.getText());
            }
        }
        return contentString.toString().strip();
    }
}
