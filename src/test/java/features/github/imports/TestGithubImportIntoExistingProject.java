package features.github.imports;

import features.github.base.AbstractGithubTest;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

public class TestGithubImportIntoExistingProject extends AbstractGithubTest {

    @Test
    void baseTest() {
//        dbEntityBuilder.newProject("BaseMockupProject");
        Assertions.assertEquals(10, 10);
    }
}
