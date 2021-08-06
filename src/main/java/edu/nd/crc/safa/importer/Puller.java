package edu.nd.crc.safa.importer;

import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Properties;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import edu.nd.crc.safa.entities.ArtifactBody;
import edu.nd.crc.safa.entities.Project;
import edu.nd.crc.safa.entities.ProjectVersion;
import edu.nd.crc.safa.entities.TraceLink;
import edu.nd.crc.safa.importer.JIRA.Issue;
import edu.nd.crc.safa.repositories.ArtifactBodyRepository;
import edu.nd.crc.safa.repositories.TraceLinkRepository;
import edu.nd.crc.safa.repositories.TraceMatrixRepository;
import edu.nd.crc.safa.responses.ServerError;
import edu.nd.crc.safa.services.Neo4JService;

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

    JIRA mJira;
    public Neo4JService mNeo4JService;
    private ArtifactBodyRepository artifactBodyRepository;
    private TraceMatrixRepository traceMatrixRepository;
    private TraceLinkRepository traceLinkRepository;

    private Pattern mCommitApplies = Pattern.compile(".*(UAV-\\d+).*");
    private Pattern mPackagePattern = Pattern.compile(".*src/(.*)/(.*\\.java)");

    private Set<String> foundNodes = new HashSet<String>();

    @Autowired
    public Puller(Neo4JService neo4JService,
                  JIRA jira,
                  ArtifactBodyRepository artifactBodyRepository,
                  TraceMatrixRepository traceMatrixRepository,
                  TraceLinkRepository traceLinkRepository) {
        this.mNeo4JService = neo4JService;
        this.mJira = jira;
        this.artifactBodyRepository = artifactBodyRepository;
        this.traceMatrixRepository = traceMatrixRepository;
        this.traceLinkRepository = traceLinkRepository;
    }

    public void execute() throws ServerError {
        mNeo4JService.execute();
    }

    public void parseJIRAIssues() {
        try {
            String[] types = new String[]{"Requirement", "Hazard", "Sub-task", "Design Definition", "Context",
                "Acceptance Test", "Environmental Assumption", "Simulation"
            };

            // Loop over issues returned from JIRA and add the found nodes and links
            for (Issue issue : mJira.getIssues(types)) {
                Map<String, Object> data = new HashMap<String, Object>();
                data.put("source", issue.source);
                data.put("isDelegated", issue.isDelegated);
                data.put("status", issue.status);
                data.put("name", issue.name);
                data.put("href", issue.href);
                data.put("description", issue.description);
                data.put("type", issue.type);

                foundNodes.add(issue.key);
                mNeo4JService.addNode(issue.key, issue.issuetype, JsonStream.serialize(data).toString());

                // Check that the link is only an inward link to this node
                if (issue.links.size() > 0) {
                    issue.links.stream().filter((link) -> {
                        return Arrays.asList(types).stream().anyMatch((type) -> {
                            return link.InwardType.equals(type);
                        });
                    }).forEach((link) -> {
                        mNeo4JService.addLink(issue.key, link.Type, link.InwardKey);
                    });
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
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
                    System.out.println("Sorry, unable to find config.properties");
                    return;
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
                                        if (foundNodes.stream().anyMatch((node) -> id.equals(node))) {
                                            mNeo4JService.addSource(m.group(2), rev.name(), pkg, id);
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
            System.err.println(e.toString());
        }
    }

    public String mySQLNeo(Project project, ProjectVersion projectVersion) {
        try {
            insertArtifacts(projectVersion);
            insertConnections(project);
            return "{\"complete\": false}";
        } catch (Exception e) {
            System.out.println(String.format("Completed MysqlToNeo4j with exceptions: %s", e.getMessage()));
            return String.format("{\"complete\": true, \"message\": \"%s\"}", e.getMessage());
        }
    }

    public void insertArtifacts(ProjectVersion projectVersion) throws Exception {
        List<ArtifactBody> artifacts = this.artifactBodyRepository.findByProjectVersion(projectVersion);
        for (ArtifactBody artifact : artifacts) {
            String type = artifact.getTypeName();
            String id = artifact.getName();
            String summary = artifact.getSummary();
            String content = artifact.getContent();

            Map<String, Object> data = new HashMap<String, Object>();
            data.put("source", "Flatfile");
            data.put("isDelegated", "N/A");
            data.put("status", "N/A");
            data.put("name", summary);
            data.put("href", "N/A");
            data.put("description", content);
            data.put("type", type);

            foundNodes.add(id);
            mNeo4JService.addNode(id, type, JsonStream.serialize(data).toString());
        }
    }

    public void insertConnections(Project project) {
        List<TraceLink> projectLinks = traceLinkRepository.findByProject(project);
        for (TraceLink link : projectLinks) {
            if (link.isApproved()) {
                mNeo4JService.addLink(link.getSourceName(), link.getSourceType().getName(), link.getTargetName());
            }
        }
    }
}
