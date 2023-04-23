package edu.nd.crc.safa.features.github.entities.api.graphql;

import java.util.Date;

import lombok.Data;

@Data
public class Repository {
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
