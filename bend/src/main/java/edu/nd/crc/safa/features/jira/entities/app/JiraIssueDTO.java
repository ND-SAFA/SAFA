package edu.nd.crc.safa.features.jira.entities.app;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.annotation.Nullable;
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
    private String id;
    /**
     * The name of the issue within the project (e.g. RE-26)
     */
    private String key;
    /**
     * Fields containing summary, description, and type.
     */
    private JiraIssueFields fields;

    @Data
    @JsonIgnoreProperties(ignoreUnknown = true)
    public static class JiraIssueFields {
        private Boolean subtask;
        /**
         * The title appearing for each issue.
         */
        private String summary;

        /**
         * Descriptions of the type of issue.
         */
        @JsonProperty("issuetype")
        private JiraIssueType issueType;
        /**
         * List of ingoing and outgoing links to other issues.
         */
        @JsonProperty("issuelinks")
        private List<JiraIssueLink> issueLinks = new ArrayList<>();
        /**
         * The text defining this issue.
         */
        @Nullable
        private JiraDescription description;
        private Date updated;
        private Date created;
        private JiraProjectResponseDTO project;
        private JiraPriority priority;
        private JiraIssueStatus status;
        private JiraIssueAccount creator;
        private JiraIssueAccount reporter;
        private JiraIssueVotes votes;

        @Data
        public static class JiraDescription {
            private int version;
            private String type;
            private List<Content> content = new ArrayList<>();

            @Data
            public static class Content {
                private String type;
                // Cannot rename because this is the format defined by JIRA
                private List<ContentContent> content = new ArrayList<>();
            }

            @Data
            public static class ContentContent {
                private String type;
                private String text;
            }
        }

        @Data
        @JsonIgnoreProperties(ignoreUnknown = true)
        public static class JiraIssueType {
            private String id;
            private String name;
            private String description;
        }

        @Data
        @JsonIgnoreProperties(ignoreUnknown = true)
        public static class JiraPriority {
            private String id;
            private String name;
        }

        @Data
        @JsonIgnoreProperties(ignoreUnknown = true)
        public static class JiraIssueLink {

            private JiraIssueLinkType type;
            private JiraIssueDTO inwardIssue;
            private JiraIssueDTO outwardIssue;

            @Data
            @JsonIgnoreProperties(ignoreUnknown = true)
            public static class JiraIssueLinkType {
                private String id;
                private String name;
                private String inward;
                private String outward;
            }
        }

        @Data
        @JsonIgnoreProperties(ignoreUnknown = true)
        public static class JiraIssueStatus {
            private String id;
            private String name;
        }

        @Data
        @JsonIgnoreProperties(ignoreUnknown = true)
        public static class JiraIssueAccount {
            private String accountId;
            private String displayName;
            private String accountType;
            private String timezone;
            private Boolean active;
        }

        @Data
        @JsonIgnoreProperties(ignoreUnknown = true)
        public static class JiraIssueVotes {
            private Integer votes;
        }

    }
}
