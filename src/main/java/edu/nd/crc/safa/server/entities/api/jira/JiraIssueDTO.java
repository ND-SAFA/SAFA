package edu.nd.crc.safa.server.entities.api.jira;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

/**
 * DTO representing a retrieved JIRA issue
 *
 */
@Data
public class JiraIssueDTO {

    String id;
    String key;
    JiraIssueFields fields;

    @Data
    public static class JiraIssueFields {
        Boolean subtask;
        String summary;
        Date created;
        JiraProjectResponseDTO project;
        JiraIssueType issueType;
        JiraPriority priority;
        @JsonProperty("issuelinks")
        List<JiraIssueLink> issueLinks = new ArrayList<>();
        Date updated;
        JiraIssueStatus status;
        JiraIssueAccount creator;
        JiraIssueAccount reporter;
        JiraIssueVotes votes;

        @Data
        public static class JiraIssueType {
            String id;
            String name;
            String description;
        }

        @Data
        public static class JiraPriority {
            String id;
            String name;
        }

        @Data
        public static class JiraIssueLink {

            JiraIssueLinkType type;
            JiraIssueDTO inwardIssue;
            JiraIssueDTO outwardIssue;

            @Data
            public static class JiraIssueLinkType {
                String id;
                String name;
                String inward;
                String outward;
            }
        }

        @Data
        public static class JiraIssueStatus {
            String id;
            String name;
        }

        @Data
        public static class JiraIssueAccount {
            String accountId;
            String displayName;
            String accountType;
            String timezone;
            Boolean active;
        }

        @Data
        public static class JiraIssueVotes {
            Integer votes;
        }

    }
}
