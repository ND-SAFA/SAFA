package edu.nd.crc.safa.importer;

import java.io.File;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Collection;
import java.util.Arrays;
import java.util.Scanner; 
import java.util.Set;
import java.util.HashSet;

import com.jsoniter.JsonIterator;
import org.springframework.stereotype.Component;

@Component
public class GenerateFlatfile {
    public String generateFiles() throws Exception {
        String flatfileDir = "/flatfilesDir";
        String generatedDir = "/generatedFilesDir";

        String requiredFilePath = flatfileDir + "/requiredData.json";
        String generatedFilePath = flatfileDir + "/generatedData.json";
        String errorFileName = generatedDir + '/' + "ErrorText.csv";

        UploadFlatfile.createDirectory(flatfileDir);
        UploadFlatfile.createDirectory(generatedDir);

        try {
            pathErrorChecking(requiredFilePath, generatedFilePath);
        } catch(Exception e) {
            return String.format("{ \"success\": false, \"message\": \"%s\"}", e.getMessage());
        }
        
        String data = new String(Files.readAllBytes(Paths.get(generatedFilePath)));
        if (data.equals("[]")){
            return "{ \"success\": true, \"message\": \"No links needed to be generated.\"}";
        }
        
        List<String> generatedFiles = generateFilesHelper(flatfileDir, generatedDir, errorFileName, data);

        updateRequiredJson(requiredFilePath, generatedFiles);

        return "{ \"success\": true, \"message\": \"Successfully generated links\"}";
    }

    public List<String> generateFilesHelper(String flatfileDir, String generatedDir, String errorFileName, String data) throws Exception {
        Flatfile mFlatfile = new Flatfile();
        Flatfile.ErrorText errorText = mFlatfile.new ErrorText();

        List<String> generatedFiles = new ArrayList<String>();
        JsonIterator iterator = JsonIterator.parse(data);

        System.out.println("Start reading Array");
        System.out.println(data);
       
        while (iterator.readArray()) {
            String filename = "";
            String source = "";
            String target = "";

            for (String field = iterator.readObject(); field != null; field = iterator.readObject()) {
                if (field.equals("filename")) {
                    filename = iterator.readString();
                }
                else if (field.equals("source")) {
                    source = iterator.readString();
                }
                else {
                    target = iterator.readString();
                }
            }

            String destPath = generatedDir + "/" + filename;
            String sourcePath = flatfileDir + "/" + source + ".csv";
            String targetPath = flatfileDir + "/" + target + ".csv";

            System.out.println("generateLinks start");
            generateLinks(sourcePath, targetPath, destPath, mFlatfile, errorText);
            System.out.println("generateLinks complete");

            generatedFiles.add(filename);
        }

        System.out.println("Completed reading Array");
        mFlatfile.generateErrorReport(errorText.text, errorFileName);

        return generatedFiles;
    }

