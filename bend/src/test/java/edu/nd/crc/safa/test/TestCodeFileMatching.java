package edu.nd.crc.safa.test;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.nio.file.Path;
import java.util.List;

import edu.nd.crc.safa.utilities.FileUtilities;

import org.junit.jupiter.api.Test;

public class TestCodeFileMatching {

    @Test
    public void testCodeFileMatching() {
        List<Path> matchingPaths = List.of(
            Path.of("CMakeLists.txt"),
            Path.of("path/to/CMakeLists.txt"),
            Path.of("/path/from/root/to/CMakeLists.txt"),
            Path.of("file.cpp"),
            Path.of("path/to/file.cpp"),
            Path.of("/path/from/root/to/file.cpp"),
            Path.of(".gitignore"),
            Path.of("path/to/.gitignore"),
            Path.of("/path/from/root/to/.gitignore")
        );

        List<Path> nonMatchingPaths = List.of(
            Path.of("image.jpeg"),
            Path.of("CMakeLists.txt.png"),
            Path.of("path/with/file.h/in/it.txt"),
            Path.of("weirdFile.gitignore")
        );

        matchingPaths.forEach(
            path -> assertTrue(FileUtilities.isCodeFile(path), "Expected " + path + " to be a code file.")
        );

        nonMatchingPaths.forEach(
            path -> assertFalse(FileUtilities.isCodeFile(path), "Expected " + path + " not to be a code file.")
        );
    }
}
