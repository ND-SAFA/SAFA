package edu.nd.crc.safa.features.github.entities.app;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Getter;

@AllArgsConstructor
@Getter
public enum GithubRepositoryFileType {
    @JsonProperty("blob")
    FILE,

    @JsonProperty("tree")
    FOLDER,

    @JsonProperty("commit")
    SUBMODULE
}
