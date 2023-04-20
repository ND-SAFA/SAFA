package edu.nd.crc.safa.features.github.entities.api;

import java.util.Date;

import edu.nd.crc.safa.features.github.entities.api.graphql.Edges;
import edu.nd.crc.safa.features.github.entities.api.graphql.GithubResponse;
import edu.nd.crc.safa.features.github.entities.api.graphql.RepositoryVisibility;

import lombok.Data;
import lombok.Getter;
import lombok.ToString;

/**
 * Response for {@code github/GetRepositories.graphql}.
 */
@Getter
@ToString
public class GithubGraphQlRepositoriesResponse extends GithubResponse<GithubGraphQlRepositoriesResponse.Payload> {

    @Data
    public static class Payload {

        private Viewer viewer;

        @Data
        public static class Viewer {
            private Edges<Repository> repositories;
        }

        @Data
        public static class Repository {
            private String id;
            private String name;
            private Owner owner;
            private String nameWithOwner;
            private boolean isPrivate;
            private String url;
            private String description;
            private RepositoryVisibility visibility;
            private Date createdAt;
            private Language primaryLanguage;
            private Branch defaultBranchRef;
            private Edges<Branch> refs;
        }

        @Data
        public static class Owner {
            private String login;
        }

        @Data
        public static class Language {
            private String name;
        }

        @Data
        public static class Branch {
            private String name;
        }
    }
}
