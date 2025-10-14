package edu.nd.crc.safa.features.permissions;

import java.util.ArrayList;
import java.util.List;
import java.util.Set;

import edu.nd.crc.safa.features.permissions.entities.Permission;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.Getter;

@JsonIgnoreProperties({"cause", "stackTrace", "suppressed", "localizedMessage", "exception", "errors"})
@Getter
public class MissingPermissionException extends SafaError {

    @JsonIgnore
    private final Set<Permission> missingPermissions;

    private final List<String> additionalErrors;

    public MissingPermissionException(Set<Permission> missingPermissions, boolean needAll,
                                      List<String> additionalErrors) {
        super(getPermissionMessage(missingPermissions, needAll, additionalErrors));
        this.missingPermissions = missingPermissions;
        this.additionalErrors = additionalErrors;
    }

    public MissingPermissionException(Set<Permission> missingPermissions, boolean needAll) {
        this(missingPermissions, needAll, new ArrayList<>());
    }

    public MissingPermissionException(Permission missingPermission) {
        this(Set.of(missingPermission), true);
    }

    public MissingPermissionException(List<String> additionalErrors) {
        this(Set.of(), true, additionalErrors);
    }

    public List<String> getPermissions() {
        return getPermissionNames(missingPermissions);
    }

    private static List<String> getPermissionNames(Set<Permission> permissions) {
        return permissions.stream().map(Permission::getName).toList();
    }

    private static String getPermissionMessage(Set<Permission> missingPermissions, boolean needAll,
                                               List<String> additionalErrors) {
        if (missingPermissions.isEmpty()) {
            return "All permissions met, but additional errors were encountered:\n"
                + getAdditionalErrors(additionalErrors);
        }

        return
            String.format(
                "Missing permissions. User must have %s of these permissions: %s",
                (needAll ? "all" : "any"),
                getPermissionNames(missingPermissions)
            );
    }

    private static String getAdditionalErrors(List<String> additionalErrors) {
        return String.join("\n", additionalErrors);
    }
}
