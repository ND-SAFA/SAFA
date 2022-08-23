package edu.nd.crc.safa.features.jira.entities.app;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import javax.annotation.Nullable;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

/**
 * DTO representing a retrieved JIRA issue
 */
@Data
@JsonIgnoreProperties(ignoreUnknown = true)
public class JiraIssueDTO {

    /**
     * JIRA id for issue
     */
    String id;
    /**
     * The name of the issue within the project (e.g. RE-26)
     */
    String key;
    /**
     * Fields containing summary, description, and type.
     */
    JiraIssueFields fields;

    @Data
    @JsonIgnoreProperties(ignoreUnknown = true)
    public static class JiraIssueFields {
        Boolean subtask;
        /**
         * The title appearing for each issue.
         */
        String summary;

        /**
         * Descriptions of the type of issue.
         */
        @JsonProperty("issuetype")
        JiraIssueType issueType;
        /**
         * List of ingoing and outgoing links to other issues.
         */
        @JsonProperty("issuelinks")
        List<JiraIssueLink> issueLinks = new ArrayList<>();
        /**
         * The text defining this issue.
         */
        @Nullable
        JiraDescription description;
        Date updated;
        Date created;
        JiraProjectResponseDTO project;
        JiraPriority priority;
        JiraIssueStatus status;
        JiraIssueAccount creator;
        JiraIssueAccount reporter;
        JiraIssueVotes votes;

        @Data
        public static class JiraDescription {
            int version;
            String type;
            List<Content> content = new ArrayList<>();

            @Data
            public static class Content {
                String type;
                List<ContentContent> content = new ArrayList<>(); // Cannot rename because this is the format defined by JIRA
            }

            @Data
            public static class ContentContent {
                String type;
                String text;
            }
        }

        @Data
        @JsonIgnoreProperties(ignoreUnknown = true)
        public static class JiraIssueType {
            String id;
            String name;
            String description;
        }

        @Data
        @JsonIgnoreProperties(ignoreUnknown = true)
        public static class JiraPriority {
            String id;
            String name;
        }

        @Data
        @JsonIgnoreProperties(ignoreUnknown = true)
        public static class JiraIssueLink {

            JiraIssueLinkType type;
            JiraIssueDTO inwardIssue;
            JiraIssueDTO outwardIssue;

            @Data
            @JsonIgnoreProperties(ignoreUnknown = true)
            public static class JiraIssueLinkType {
                String id;
                String name;
                String inward;
                String outward;
            }
        }

        @Data
        @JsonIgnoreProperties(ignoreUnknown = true)
        public static class JiraIssueStatus {
            String id;
            String name;
        }

        @Data
        @JsonIgnoreProperties(ignoreUnknown = true)
        public static class JiraIssueAccount {
            String accountId;
            String displayName;
            String accountType;
            String timezone;
            Boolean active;
        }

        @Data
        @JsonIgnoreProperties(ignoreUnknown = true)
        public static class JiraIssueVotes {
            Integer votes;
        }

    }
}