    public void generateLinks(String sourcePath, String targetPath, String destPath, Flatfile mFlatfile, Flatfile.ErrorText errorText) throws Exception {
        String sfile = sourcePath;
        String tfile = targetPath;
        String dfile = destPath;

        List<Flatfile.DataEntry> sourceEntry = parseDataFiles(sfile, errorText, mFlatfile);
        List<Flatfile.DataEntry> targetEntry = parseDataFiles(tfile, errorText, mFlatfile);

        Map<String, Collection<String>> sTokens = new HashMap<>(), tTokens = new HashMap<>();
        for (Flatfile.DataEntry doc : sourceEntry) {
            sTokens.put(doc.id, Arrays.asList(doc.content.split(" ")));
        }

        for (Flatfile.DataEntry doc : targetEntry) {
            tTokens.put(doc.id, Arrays.asList(doc.content.split(" ")));
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
        Files.write(Paths.get(dfile), lines);
    }

    public void pathErrorChecking(String requiredFilePath, String generatedFilePath) throws Exception {
        File requiredFile = new File(requiredFilePath);
        if (!requiredFile.exists()) {
            throw new Exception("Please upload files. No files have been uploaded");
        }

        File generatedFile = new File(generatedFilePath);
        if (!generatedFile.exists()) {
            throw new Exception("Please upload files. No files have been uploaded");
        }
    }

    public void updateRequiredJson(String requiredFilePath, List<String> generatedFiles) throws Exception {
        if (generatedFiles.size() > 0) {
            String jsonArr = UploadFlatfile.createJsonArray(generatedFiles);
            String requiredData = new String(Files.readAllBytes(Paths.get(requiredFilePath)));
            String regex =  "\"generatedFiles\":\\[.*\\],\"expectedGeneratedFiles\"";
            String replacement =  String.format("\"generatedFiles\":%s,\"expectedGeneratedFiles\"", jsonArr);
            
            String newRequiredData = requiredData.replaceAll(regex, replacement);
            Files.write(Paths.get(requiredFilePath), newRequiredData.getBytes());
        }
    }

    // Function is a modified version of ParseDataFiles in Flatfile.java. Needs refactoring
    public List<Flatfile.DataEntry> parseDataFiles(String filePath, Flatfile.ErrorText errorText, Flatfile mFlatfile) throws Exception {
        /* Parse Data Files */  
       
        File dataFile = new File(filePath); 
        Scanner rowScanner = new Scanner(dataFile); 
        String headers = rowScanner.nextLine(); 
        String[] headersArray = headers.split(",");

        int index = 0; 
        int headerIndex = 0; 
        String temp = ""; 
        List<String> dataToAdd = new ArrayList<String>();
        int lineNumber = 1;

        List<Flatfile.DataEntry> entryList = new ArrayList<Flatfile.DataEntry>(); 
        Set<String> uniqueIDs = new HashSet<String>();

        while (rowScanner.hasNextLine()) {
            String data = rowScanner.nextLine();
            lineNumber++;
            index = 0; 
            
            while (headerIndex < 3) {      // if line ends but not enough fields, must be # 
                if (Character.compare(data.charAt(index), '\"') == 0) {
                    index += 1;
                    while (Character.compare(data.charAt(index), '\"') != 0) {
                        temp += data.charAt(index);
                        index += 1; 
                        if (index >= data.length()) {
                            data = rowScanner.nextLine();
                            lineNumber++;

                            while (data.length() < 1) {
                                data = rowScanner.nextLine();
                                lineNumber++;
                            }
                            index = 0; 
                        }
                    }
                    headerIndex += 1;
                    index += 2;     // need to move past the following comma 
                    dataToAdd.add(temp); 
                    temp = ""; 
                }
                else if (Character.compare(data.charAt(index), ',') == 0) {
                    headerIndex += 1; 
                    index += 1;
                    dataToAdd.add(temp); 
                    temp = ""; 
                }
                else {
                    temp += data.charAt(index); 
                    index += 1; 
                } 
                if (index >= data.length()) {
                    dataToAdd.add(temp);       
                    temp = ""; 
                    headerIndex += 1; 
                    index = 0; 
                }
            }
            Flatfile.DataEntry dataEntry = mFlatfile.createDataEntry(headersArray, dataToAdd);
            if (uniqueIDs.contains(dataEntry.id)){
                String message = String.format("Entry Ignored Because ID: %s Appears Earlier in CSV.", dataEntry.id);
                String[] pathArray = filePath.split("/");
                String fileName = pathArray[pathArray.length - 1];
                
                mFlatfile.errorGenerator(fileName, lineNumber, message, errorText);
            } else {
                uniqueIDs.add(dataEntry.id);
                entryList.add(dataEntry); 
            }
            headerIndex = 0; 
            dataToAdd = new ArrayList<String>();
        }
        rowScanner.close();
        return entryList;
    }
    
}
