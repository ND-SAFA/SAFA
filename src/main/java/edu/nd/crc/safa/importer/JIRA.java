package edu.nd.crc.safa.importer;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Base64;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import com.jsoniter.JsonIterator;
import com.jsoniter.ValueType;
import com.jsoniter.any.Any;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

@Component
public class JIRA {
    public class Issue {
        String source;
        String key;
        String href;
        boolean isDelegated;
        String status;
        String name;
        String description;
        String type;
        String issuetype;
        List<IssueLink> links;
    }

    public class IssueLink {
        String Type;
        String InwardKey;
        String InwardType;
    }

    private String uri;
    @Autowired @Value("${jira.username:}") String mUsername;
    @Autowired @Value("${jira.password:}") String mPassword;


    public JIRA() {
        uri = "http://spwd.cse.nd.edu:8080/";
    }
    
    private String encodeValue(String value) {
        try {
            return URLEncoder.encode(value, StandardCharsets.UTF_8.toString());
        } catch (Exception e) {
            return "";
        }
    }

    public List<Issue> getIssues(String[] types) throws Exception {
        List<Issue> retVal = new ArrayList<Issue>();

        int remaining = 0, downloaded = 0;
        do {
            // Generate URL
            Map<String, String> requestParams = new HashMap<String, String>();
            requestParams.put("maxResults", "1000");
            requestParams.put("fields", "summary,issuelinks,customfield_10100,description,status,assignee,issuetype");
            requestParams.put("jql",
                    "type in ('Requirement','Hazard','Sub-task','Design Definition','Context','Acceptance Test','Environmental Assumption','Simulation')");

            String encodedURL = requestParams.keySet().stream()
                    .map(key -> key + "=" + encodeValue(requestParams.get(key)))
                    .collect(Collectors.joining("&", "http://spwd.cse.nd.edu:8080/rest/api/2/search?", ""));

            URL url = new URL(encodedURL);
            HttpURLConnection con = (HttpURLConnection) url.openConnection();
            con.setRequestMethod("GET");

            // Add authentication
            String auth = mUsername + ":" + mPassword;
            byte[] encodedAuth = Base64.getEncoder().encode(auth.getBytes(StandardCharsets.UTF_8));
            con.setRequestProperty("Authorization", "Basic " + new String(encodedAuth));

            // Get response
            BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));
            String inputLine;
            StringBuffer content = new StringBuffer();
            while ((inputLine = in.readLine()) != null) {
                content.append(inputLine);
            }
            in.close();

            // Close connection
            con.disconnect();

            // Parse JSON
            Any iter = JsonIterator.deserialize(content.toString());
            remaining = iter.get("total").toInt();

            for (Any i : iter.get("issues").asList()) {
                Issue issue = new Issue();

                issue.source = "JIRA";
                issue.key = i.get("key").toString();
                issue.href = uri + "browse/" + issue.key;

                Any fields = i.get("fields");
                issue.isDelegated = false;
                if (fields.get("assignee").valueType() != ValueType.INVALID) {
                    issue.isDelegated = true;
                }

                issue.status = fields.get("status").get("name").toString();
                issue.name = fields.get("summary").toString();
                issue.description = fields.get("description").toString("");
                issue.issuetype = fields.get("issuetype").get("name").toString();

                issue.type = "";
                if (fields.get("customfield_10100").valueType() != ValueType.INVALID) {
                    if (fields.get("customfield_10100").get("value").valueType() != ValueType.INVALID) {
                        char[] charArray = fields.get("customfield_10100").get("value").toString().toLowerCase()
                                .toCharArray();
                        charArray[0] = Character.toUpperCase(charArray[0]);
                        issue.type = new String(charArray);
                    }
                }

                issue.links = new ArrayList<IssueLink>();
                for (Any l : fields.get("issuelinks").asList()) {

                    IssueLink link = new IssueLink();

                    link.Type = l.get("type").get("name").toString().toUpperCase();

                    Any inward = l.get("inwardIssue");
                    link.InwardKey = inward.get("key").toString();
                    link.InwardType = inward.get("fields").get("issuetype").get("name").toString();

                    issue.links.add(link);
                }

                downloaded++;
                retVal.add(issue);
            }
        } while (downloaded < remaining);

        return retVal;
    }

    public String getUri() {
        return uri;
    }

    public void setUri(String uri) {
        return;
    }
}