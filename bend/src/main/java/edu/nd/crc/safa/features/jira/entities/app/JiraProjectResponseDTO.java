package edu.nd.crc.safa.features.jira.entities.app;

import java.util.Map;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;


/**
 * JIRA api response for the endpoint /project/{id}
 */
@Data
@JsonIgnoreProperties(ignoreUnknown = true)
public class JiraProjectResponseDTO {

    private static final String SMALL_AVATAR_KEY = "16x16";

    private static final String MEDIUM_AVATAR_KEY = "32x32";

    private String id;
    private String description;
    private String key;
    private String name;
    private Boolean isPrivate;
    private String style;
    private String smallAvatarUrl;
    private String mediumAvatarUrl;

    /**
     * Retrieve project avatar URLs
     *
     * @param avatarUrlsJson object child situated at .avatarUrls in the JSON object tree
     */
    @JsonProperty("avatarUrls")
    public void setAvatarUrls(Map<String, String> avatarUrlsJson) {
        this.smallAvatarUrl = avatarUrlsJson.get(SMALL_AVATAR_KEY);
        this.mediumAvatarUrl = avatarUrlsJson.get(MEDIUM_AVATAR_KEY);
    }
}
