package edu.nd.crc.safa.config;

import lombok.AccessLevel;
import lombok.NoArgsConstructor;

@NoArgsConstructor(access = AccessLevel.PRIVATE)
public class DefaultArtifactTypeIcons {

    public static String getArtifactIcon(String name) {
        name = cleanArtifactName(name);
        if (name.contains("functional")) {
            return "mdi-function";
        } else if (name.contains("requirement")) {
            return "mdi-clipboard-text";
        } else if (name.contains("design")) {
            return "mdi-math-compass";
        } else if (name.contains("hazard")) {
            return "mdi-hazard-lights";
        } else if (name.contains("environmental")) {
            return "mdi-pine-tree-fire";
        } else {
            return "mdi-help";
        }
    }

    private static String cleanArtifactName(String name) {
        name = name.toLowerCase().strip();
        int length = name.length();
        name = name.charAt(length - 1) == 's' ? name.substring(0, length - 1) : name;
        return name;
    }
}
