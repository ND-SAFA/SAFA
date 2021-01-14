package edu.nd.crc.safa.importer;
// import sun.awt.windows.WPrinterJob;

import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Collection;
import java.util.Arrays;

import org.springframework.stereotype.Component;

@Component
public class GenerateFlatfile {
    public void generateLinks(String sourcePath, String targetPath, String destPath) throws Exception {
        Path sfile = Paths.get(sourcePath);
        Path tfile = Paths.get(targetPath);
        Path dfile = Paths.get(destPath);

        List<String> sDocs = Files.readAllLines(sfile);
        List<String> tDocs = Files.readAllLines(tfile);
        sDocs.remove(0);
        tDocs.remove(0);
        Map<String, Collection<String>> sTokens = new HashMap<>(), tTokens = new HashMap<>();
        for (String doc : sDocs) {
            String[] parts = doc.split(",");
            String id = parts[1], content = parts[2];
            sTokens.put(id, Arrays.asList(content.split(" ")));
        }
        for (String doc : tDocs) {
            String[] parts = doc.split(",");
            String id = parts[0], content = parts[2];
            tTokens.put(id, Arrays.asList(content.split(" ")));
        }

        VSM vsm = new VSM();
        vsm.buildIndex(tTokens.values());
        List<String> lines = new ArrayList<>();
        lines.add("sid,tid,score");
        for (String sid : sTokens.keySet()) {
            for (String tid : tTokens.keySet()) {
                double score = vsm.getRelevance(sTokens.get(sid), tTokens.get(tid));
                lines.add(String.format("%s,%s,%s", sid, tid, score));
            }
        }
        Files.write(dfile, lines);
    }
}
