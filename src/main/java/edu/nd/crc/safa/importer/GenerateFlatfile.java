package edu.nd.crc.safa.importer;
// import sun.awt.windows.WPrinterJob;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.File;
import java.nio.file.Files;
// import java.nio.file.Path;
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
    public File createGeneratedFilesDir() throws Exception {
        String dir = "/generatedFilesDir";
        File myDir = new File(dir);

        if (!myDir.exists()) {
            if (!myDir.mkdirs()){
                throw new Exception("Error creating Generated Files folder: Path: /generatedFilesDir");
            }
        }

        if (!myDir.isDirectory()) {
            if (!myDir.delete()){
                throw new Exception("Error deleting Generated Files file: Path: /generatedFilesDir");
            }
            if (!myDir.mkdirs()){
                throw new Exception("Error creating Generated Files folder: Path: /generatedFilesDir");
            }
        }

        return myDir;
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

    public String generateFiles() throws Exception {
        Flatfile mFlatfile = new Flatfile();
        Flatfile.ErrorText errorText = mFlatfile.new ErrorText();
        
        String fullPath = "/flatfilesDir/generatedData.json";
        
        File file = new File(fullPath);
        if (!file.exists()) {
            return "{ \"success\": true, \"message\": \"Please upload files.\"}";
        }

        String data = new String(Files.readAllBytes(Paths.get(fullPath)));
        if (data.equals("[]")){
            return "{ \"success\": true, \"message\": \"No links needed to be generated.\"}";
        }

        String flatfileDir = "/flatfilesDir";
        String generatedDir = "/generatedFilesDir";
        String errorFileName = generatedDir + '/' + "ErrorText.csv";
        createGeneratedFilesDir();
        
        JsonIterator iterator = JsonIterator.parse(data);

        List<String> generatedFiles = new ArrayList<String>();
        System.out.println(data);
        System.out.println("Before reading Array");
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
            // System.out.println(destPath);
            // System.out.println(sourcePath);
            // System.out.println(targetPath);
            System.out.println("generateLinks start");
            generateLinks(sourcePath, targetPath, destPath, mFlatfile, errorText);
            System.out.println("generateLinks complete");
             
            // Prints files tracematrix in terminal
            // System.out.println(destPath);
            // try (BufferedReader br = new BufferedReader(new FileReader(destPath))) {
            //     String line;
            //     while ((line = br.readLine()) != null) {
            //         System.out.println(line);
            //     }
            // }
            // System.out.println();

            generatedFiles.add(filename);
        }
        System.out.println("Done reading Array");
        if (generatedFiles.size() > 0) {
            String requiredFilePath = "/flatfilesDir/requiredData.json";

            File requiredFile = new File(requiredFilePath);
            if (!requiredFile.exists()) {
                return "{ \"success\": false, \"message\": \"Error Path: /flatfilesDir/requiredData.json does not exist.\"}";
            }

            String jsonArr = UploadFlatfile.createJsonArray(generatedFiles);
            String requiredData = new String(Files.readAllBytes(Paths.get(requiredFilePath)));
            String regex =  "\"generatedFiles\":\\[.*\\],\"expectedGeneratedFiles\"";
            String replacement =  String.format("\"generatedFiles\":%s,\"expectedGeneratedFiles\"", jsonArr);
            
            String newRequiredData = requiredData.replaceAll(regex, replacement);
            Files.write(Paths.get(requiredFilePath), newRequiredData.getBytes());

            mFlatfile.generateErrorReport(errorText.text, errorFileName);
        }

         // Prints ErrorFile in terminal
        //  System.out.println(errorFileName);
        //  try (BufferedReader br = new BufferedReader(new FileReader(errorFileName))) {
        //      String line;
        //      while ((line = br.readLine()) != null) {
        //          System.out.println(line);
        //      }
        //  }
        //  System.out.println();
        
        return "{ \"success\": true}";
    }
    
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
