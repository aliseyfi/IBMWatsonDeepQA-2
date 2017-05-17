import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Hashtable;
import java.util.Set;

/**
 * 
 */

/**
 * @author badrashiny
 * @Date 05/14/2017
 *
 */
public class Eval {

	/**
	 * compares the predicted alignment to the gold alignment
	 * The files in the predictionDir must have the same names of the files in the goldDir
	 * If the script couldn't find files with the same names of the gold files, it will count these files as mistakes 
	 * @throws IOException 
	 */
	public Eval(String goldDir, String predictionDir) throws IOException {
		// get the files names form the gold directory
		File gDir = new File(goldDir);
		File[] listOfGoldFiles = gDir.listFiles();
		double totalGold=0;
		double totalPredicted=0;
		double recall=0;
		double prec=0;
		for(int i=0;i<listOfGoldFiles.length;i++){
			if(listOfGoldFiles[i].getName().equals(".DS_Store")){//ignore the macOS system file
				continue;
			}
			Hashtable<String,String>goldAlignment=loadFile(listOfGoldFiles[i].getCanonicalPath());
			totalGold+=goldAlignment.size();
			File predictedFile = new File(predictionDir+"/"+listOfGoldFiles[i].getName());
			if(!predictedFile.exists()){
				System.out.println("Predicted file not found: "+predictedFile.getCanonicalPath());
				continue;
			}
			Hashtable<String,String>predictedAlignment=loadFile(predictedFile.getCanonicalPath());
			totalPredicted+=predictedAlignment.size();
			Set<String> keys = predictedAlignment.keySet();
	        for(String point1: keys){
	        	String point2=predictedAlignment.get(point1);
	        	if((goldAlignment.containsKey(point1) && goldAlignment.get(point1).equals(point2))||
	        	   (goldAlignment.containsKey(point2) && goldAlignment.get(point2).equals(point1))){// the order of points is not important. Any of them can be in the first column
	        		recall++;
	        		prec++;	        	
	        	}	            
	        }
		}
		recall=recall/totalGold;
		prec=prec/totalPredicted;
		double fScore=2*recall*prec/(recall+prec);
		System.out.println("Recall = "+Double.toString(recall));
		System.out.println("Precision = "+Double.toString(prec));
		System.out.println("F-Score = "+Double.toString(fScore));	
	}

	private Hashtable<String,String>loadFile(String filePath) throws IOException{
		BufferedReader readbuffer= new BufferedReader(new InputStreamReader(new FileInputStream(filePath), "UTF8"));
		Hashtable<String,String>alignment=new Hashtable<String,String>();
		String strRead;
		while ((strRead=readbuffer.readLine())!=null){
			strRead=strRead.trim();
			if(strRead.isEmpty()){//i.e. empty line
				continue;
			}
			String[] tmp=strRead.split("\t");
			if (tmp.length!=2){//i.e. wrong formatted line. Each line must be 2 columns
				continue;
			}else{
				alignment.put(tmp[0], tmp[1]);
			}						
		}
		readbuffer.close();
		return alignment;		
	}
	/**
	 * @param args
	 * @throws IOException 
	 */
	public static void main(String[] args) throws IOException {
		new Eval(args[0], args[1]);
//		new Eval("Corpus/Gold", "Out");

	}

}
