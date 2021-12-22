package edu.nd.crc.safa.importer;

import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Properties;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import edu.nd.crc.safa.importer.JIRA.Issue;
import edu.nd.crc.safa.server.entities.app.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.app.TraceAppEntity;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.services.EntityVersionService;
import edu.nd.crc.safa.server.services.TraceLinkService;

import com.jsoniter.output.JsonStream;
import org.eclipse.jgit.api.Git;
import org.eclipse.jgit.diff.DiffEntry;
import org.eclipse.jgit.diff.DiffFormatter;
import org.eclipse.jgit.revwalk.RevCommit;
import org.eclipse.jgit.transport.UsernamePasswordCredentialsProvider;
import org.eclipse.jgit.util.io.NullOutputStream;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

@Component
public class Puller {
    private final Pattern mCommitApplies = Pattern.compile(".*(UAV-\\d+).*");
    private final Pattern mPackagePattern = Pattern.compile(".*src/(.*)/(.*\\.java)");
    private final Set<String> foundNodes = new HashSet<String>();
    private final JIRA mJira;
    private final EntityVersionService entityVersionService;
    private final TraceLinkService traceLinkService;

    @Value("${git.username:}")
    String gitUsername;
    @Value("${git.password:}")
    String gitPassword;
    @Value("${git.url:}")
    String gitURL;
    @Value("${git.branch:master}")
    String gitBranch;
    @Value("${tim.requiredTraceScore:}")
    Double traceRequiredScore;

    @Autowired
    public Puller(JIRA jira,
                  EntityVersionService entityVersionService,
                  TraceLinkService traceLinkService) {
        this.mJira = jira;
        this.entityVersionService = entityVersionService;
        this.traceLinkService = traceLinkService;
    }

    public void parseJIRAIssues(ProjectVersion projectVersion) throws Exception {
        String[] types = new String[]{"Requirement", "Hazard", "Sub-task", "Design Definition", "Context",
            "Acceptance Test", "Environmental Assumption", "Simulation"
        };

        // Loop over issues returned from JIRA and add the found nodes and links
        List<ArtifactAppEntity> artifacts = new ArrayList<>();
        List<TraceAppEntity> traces = new ArrayList<>();
        for (Issue issue : mJira.getIssues(types)) {
            String issueContent = getIssueContent(issue); // TODO: Revisit what goes into content.
            foundNodes.add(issue.key);

            String artifactName = issue.key;
            String typeName = issue.key;

            artifacts.add(new ArtifactAppEntity(null, typeName, artifactName, "", issueContent));

            // Check that the link is only an inward link to this node
            if (issue.links.size() > 0) {
                issue.links.stream().filter((link) -> Arrays
                        .stream(types)
                        .anyMatch((type) -> link
                            .InwardType
                            .equals(type)))
                    .forEach((link) -> {
                        String source = issue.key;
                        String target = link.InwardKey;
                        TraceAppEntity trace = new TraceAppEntity(source, target);
                        traces.add(trace);
                    });
            }
        }
        entityVersionService.commitVersionArtifacts(projectVersion, artifacts);
        entityVersionService.commitVersionTraces(projectVersion, traces);
    }

    private String getIssueContent(Issue issue) {
        Map<String, Object> data = new HashMap<>();
        data.put("source", issue.source);
        data.put("isDelegated", issue.isDelegated);
        data.put("status", issue.status);
        data.put("name", issue.name);
        data.put("href", issue.href);
        data.put("description", issue.description);
        data.put("type", issue.type);
        return JsonStream.serialize(data);
    }

    /**
     * ParseSourceLinks clones the specified git repository, or pulls the changes of it, before
     * looping through the commits, from the latest to the oldest, and parses the issue id and
     * files modified out of the commit log and adds them, if they are not ignored, to the sources
     * to be applied to the databse.
     */
    public void parseSourceLinks() {
        try (DiffFormatter diffFormatter = new DiffFormatter(NullOutputStream.INSTANCE)) {

            File tmpDir = new File("./safa-git/");

            Git git;
            if (!tmpDir.exists()) {
                git = Git.cloneRepository().setURI(gitURL).setDirectory(tmpDir)
                    .setCredentialsProvider(new UsernamePasswordCredentialsProvider(gitUsername, gitPassword))
                    .setBranch("refs/heads/" + gitBranch).call();
            } else {
                git = Git.open(tmpDir);
                git.pull().setCredentialsProvider(new UsernamePasswordCredentialsProvider(
                    gitUsername, gitPassword)).call();
            }

            diffFormatter.setRepository(git.getRepository());

            Properties prop = new Properties();
            try (InputStream input = Puller.class.getClassLoader().getResourceAsStream("ignore.properties")) {
                if (input == null) {
                    throw new RuntimeException("Sorry, unable to find config.properties");
                }
                prop.load(input);
            } catch (IOException ex) {
                ex.printStackTrace();
            }

            // Parse commit logs
            Set<String> seenFiles = new HashSet<String>();

            Iterable<RevCommit> logs = git.log().call();
            for (RevCommit rev : logs) {
                // Check that we have an issue id inside the commit message
                if (rev.getShortMessage().contains("UAV-")) {
                    Set<String> commitFiles = new HashSet<String>();

                    // Loop over sections of the commit message seperated by a space
                    String[] parts = rev.getShortMessage().split(" ");
                    for (String part : parts) {

                        // Use a regex query to check if the part of the message contains an issue id
                        Matcher commitMatcher = mCommitApplies.matcher(part);
                        if (commitMatcher.find()) {
                            final String id = commitMatcher.group(1);

                            // Get list of files changed between the current revision and its parent
                            List<DiffEntry> mainEntries = diffFormatter.scan(rev, rev.getParent(0));
                            mainEntries.forEach(entry -> {

                                // Use a regex query to check if the file is a java file within the src directory
                                Matcher m = mPackagePattern.matcher(entry.getNewPath());
                                if (m.find()) {
                                    final String pkg = m.group(1).replace("main/java/", "").replace("/", ".");

                                    // Check if the file and id have been specified to be ignored in the properties file
                                    if (prop.containsKey(id)) {
                                        for (String possible : prop.getProperty(id).split(",")) {
                                            if (entry.getNewPath().contains(possible)) {
                                                return;
                                            }
                                        }
                                    }

                                    // Only add it one time as the commits are newest to oldest
                                    if (!seenFiles.contains(entry.getNewPath())) {
                                        if (foundNodes.stream().anyMatch(id::equals)) {
                                            throw new RuntimeException("Adding source in puller has not been restored");
                                        }
                                        commitFiles.add(entry.getNewPath());
                                    }
                                }
                            });
                        }
                    }

                    seenFiles.addAll(commitFiles);
                }
            }
        } catch (Exception e) {
            System.err.println(e);
        }
    }
}
