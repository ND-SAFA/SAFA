package edu.nd.crc.safa.importer;

import static org.neo4j.driver.v1.Values.parameters;

import java.nio.charset.StandardCharsets;
import java.util.Base64;
import java.util.HashSet;
import java.util.Set;
import java.util.stream.Collectors;

import org.javatuples.Quartet;
import org.javatuples.Triplet;
import org.neo4j.driver.v1.Driver;
import org.neo4j.driver.v1.Record;
import org.neo4j.driver.v1.Session;
import org.neo4j.driver.v1.StatementResult;
import org.neo4j.driver.v1.Transaction;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class Database implements AutoCloseable {
    public class EmptyException extends Exception{
        private static final long serialVersionUID = 7123803818445430594L;
    };

    // Incoming Data
    private Set<Triplet<String, String, String>> mExternalNodeLinkMap = new HashSet<Triplet<String, String, String>>();
    private Set<Triplet<String, String, String>> mExternalNodeMap = new HashSet<Triplet<String, String, String>>();
    private Set<Quartet<String, String, String, String>> mExternalSourceMap = new HashSet<Quartet<String, String, String, String>>();

    // Current Data
    private Set<Triplet<String, String, String>> mNodeLinkMap = new HashSet<Triplet<String, String, String>>();
    private Set<Triplet<String, String, String>> mNodeMap = new HashSet<Triplet<String, String, String>>();
    private Set<Quartet<String, String, String, String>> mSourceMap = new HashSet<Quartet<String, String, String, String>>();

    @Autowired
    Driver driver;
    private static int mLatestVersion = 0;

    public Database() {
    }

    public StatementResult Query(final String query) {
        try (Session session = driver.session()) {
            return session.run(query);
        }
    }

    /**
     * This function creates a new tag within the database which stores the next version to be used by sucessive commands
     */
    public int Tag() throws EmptyException{
        final int nextVersion = this.CurrentVersion() + 1;
        if( nextVersion == 0 ){
            throw new EmptyException();
        }

        try (Session session = driver.session()) {
            try (Transaction tx = session.beginTransaction()) {
                tx.run("MERGE (v:VERSION {id: 'VERSION'}) SET v.number=$version RETURN v;", parameters("version", nextVersion));
                tx.success();
            }
        }
        return nextVersion;
    }

    /**
     * This function calculates the currenty version of the database by searching for the latest tagged version. If one
     * doesn't exist the it checks to see if there are any nodes and if so then we are on the first version.
     */
    public int CurrentVersion() {
        int version = -1;
        
        // Check if we have a version node which stores the current version
        try (Session session = driver.session()) {
            StatementResult result = session.run("MATCH (v:VERSION) RETURN v.number");
            if (result.hasNext()) {
                Record record = result.next();
                version = record.get("v.number").asInt();
            }
        }

        // If we have no version and but we have nodes then our current version is 0
        if( version == -1 ){
            int count = 0;
            try (Session session = driver.session()) {
                StatementResult result = session.run("MATCH (n) RETURN count(*)");
                if (result.hasNext()) {
                    Record record = result.next();
                    count = record.get("count(*)").asInt();
                }
            }
            if( count > 0 ) {
                version = 0;
            }
        }

        return version;
    }

    /**
     * This function clears the entire database of nodes and links
     */
    public void Clear(){
        try (Session session = driver.session()) {
            try (Transaction tx = session.beginTransaction()) {
                if (VERBOSE) {
                    System.out.println("MATCH (n) DETACH DELETE n;");
                }
                tx.run("MATCH (n) DETACH DELETE n");
                tx.success();
            }
        }

        mNodeLinkMap = new HashSet<Triplet<String, String, String>>();
        mNodeMap = new HashSet<Triplet<String, String, String>>();
        mSourceMap = new HashSet<Quartet<String, String, String, String>>();
    }

    private String RemovedDataQuery(int version) {
        return "MATCH (p)-[r:UPDATES]->(c)\n" +
            String.format("WHERE r.version <= %s\n", version) +
            "WITH p, c, r AS rs ORDER BY r.version DESC\n" +
            "WITH p, c, head(collect([p, rs, c])) AS removed\n" +
            "WITH [c in collect(removed) WHERE c[1].type='REMOVE' | [c[0],c[2]]] as excluded\n" +
            "WITH [e in excluded | e[0]] AS eHead, [e in excluded | e[1]] AS eTail, apoc.coll.toSet(apoc.coll.flatten([e in excluded WHERE e[0].id=e[1].id| e[0]])) AS eNo\n" +
            // Find all removed relationships
            "OPTIONAL MATCH (a)-[eR]-(b)\n" +
            "WHERE a IN eHead AND b IN eTail\n" +
            "WITH eNo, apoc.coll.toSet(apoc.coll.flatten(collect(eR))) AS eRelationships\n" +
            // Find any nodes added after wanted version
            "OPTIONAL MATCH (p)-[r:UPDATES]->(c)\n" +
            "WITH eRelationships, eNo, p, c, r AS rs ORDER BY r.version\n" +
            "WITH eRelationships, eNo, p, c, head(collect([p, rs, c])) AS removed\n" +
            String.format("WITH eRelationships, eNo, apoc.coll.toSet([c in collect(removed) WHERE c[1].type='ADD' AND c[1].version > %s | c[2]]) as added\n", version) +
            "WITH eRelationships, apoc.coll.toSet(apoc.coll.flatten([eNo, added])) AS eNodes\n";
    }

    /**
     * Retrieves nodes, sources and links from the database and stores them in hashsets for comparisons later
     */
    public void UpdateDatabaseEntries(){
        mNodeLinkMap = new HashSet<Triplet<String, String, String>>();
        mNodeMap = new HashSet<Triplet<String, String, String>>();
        mSourceMap = new HashSet<Quartet<String, String, String, String>>();

        // Find next version
        mLatestVersion = CurrentVersion();
        
        try (Session session = driver.session()) {
            String command = RemovedDataQuery(mLatestVersion) + " MATCH (n)\n"
                    + " WHERE labels(n)[0]<>'Package' AND labels(n)[0]<>'Code' AND labels(n)[0]<>'VERSION' AND NOT n IN eNodes"
                    + " RETURN n.id AS id, n.DATA as data, labels(n)[0] AS type ORDER BY n.id";
            StatementResult result = session.run(command);
            while (result.hasNext()) {
                Record record = result.next();

                final String id = record.get("id").asString();
                final String type = record.get("type").asString();
                String data = record.get("data").asString();

                // Get modifications to update data
                String mCommand = String.format("MATCH (c) WHERE c.id='%s' MATCH (c)-[r:UPDATES]->(c)\n", id)
                        + String.format("WHERE r.type='MODIFIED' AND r.version <= %d\n", mLatestVersion)
                        + "RETURN r.data AS data ORDER BY r.version DESC LIMIT 1\n";
                StatementResult mResult = session.run(mCommand);
                while (mResult.hasNext()) {
                    data = new String(Base64.getDecoder().decode(mResult.next().get("data").asString()));
                }

                mNodeMap.add(Triplet.with(id, type, data));
            }
        }

        try (Session session = driver.session()) {
            String command = RemovedDataQuery(mLatestVersion) + " MATCH path=((c)<-[r]-(p))"
                    + " WHERE NOT c:Code AND NOT c:Package AND TYPE(r)<>'UPDATES' AND NOT any(e in eRelationships WHERE e IN relationships(path)) AND NOT any(e in eNodes WHERE e IN nodes(path))"
                    + " RETURN p.id AS parent, c.id AS child, TYPE(r) AS type";
            StatementResult result = session.run(command);
            while (result.hasNext()) {
                Record record = result.next();
                mNodeLinkMap.add(Triplet.with(record.get("parent").asString(), record.get("type").asString(),
                        record.get("child").asString()));
            }
        }

        try (Session session = driver.session()) {
            String command = RemovedDataQuery(mLatestVersion) + " MATCH p=((i)-[:IMPLEMENTS]->(parent:Package)-[:CONTAINED_BY]->(node:Code))"
                    + " WHERE NOT any(e in eRelationships WHERE e IN relationships(p)) AND NOT any(e in eNodes WHERE e IN nodes(p))"
                    + " RETURN i.id AS issue, parent.id AS pkg, node.id AS file, node.commit AS commit";
            StatementResult result = session.run(command);
            while (result.hasNext()) {
                Record record = result.next();

                // Get current node paramters
                final String issue = record.get("issue").asString();
                final String file = record.get("file").asString();
                final String pkg = record.get("pkg").asString();
                String commit = record.get("commit").asString();

                // Get modifications to update data
                String mCommand = String.format("MATCH (c:Code) WHERE c.id='%s' MATCH (c)-[r:UPDATES]->(c)\n", file)
                        + String.format("WHERE r.type='MODIFIED' AND r.version <= %d\n", mLatestVersion)
                        + "RETURN r.data AS data ORDER BY r.version DESC LIMIT 1\n";
                StatementResult mResult = session.run(mCommand);
                while (mResult.hasNext()) {
                    commit = mResult.next().get("data").asString();
                }

                // Add node
                mSourceMap.add(Quartet.with(pkg, file, commit, issue));
            }
        }
    }

    public int GetLatestVersion() {
        int version = 0;
        try (Session session = driver.session()) {
            StatementResult result = session.run("MATCH ()-[r:UPDATES]-() RETURN r.version AS version ORDER BY r.version DESC LIMIT 1");
            if (result.hasNext()) {
                Record record = result.next();
                version = record.get("version").asInt();
            }
        }
        return version;
    }

    public int GetNodeCount(final String type){
        int count = 0;
        try (Session session = driver.session()) {
            StatementResult result = session.run(String.format("MATCH (:%s) RETURN count(*)", type));
            count = result.next().get("count(*)").asInt();
        }
        return count;
    }

    public void PrintNodes(final String type){
        try (Session session = driver.session()) {
            StatementResult result = session.run("MATCH (n) WHERE [$type IN LABELS(n)] RETURN n", parameters("type", type));
            if (result.hasNext()) {
                Record record = result.next();
                System.out.println(record.get("n").asMap());
            }
        }
    }

    public void PrintRelationships(final String id){
        try (Session session = driver.session()) {
            StatementResult result = session.run("MATCH ({id: $id})-[r]-() RETURN r", parameters("id", id));
            if (result.hasNext()) {
                Record record = result.next();
                System.out.println(record.get("r").asMap());
            }
        }
    }

    public int GetLinkCount(final String type){
        int count = 0;
        try (Session session = driver.session()) {
            count = session.run("MATCH ()<-[r]-() WHERE TYPE(r)=$type RETURN count(*)", parameters("type", type)).single().get("count(*)").asInt();
        }
        return count;
    }

    public void AddNode(final String id, final String type, final String data){
        mExternalNodeMap.add(Triplet.with(id, type, data));
    }

    public void AddLink(final String parent, final String type, final String child){
        mExternalNodeLinkMap.add(Triplet.with(parent, type, child));
    }

    public void AddSource(final String name, final String commit, final String parent, final String issue){
        mExternalSourceMap.add(Quartet.with(parent, name, commit, issue));
    }

    public void Execute(){
        // Delete old updates
        mLatestVersion = CurrentVersion();

        ProcessOldSources();  
        ProcessOldLinks();    
        ProcessOldIssues();  

        // Delete old updates
        try (Session session = driver.session()) {
            try (Transaction tx = session.beginTransaction()) {
                tx.run("MATCH ()-[r:UPDATES]-() WHERE r.version = $version DELETE r", parameters("version", mLatestVersion));
                tx.success();
            }
        }


        // Update current contents
        UpdateDatabaseEntries();

        if( mLatestVersion == -1 ) {
            mLatestVersion = 0;
        }

        ProcessIssues();
        ProcessLinks();
        ProcesSources();

        // Clear inputted entries
        mExternalNodeLinkMap = new HashSet<Triplet<String, String, String>>();
        mExternalNodeMap = new HashSet<Triplet<String, String, String>>();
        mExternalSourceMap = new HashSet<Quartet<String, String, String, String>>();
    }

    /**
     * This function processes the added, removed and modified links and updates the database to represent the new state.
     */
    private void ProcessIssues(){
        // Find all added issues
        Set<Triplet<String, String, String>> added = mExternalNodeMap.stream().filter((n) -> {
            return !mNodeMap.stream().anyMatch((o) -> {
                return o.getValue0().equals(n.getValue0());
            });
        }).collect(Collectors.toSet());

        // Find all removed issues
        Set<Triplet<String, String, String>> removed = mNodeMap.stream().filter((n) -> {
            return !mExternalNodeMap.stream().anyMatch((o) -> {
                return o.getValue0().equals(n.getValue0());
            });
        }).collect(Collectors.toSet());

        // Find all modified issues
        Set<Triplet<String, String, String>> modified = mExternalNodeMap.stream().filter((n) -> {
            return mNodeMap.stream().anyMatch((o) -> {
                return o.getValue0().equals(n.getValue0()) && o.getValue1().equals(sanitizeType(n.getValue1())) && !o.getValue2().equals(new String(Base64.getEncoder().encodeToString(n.getValue2().getBytes())));
            });
        }).collect(Collectors.toSet());

        // Apply changes to the database
        Set<String> seenTypes = new HashSet<String>();
        try (Session session = driver.session()) {
            try (Transaction tx = session.beginTransaction()) {
                added.forEach((node) -> {
                    if (VERBOSE) {
                        System.out.println("Adding " + node.getValue0() + " " + node.getValue1());
                        System.out.println(String.format("MERGE (:%s {id:'%s', DATA:'%s'});", sanitizeType(node.getValue1()), node.getValue0(), Base64.getEncoder().encodeToString(node.getValue2().getBytes())));
                        System.out.println(String.format("MATCH (c {id:'%s'}) CREATE (c)-[:UPDATES {type:'ADD', version: %d}]->(c);", node.getValue0(), mLatestVersion));
                    }
                    seenTypes.add(node.getValue1());
                    tx.run(String.format("MERGE (:%s {id:$id, DATA:$data})", sanitizeType(node.getValue1())),
                            parameters("id", node.getValue0(), "data",
                                    Base64.getEncoder().encodeToString(node.getValue2().getBytes())));
                    tx.run("MATCH (c {id:$id}) CREATE (c)-[:UPDATES {type:'ADD', version: $version}]->(c)",
                            parameters("id", node.getValue0(), "version", mLatestVersion));
                });

                modified.forEach((node) -> {
                    if (VERBOSE) {
                        System.out.println("Modifying " + node.getValue0() + " " + node.getValue1());
                        System.out.println(String.format("MATCH (c) WHERE c.id='%s' CREATE (c)<-[:UPDATES {type:'MODIFIED', version: %d, data:'%s'}]-(c);", node.getValue0(), mLatestVersion, Base64.getEncoder().encodeToString(node.getValue2().getBytes())));
                    }
                    tx.run("MATCH (c) WHERE c.id=$cid CREATE (c)<-[:UPDATES {type:'MODIFIED', version: $version, data:$data}]-(c)",
                                parameters( "cid", node.getValue0(), "version", mLatestVersion, "data", Base64.getEncoder().encodeToString(node.getValue2().getBytes())));
                });

                removed.forEach((node) -> {
                    if (VERBOSE) {
                        System.out.println("Removing " + node.getValue0() + " " + node.getValue1());
                        System.out.println(String.format("MATCH (c {id:'%s'}) CREATE (c)-[:UPDATES {type:'REMOVE', version: %d}]->(c);", node.getValue0(), mLatestVersion));
                    }
                    tx.run("MATCH (c {id:$id}) CREATE (c)-[:UPDATES {type:'REMOVE', version: $version}]->(c)",
                            parameters("id", node.getValue0(), "version", mLatestVersion));
                });

                tx.success();
            }
        }

        try (Session session = driver.session()) {
            try (Transaction tx = session.beginTransaction()) {
                seenTypes.stream().forEach((type) -> {
                    tx.run(String.format("CREATE INDEX ON :%s(id)", sanitizeType(type)));
                });
                tx.success();
            }
        }
    }

    /**
     * This function first finds all issue nodes that match the current (untagged) version and then finds all issue nodes for the tagged version. 
     * It then creates a set of nodes that are in the current version but not the tagged version and then removes them.
     */
    private void ProcessOldIssues() {
        try (Session session = driver.session()) {
            // Get data for current version
            Set<Triplet<String, String, String>> cNodes = new HashSet<Triplet<String, String, String>>();

            String cCommand = RemovedDataQuery(mLatestVersion) + " MATCH (n)\n"
                    + " WHERE labels(n)[0]<>'Package' AND labels(n)[0]<>'Code' AND labels(n)[0]<>'VERSION' AND NOT n IN eNodes"
                    + " RETURN n.id AS id, n.DATA as data, labels(n)[0] AS type ORDER BY n.id";
            StatementResult cResult = session.run(cCommand);
            while (cResult.hasNext()) {
                Record record = cResult.next();
                final String id = record.get("id").asString();
                final String type = record.get("type").asString();
                final String data = record.get("data").asString();
                cNodes.add(Triplet.with(id, type, data));
            }

            Set<Triplet<String, String, String>> pNodes = new HashSet<Triplet<String, String, String>>();

            // Get data for previous version
            if( mLatestVersion > 0 ){
                String pCommand = "OPTIONAL MATCH (p)-[r:UPDATES]->(c)\n"
                        + "WITH p, c, r AS rs ORDER BY r.version\n"
                        + "WITH p, c, head(collect([p, rs, c])) AS removed\n"
                        + String.format("WITH apoc.coll.toSet([c in collect(removed) WHERE c[1].type='ADD' AND c[1].version > %s | c[2]]) as eNodes\n", mLatestVersion-1)
                        + " MATCH (n)\n"
                        + " WHERE labels(n)[0]<>'Package' AND labels(n)[0]<>'Code' AND labels(n)[0]<>'VERSION' AND NOT n IN eNodes "
                        + " RETURN n.id AS id, n.DATA as data, labels(n)[0] AS type ORDER BY n.id";
                StatementResult pResult = session.run(pCommand);
                while (pResult.hasNext()) {
                    Record record = pResult.next();
                    final String id = record.get("id").asString();
                    final String type = record.get("type").asString();
                    final String data = record.get("data").asString();
                    pNodes.add(Triplet.with(id, type, data));
                }
            }
                
            // Calculate differences
            Set<Triplet<String, String, String>> added = cNodes.stream().filter((n) -> {
                return !pNodes.stream().anyMatch((o) -> {
                    return o.getValue0().equals(n.getValue0());
                });
            }).collect(Collectors.toSet());

            // Remove added issues
            try (Transaction tx = session.beginTransaction()) {
                added.forEach((node) -> {
                    if (VERBOSE) {
                        System.out.println("Removing " + node.getValue0() + " " + node.getValue1());
                        System.out.println(String.format("MATCH (n {id:'%s'}) DETACH DELETE n;", node.getValue0()));
                    }
                    tx.run("MATCH (n {id:$id}) DETACH DELETE n", parameters("id", node.getValue0()));
                });
                tx.success();
            }
        }
    }

    /**
     * This function processes the added and removed links and updates the database to represent the new state.
     */
    public void ProcessLinks(){
        // Find added links
        Set<Triplet<String, String, String>> added = mExternalNodeLinkMap.stream().filter((n) -> {
            return !mNodeLinkMap.stream().anyMatch((o) -> {
                return o.getValue0().equals(n.getValue0()) && o.getValue2().equals(n.getValue2());
            });
        }).collect(Collectors.toSet());

        // Find removed links
        Set<Triplet<String, String, String>> removed = mNodeLinkMap.stream().filter((n) -> {
            return !mExternalNodeLinkMap.stream().anyMatch((o) -> {
                return o.getValue0().equals(n.getValue0()) && o.getValue2().equals(n.getValue2());
            });
        }).collect(Collectors.toSet());

        // Apply changes to the database
        try (Session session = driver.session()) {
            try (Transaction tx = session.beginTransaction()) {
                added.forEach((link) -> {
                    if (VERBOSE) {
                        System.out.println("Adding link between " + link.getValue0() + " " + link.getValue2());
                        System.out.println(String.format("MATCH (p {id:'%s'}) MATCH (c {id:'%s'}) MERGE (c)<-[:%s]-(p);", link.getValue0(), link.getValue2(), link.getValue1()));
                        System.out.println(String.format("MATCH (c {id:'%s'})<-[r]-(p {id:'%s'}) WHERE NOT exists(r.type) CREATE (c)<-[:UPDATES {type:'ADD', version: %d}]-(p);", link.getValue2(), link.getValue0(), mLatestVersion));
                    }
                    tx.run(String.format("MATCH (p {id:$pid}) MATCH (c {id:$cid}) MERGE (c)<-[:%s]-(p)",
                            link.getValue1()), parameters("pid", link.getValue0(), "cid", link.getValue2()));
                    tx.run("MATCH (c {id:$cid})<-[r]-(p {id:$pid}) WHERE NOT exists(r.type) CREATE (c)<-[:UPDATES {type:'ADD', version: $version}]-(p)",
                            parameters("pid", link.getValue0(), "cid", link.getValue2(), "version",
                                    mLatestVersion));
                });

                removed.forEach((link) -> {
                    if (VERBOSE) {
                        System.out.println("Removing link between " + link.getValue0() + " " + link.getValue2());
                        System.out.println(String.format("MATCH (c {id:'%s'})<-[r]-(p {id:'%s'}) WHERE NOT exists(r.type) CREATE (c)<-[:UPDATES {type:'REMOVE', version: %d}]-(p)", link.getValue2(), link.getValue0(), mLatestVersion));
                    }
                    tx.run("MATCH (c {id:$cid})<-[r]-(p {id:$pid}) WHERE NOT exists(r.type) CREATE (c)<-[:UPDATES {type:'REMOVE', version: $version}]-(p)",
                            parameters("pid", link.getValue0(), "cid", link.getValue2(), "version", mLatestVersion));
                });

                tx.success();
            }
        }
    }

    /**
     * This function first finds all links that match the current (untagged) version and then finds all links for the tagged version. 
     * It then creates a set of links that are in the current version but not the tagged version and then removes them.
     */
    private void ProcessOldLinks(){
        try (Session session = driver.session()) {
            // Get data for current version
            Set<Triplet<String, String, String>> cLinks = new HashSet<Triplet<String, String, String>>();

            String cCommand = RemovedDataQuery(mLatestVersion) + " MATCH path=((c)<-[r]-(p))"
                    + " WHERE NOT c:Code AND NOT c:Package AND TYPE(r)<>'UPDATES' AND NOT any(e in eRelationships WHERE e IN relationships(path)) AND NOT any(e in eNodes WHERE e IN nodes(path))"
                    + " RETURN p.id AS parent, c.id AS child, TYPE(r) AS type";
            StatementResult cResult = session.run(cCommand);
            while (cResult.hasNext()) {
                Record record = cResult.next();
                cLinks.add(Triplet.with(record.get("parent").asString(), record.get("type").asString(), record.get("child").asString()));
            }

            // Get data for previous version
            Set<Triplet<String, String, String>> pLinks = new HashSet<Triplet<String, String, String>>();

            if( mLatestVersion > 0 ){
                String pCommand = "OPTIONAL MATCH (p)-[r:UPDATES]->(c)\n"
                    + "WITH p, c, r AS rs ORDER BY r.version\n"
                    + "WITH p, c, head(collect([p, rs, c])) AS removed\n"
                    + String.format("WITH apoc.coll.toSet([c in collect(removed) WHERE c[1].type='ADD' AND c[1].version > %s | c[2]]) as eNodes\n", mLatestVersion-1)
                    + " MATCH path=((c)<-[r]-(p))"
                    + " WHERE NOT c:Code AND NOT c:Package AND TYPE(r)<>'UPDATES' AND NOT any(e in eNodes WHERE e IN nodes(path))"
                    + " RETURN p.id AS parent, c.id AS child, TYPE(r) AS type";
                StatementResult pResult = session.run(pCommand);
                while (pResult.hasNext()) {
                    Record record = pResult.next();
                    pLinks.add(Triplet.with(record.get("parent").asString(), record.get("type").asString(), record.get("child").asString()));
                }
            }
                
            // Calculate differences
            Set<Triplet<String, String, String>> added = cLinks.stream().filter((n) -> {
                return !pLinks.stream().anyMatch((o) -> {
                    return o.getValue0().equals(n.getValue0());
                });
            }).collect(Collectors.toSet());

            // Remove added issues
            try (Transaction tx = session.beginTransaction()) {
                added.forEach((link) -> {
                    if (VERBOSE) {
                        System.out.println("Removing link between " + link.getValue0() + " " + link.getValue2());
                        System.out.println(String.format("MATCH (p {id:'%s'})-[r]->(c {id:'%s'}) DETACH DELETE;", link.getValue0(), link.getValue1(), link.getValue2()));
                    }
                    tx.run(String.format("MATCH (p {id:$pid})-[r:%s]->(c {id:$cid}) DETACH DELETE r", link.getValue1()), parameters("pid", link.getValue0(), "cid", link.getValue2()));
                });
                tx.success();
            }
        }
    }

    /**
     * This function processes the added, removed and modified source nodes and updates the database to represent the new state.
     */
    private void ProcesSources(){
        // Find all source added nodes since tagged version
        Set<Quartet<String, String, String, String>> added = mExternalSourceMap.stream().filter((n) -> {
            return !mSourceMap.stream().anyMatch((o) -> {
                return o.getValue0().equals(n.getValue0()) && o.getValue1().equals(n.getValue1()) && o.getValue3().equals(n.getValue3());
            });
        }).collect(Collectors.toSet());

        // Find all source nodes removed since tagged version
        Set<Quartet<String, String, String, String>> removed = mSourceMap.stream().filter((n) -> {
            return !mExternalSourceMap.stream().anyMatch((o) -> {
                return o.getValue0().equals(n.getValue0()) && o.getValue1().equals(n.getValue1()) && o.getValue3().equals(n.getValue3());
            });
        }).collect(Collectors.toSet());

        // Find all source nodes modified since tagged version
        Set<Quartet<String, String, String, String>> modified = mExternalSourceMap.stream().filter((n) -> {
            return mSourceMap.stream().anyMatch((o) -> {
                return o.getValue0().equals(n.getValue0()) && o.getValue1().equals(n.getValue1()) && !o.getValue2().equals(n.getValue2()) && o.getValue3().equals(n.getValue3());
            });
        }).collect(Collectors.toSet());

        // Apply changes to the database
        try (Session session = driver.session()) {
            try (Transaction tx = session.beginTransaction()) {
                added.forEach((file) -> {
                    if (VERBOSE) {
                        System.out.println("Adding: " + file.getValue0() + " " + file.getValue1() + " " + mLatestVersion);
                        System.out.println(String.format("MERGE (:Package {id:'%s', issue:'%s'});", file.getValue0(), file.getValue3()));
                        System.out.println(String.format("MATCH (p {id:'%s' }) MATCH (c:Package {id:'%s', issue:'%s'}) MERGE (c)<-[:IMPLEMENTS]-(p);", file.getValue3(), file.getValue3(), file.getValue0()));
                        System.out.println(String.format("MERGE (:Code {id:'%s', commit:'%s', issue:'%s'});", file.getValue1(), file.getValue2(), file.getValue3()));
                        System.out.println(String.format("MATCH (p:Package {id:'%s', issue:'%s'}) MATCH (c:Code {id:'%s', commit:'%s', issue:'%s'}) MERGE (c)<-[:CONTAINED_BY]-(p);", file.getValue3(), file.getValue0(), file.getValue1(), file.getValue2(), file.getValue3()));
                        System.out.println(String.format("MATCH (c:Code {id:'%s', commit:'%s', issue:'%s'})<-[:CONTAINED_BY]-(p:Package {id:'%s', issue:'%s'}) CREATE (c)<-[:UPDATES {type:'ADD', version: %d}]-(p);", file.getValue1(), file.getValue2(), file.getValue3(), file.getValue3(), file.getValue0(), mLatestVersion));
                    }

                    // Create package
                    tx.run("MERGE (:Package {id:$package, issue:$issue})", parameters("package", file.getValue0(), "issue", file.getValue3()));
                    tx.run("MATCH (p {id:$pid}) MATCH (c:Package {id:$package, issue:$issue}) MERGE (c)<-[:IMPLEMENTS]-(p)",
                            parameters("pid", file.getValue3(), "package", file.getValue0(), "issue", file.getValue3()));

                    // Create file
                    tx.run("MERGE (:Code {id:$file, commit:$commit, issue:$issue})", parameters("file", file.getValue1(), "commit", file.getValue2(), "issue", file.getValue3()));
                    tx.run("MATCH (p:Package {id:$pkg, issue:$issue}) MATCH (c:Code {id:$file, commit:$commit, issue:$issue}) MERGE (c)<-[:CONTAINED_BY]-(p)",
                            parameters("pkg", file.getValue0(), "file", file.getValue1(), "issue", file.getValue3(), "commit", file.getValue2()));
                    tx.run("MATCH (c:Code {id:$cid, commit:$commit, issue:$issue})<-[:CONTAINED_BY]-(p:Package {id:$pid, issue:$issue}) CREATE (c)<-[:UPDATES {type:'ADD', version: $version}]-(p)",
                            parameters("pid", file.getValue0(), "cid", file.getValue1(), "version", mLatestVersion, "issue", file.getValue3(), "commit", file.getValue2()));
                });

                modified.forEach((file) -> {
                    if (VERBOSE) {
                        System.out.println("Modifying: " + file.getValue0() + " " + file.getValue1() + " " + mLatestVersion);
                        System.out.println(String.format("MATCH (c:Code) WHERE c.id='%s' CREATE (c)<-[:UPDATES {type:'MODIFIED', version: %d, data:'%s'}]-(c);", file.getValue1(), mLatestVersion+1, file.getValue2()));
                    }
                    tx.run("MATCH (c:Code) WHERE c.id=$cid CREATE (c)<-[:UPDATES {type:'MODIFIED', version: $version, data:$data}]-(c)",
                            parameters( "cid", file.getValue1(), "version", mLatestVersion, "data", file.getValue2()));
                });

                removed.forEach((file) -> {
                    if (VERBOSE) {
                        System.out.println("Removing: " + file.getValue0() + " " + file.getValue1() + " " + mLatestVersion);
                        System.out.println(String.format("MATCH (c:Code {id:'%s', issue:'%s'})<-[:CONTAINED_BY]-(p:Package {id:'%s', issue:'%s'}) CREATE (c)<-[:UPDATES {type:'REMOVE', version: %d}]-(p);", file.getValue1(), file.getValue3(), file.getValue3(), file.getValue0(), mLatestVersion+1));
                    }
                    tx.run("MATCH (c:Code {id:$cid, issue:$issue})<-[:CONTAINED_BY]-(p:Package {id:$pid, issue:$issue}) CREATE (c)<-[:UPDATES {type:'REMOVE', version: $version}]-(p)",
                            parameters("pid", file.getValue0(), "cid", file.getValue1(), "version", mLatestVersion, "issue", file.getValue3()));
                });

                tx.success();
            }
        }
    }

    /**
     * This function first finds all source nodes that match the current (untagged) version and then finds all source nodes for the tagged version. 
     * It then creates a set of nodes that are in the current version but not the tagged version and then removes them.
     */
    private void ProcessOldSources() {
        // Handles Sources
        try (Session session = driver.session()) {
            // Get data for current version
            Set<Quartet<String, String, String, String>> cSources = new HashSet<Quartet<String, String, String, String>>();

            String cCommand = RemovedDataQuery(mLatestVersion) + " MATCH p=((i)-[:IMPLEMENTS]->(parent:Package)-[:CONTAINED_BY]->(node:Code))"
                    + " WHERE NOT any(e in eRelationships WHERE e IN relationships(p)) AND NOT any(e in eNodes WHERE e IN nodes(p))"
                    + " RETURN i.id AS issue, parent.id AS pkg, node.id AS file, node.commit AS commit";
            StatementResult cResult = session.run(cCommand);
            while (cResult.hasNext()) {
                Record record = cResult.next();

                // Get current node paramters
                final String issue = record.get("issue").asString();
                final String file = record.get("file").asString();
                final String pkg = record.get("pkg").asString();
                final String commit = record.get("commit").asString();

                // Add node
                cSources.add(Quartet.with(pkg, file, commit, issue));
            }

            // Get data for previous version
            Set<Quartet<String, String, String, String>> pSources = new HashSet<Quartet<String, String, String, String>>();

            if( mLatestVersion > 0 ){
                String pCommand = "OPTIONAL MATCH (p)-[r:UPDATES]->(c)\n"
                    + "WITH p, c, r AS rs ORDER BY r.version\n"
                    + "WITH p, c, head(collect([p, rs, c])) AS removed\n"
                    + String.format("WITH apoc.coll.toSet([c in collect(removed) WHERE c[1].type='ADD' AND c[1].version > %s | c[2]]) as eNodes\n", mLatestVersion-1)
                    + " MATCH p=((i)-[:IMPLEMENTS]->(parent:Package)-[:CONTAINED_BY]->(node:Code))"
                    + " WHERE NOT any(e in eNodes WHERE e IN nodes(p))"
                    + " RETURN i.id AS issue, parent.id AS pkg, node.id AS file, node.commit AS commit";
                StatementResult pResult = session.run(pCommand);
                while (pResult.hasNext()) {
                    Record record = pResult.next();

                    // Get current node paramters
                    final String issue = record.get("issue").asString();
                    final String file = record.get("file").asString();
                    final String pkg = record.get("pkg").asString();
                    final String commit = record.get("commit").asString();

                    // Add node
                    pSources.add(Quartet.with(pkg, file, commit, issue));
                }
            }
                
            // Calculate differences
            Set<Quartet<String, String, String, String>> added = cSources.stream().filter((n) -> {
                return !pSources.stream().anyMatch((o) -> {
                    return o.getValue0().equals(n.getValue0()) && o.getValue1().equals(n.getValue1()) && o.getValue3().equals(n.getValue3());
                });
            }).collect(Collectors.toSet());

            // Remove added issues
            try (Transaction tx = session.beginTransaction()) {
                added.forEach((file) -> {
                    if (VERBOSE) {
                        System.out.println("Removing: " + file.getValue0() + " " + file.getValue1());
                        System.out.println(String.format("MATCH (:Code {id:'%s', commit:'%s'})<-[r:CONTAINED_BY]-(:Package {id:'%s', issue:'%s'}) DETACH DELETE r;", file.getValue1(), file.getValue2(), file.getValue3(), file.getValue0(), mLatestVersion));
                        System.out.println(String.format("MATCH (c:Code {id:'%s', commit:'%s'}) DETACH DELETE c;", file.getValue1(), file.getValue2()));
                    }
                
                    tx.run("MATCH (:Code {id:$cid, commit:$commit})<-[r:CONTAINED_BY]-(:Package {id:$pid, issue:$issue}) DETACH DELETE r;", parameters("cid", file.getValue1(), "commit", file.getValue2(), "pid", file.getValue3(), "issue", file.getValue0()));
                    tx.run("MATCH (c:Code {id:$cid, commit:$commit}) DETACH DELETE c;", parameters("cid", file.getValue1(), "commit", file.getValue2()));
                });
                tx.success();
            }
        }
    }

    @Override
    public void close() throws Exception {
        driver.close();
    }

    private String sanitizeType(final String type) {
        return type.replace(" ", "").replace("-", "");
    }

    public boolean VERBOSE = false;
}