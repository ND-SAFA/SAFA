package edu.nd.crc.safa.importer.flatfile;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import edu.nd.crc.safa.error.ServerError;
import edu.nd.crc.safa.importer.MySQL;
import edu.nd.crc.safa.importer.vsm.Controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class GenerateFlatFile {

    private MySQL sql;
    public final String PATH_TO_GENERATED_DIR = System.getProperty("user.dir") + "/build/generatedFiles";

    @Autowired
    public GenerateFlatFile(MySQL sql) {
        this.sql = sql;
    }

    public String generateFiles() throws ServerError {

        UploadFlatFile.createDirectory(PATH_TO_GENERATED_DIR);

        List<List<String>> data = sql.generateInfo();
        System.out.println("Generate Info Works");

        if (data.size() == 0) {
            return "No links needed to be generated.";
        }

        for (List<String> row : data) {
            String sourceTable = row.get(0);
            String targetTable = row.get(1);
            String destTable = row.get(2);
            String destFilePath = String.format("%s/%s.csv", PATH_TO_GENERATED_DIR, destTable);

            generateTraceMatrixFile(sourceTable, targetTable, destFilePath, destTable);
        }

        UploadFlatFile.deleteDirectory(PATH_TO_GENERATED_DIR);

        return "Successfully generated link";
    }

    public String getLinkTypes() throws ServerError {
        List<List<String>> traces = sql.getTimTraceData();
        Map<String, ArrayList<String>> sourceTargetMap = new HashMap<String, ArrayList<String>>();
        for (List<String> trace : traces) {
            String key = String.format("\"%s\"", trace.get(1));
            String val = String.format("\"%s\"", trace.get(2));
            sourceTargetMap.computeIfAbsent(key, k -> new ArrayList<>()).add(val);
        }

        String dataDict = sourceTargetMap.toString().replace("=", ":");
        System.out.println(dataDict);
        return String.format("{ \"success\": true, \"data\": %s}", dataDict);
    }

    public void generateTraceMatrixFile(String sourceTable,
                                        String targetTable,
                                        String destFilePath,
                                        String destTable) throws ServerError {
        List<List<String>> sourceData = sql.getArtifactData(sourceTable);
        List<List<String>> targetData = sql.getArtifactData(targetTable);

        Map<String, Collection<String>> sTokens = new HashMap<>();
        Map<String, Collection<String>> tTokens = new HashMap<>();
        for (List<String> doc : sourceData) {
            sTokens.put(doc.get(0), Arrays.asList(doc.get(2).split(" ")));
        }

        for (List<String> doc : targetData) {
            tTokens.put(doc.get(0), Arrays.asList(doc.get(2).split(" ")));
        }

        Controller vsm = new Controller();
        vsm.buildIndex(tTokens.values());
        List<String> lines = new ArrayList<>();
        lines.add("Source,Target,Score");
        for (String sid : sTokens.keySet()) {
            for (String tid : tTokens.keySet()) {
                double score = vsm.getRelevance(sTokens.get(sid), tTokens.get(tid));
                lines.add(String.format("%s,%s,%s", sid, tid, score));
            }
        }

        try {
            Files.write(Paths.get(destFilePath), lines);
        } catch (IOException e) {
            throw new ServerError("error generating trace matrix file", e);
        }
        sql.createGeneratedTraceMatrixTable(destTable, destFilePath);
    }
}
