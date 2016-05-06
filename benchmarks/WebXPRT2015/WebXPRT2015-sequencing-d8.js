/*============================================================================*
* Copyright (C) 2015 BenchmarkXPRT Development Community

* Licensed under the BENCHMARKXPRT DEVELOPMENT COMMUNITY MEMBER LICENSE AGREEMENT (the "License");

* you may not use this file except in compliance with the License.

* You may obtain a copy of the License by contacting Principled Technologies, Inc.

* Unless required by applicable law or agreed to in writing, software

* distributed under the License is distributed on an "AS IS" BASIS,

* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

* See the License for the specific language governing grants and

* restrictions under the License.
*============================================================================*/
/*Workload javascript file - launches and controls workload*/
var filesArray = [];
var filesStarted = 0;
var filesDone = 0;
var totalDurationNoWW = 0;
var totalDurationWithWW = 0;
var numberOfWorkers = 0;
var workers = [];
var sequenceStringsArr= [];
var workersStartTime = 0;
var workersEndTime = 0;
var noWorkersStartTime = 0;
var noWorkersEndTime = 0;
var result = [];
var numberOfWorkers = 0;


//////////
var stdGeneticCode="/gc[acgturyswkmbdhvn]/=A," +
    "/[tu]g[ctuy]/=C," +
    "/ga[tcuy]/=D," +
    "/ga[agr]/=E," +
    "/[tu][tu][tcuy]/=F," +
    "/gg[acgturyswkmbdhvn]/=G," +
    "/ca[tcuy]/=H," +
    "/a[tu][atcuwmhy]/=I," +
    "/aa[agr]/=K," +
    "/c[tu][acgturyswkmbdhvn]|[tu][tu][agr]|[ctuy][tu][agr]/=L," +
    "/a[tu]g/=M," +
    "/aa[tucy]/=N," +
    "/cc[acgturyswkmbdhvn]/=P," +
    "/ca[agr]/=Q," +
    "/cg[acgturyswkmbdhvn]|ag[agr]|[cam]g[agr]/=R," +
    "/[tu]c[acgturyswkmbdhvn]|ag[ct]/=S," +
    "/ac[acgturyswkmbdhvn]/=T," +
    "/g[tu][acgturyswkmbdhvn]/=V," +
    "/[tu]gg/=W," +
    "/[tu]a[ctuy]/=Y," +
    "/[tu]a[agr]|[tu]ga|[tu][agr]a/=*";



var patternsArray = [];
//testing
var createFragsDur= 0;
var seqStatsDur = 0;
var findORFsinSeqDur1 = 0;
var findprotseqsDur = 0;
var revSeqDur = 0;
var revCompDur =0;
var generateSeqsWitDur =0;




//////////////



//Data files for the workload
//var files=["sample1.fasta","sample2.fasta","sample3.fasta","sample4.fasta",
//"sample5.fasta","sample6.fasta","sample7.fasta","sample8.fasta"];
var files=["sample1.js","sample2.js","sample3.js","sample4.js",
"sample5.js","sample6.js","sample7.js","sample8.js"];
//var files=["JGAW01000013.1.fasta"];
//$(document).ready(function() {
	//numberOfWorkers = parseInt(getQueryStringValue("workers"));//get the worker number
    numberOfWorkers = 0;   
	//loadImage("img1");
	//setTimeout(function(){loadImage("img2");},1000);
	//setTimeout(function(){loadImage("img3");},2000);
	//setTimeout(function(){},3000);
	start(numberOfWorkers);
//})


function loadImage(imgID){
  $("#" +imgID ).css("display","block");
}

function start(numWorkers){
	//$("#imgs").css("display", "none");
	//$("#dnaSeqSubmit").css("display", "block");

	for(i=0; i<files.length; i++){
		var arr=[];
		arr[0] = files[i];
		//arr[1] = loadXMLDocs("fasta/" + files[i]);
		load("fasta/"+ files[i]);
		arr[1]=samplestr;
		//print(arr[1]);
    
		sequenceStringsArr.push(arr);
	}
	//setTimeout(function(){
	if(numWorkers == 0){
	   sequenceFilesWithoutWW(sequenceStringsArr);
	}else
	{
	  sequenceFilesWithWW(numWorkers);	
	}
	//},1000);
	
}
function sequenceFilesWithoutWW(sequenceStringsArr){
    var totalDurationNoWW=[];
    var  iter=7;
	 for (var iii = 0;iii<iter;iii++)
     { 

	noWorkersStartTime = new Date;

	for(var x=0; x<sequenceStringsArr.length;x++){
		var res =  process(sequenceStringsArr[x][1]);
		//var res =  sequenceStringsArr[x][1];
		var arr = [];
		arr[0]= sequenceStringsArr[x][0];
		arr[1]= res;
		result.push(arr);
	}


	for (var i=0; i<result.length;i++){
		var content = "<div class='fileHeader'>";
		content += result[i][0] + " <button type='button' style='float:right;' onclick='show()'>Show details</button>";

		content += '</div></br>';
		
		//$('#dnaDiv').append(content);
		//$('#dnaDiv').append("<div class='fileinfo' id=file" + i + '></div>');
		var divId = "file" + i;
		createDisplayTable(result[i][1],divId);
		//if(i == result.length - 1 ){
			//$('#file0').css("display","block");
		//}
	}
	
	noWorkersStopTime = new Date;
    totalDurationNoWW[iii] = noWorkersStopTime-noWorkersStartTime;
 }

	

    
    var arrAfterRemovingOutliers = getArrayAfterRemovingOutliers(totalDurationNoWW);
  
    var meanScore=calculate_average(arrAfterRemovingOutliers);

    meanScore=Math.round(meanScore,0);
    print(meanScore);


	//console.log("totalDurationNoWW:" + totalDurationNoWW);
}


function calculate_average(arr) {

     var total=0;
     for (var iii = 0;iii<arr.length;iii++)
     { 
     	total = total + arr[iii];
     }

    var average = (total/arr.length); 
    
    return average;
}

function getArrayAfterRemovingOutliers(arr){   
   var medValArr = calculate_median(arr);   
   
   var medVal = 0;

   if(medValArr[0] == 1){
      median = medValArr[1];
      medVal = medValArr[1];
   }else{
      median = medValArr[1];     
      medVal = medValArr[2];     
   }
   
   arr.sort(sortNumber);
   
   var arrCount = 0;
   var  arrForfirstQuartile=[];

   for(i=0;i <arr.length; i++)
   { 
        if(arr[i] <= medVal)     
        {
            arrForfirstQuartile[arrCount] = arr[i];    
            arrCount++;
        }
    }

     
    var  firstQuartileArr = calculate_median(arrForfirstQuartile);  
    var  arrForthirdQuartile=[];
    arrCount=0;
    for(i=0;i <arr.length; i++)
    {  
        if(arr[i] > medVal)      
        {
            arrForthirdQuartile[arrCount] = arr[i];     
            arrCount++;
        }
    }

    var thirdQuartileArr = calculate_median(arrForthirdQuartile);      
    var  basicFrstQtr=[];
    var  basicThirdQtr=[];
    basicFrstQtr[0] = Math.round(firstQuartileArr[1],2);   
    basicThirdQtr[0]= Math.round(thirdQuartileArr[1],2);
    
    outlierLimit = basicThirdQtr[0] + 1.5 * (basicThirdQtr[0] - basicFrstQtr[0]);       
    var arrAfterRemovingOutliers = [];
    arrCount = 0;
    for(i=0;i <arr.length; i++)
    { 
        if(arr[i] <= outlierLimit )
        {
            arrAfterRemovingOutliers[arrCount] = arr[i];
            arrCount++;
        }
    }
    return arrAfterRemovingOutliers;
}



function sortNumber(a,b)
{
return a - b
}

function calculate_median(arr) {    
  
    arr.sort(sortNumber);

    var count = arr.length; 
    if(count % 2) { 
        median = arr[(count-1)/2];
        oddnum = 1;
    } else { 
        oddnum = 0;
        low = arr[count/2-1];
        high = arr[count/2];
        median = ((low+high)/2);
    }
    
    var returnArray = [];
    returnArray[0] = oddnum;
    returnArray[1] = median;

    return returnArray;
}









function createDisplayTable(resArray,filediv){
	//$("#dnaSeqSubmit").css("display", "none");
	//$("#dnaDiv").css("display","block");
	var content = "<div class='ORFdiv'>Sequence Details:</div>";
	content = "<div class='ORFdetailEven'>";
	content += "<table>" + '<tr><td>' + 'Length:  ' + '</td> <td>' +  resArray[0] + ' base pairs</td></tr>';
	content += '<tr><td>' + resArray[1][0][0] + ': </td> <td>' + resArray[1][0][1]+ '</td></tr>';
	content += '<tr><td>' + resArray[1][1][0] + ': </td> <td>' + resArray[1][1][1] + '</td></tr>';
	content += '<tr><td>' + resArray[1][2][0] + ': </td> <td>' + resArray[1][2][1]  + '</td></tr>';
	content += '<tr><td>' + resArray[1][3][0]+ ': </td> <td>' + resArray[1][3][1]  + '</td></tr>';
	content += "</table>";
	content += "</br>"
	content += "<div class='ORFdiv'>Open Reading Frames:</div></br>";
	content += "<div>";

	for(var i= 0;i<resArray[3].length;i++){
		var cName = "";
		if(resArray[3][i][2] == 1){
			cName = "ORFrame1";
		}else if(resArray[3][i][2] == 2){
			cName = "ORFrame2";
		}else if(resArray[3][i][2] == 3){
			cName = "ORFrame3";
		}
		content += "<div class='" + cName+ "'><p>Start Codon:" + resArray[3][i][0] + " End Codon:"  + resArray[3][i][1] + "</p>";
		var len = resArray[3][i][1] - resArray[3][i][0];
		content += "<p>Length:" + len + " Reading Frame: +" + resArray[3][i][2] + "</p>";
		content += "<p style='word-wrap:break-word;'>Amino Acid sequence: </br>" + resArray[3][i][3] + "</p></div></br>";
	}
	content += "</div></br>";
	//$('#' + filediv).append(content);
}

function sequenceFilesWithWW(nWorkers){
	workersStartTime = new Date;
	if(nWorkers <= sequenceStringsArr.length){
		for (var i=0; i<nWorkers; i++) {                                                                                                                     
			   var worker = initWorker("scripts/sequencingWorker.js");
			   worker.index = i;
			   workers[i] = worker;
			   sendWorkerTask(worker,sequenceStringsArr[i][0],sequenceStringsArr[i][1],i);
			   filesStarted++;
		}   
	}
}

function sendWorkerTask(wker,filename,filetext,wID){
	wker.postMessage({
				'filename' : filename,
				'filetext' : filetext,
				'index' : wID
	});
}

function initWorker(src) {
	var worker = new Worker(src);
	worker.addEventListener("message", messageHandler, true);
	worker.addEventListener("error", errorHandler, true);
	return worker;
}	
function messageHandler(e) {
	var messageType = e.data.type;
	switch (messageType) {
		case ("status"):
			break;
		case ("progress"):
			filesDone++;			
			if(filesStarted< sequenceStringsArr.length){
				var content = "<div class='fileHeader'>";
				content += e.data.filename + " <button type='button' onclick='show()'>Show details</button>";
				content += '</div></br>';
				
				$('#dnaDiv').append(content);
				$('#dnaDiv').append("<div class='fileinfo' id=file" + filesDone + '></div>');
				var divId = "file" + filesDone;

				createDisplayTable(e.data.retData,divId);
				var filecount = filesStarted++;

				sendWorkerTask(workers[e.data.index],sequenceStringsArr[filecount][0],sequenceStringsArr[filecount][1],e.data.index);
			}else{
				var content = "<div class='fileHeader'>";
				content += e.data.filename + " <button type='button' onclick='show()'>Show details</button>";
				content += '</div></br>';
				
				$('#dnaDiv').append(content);
				$('#dnaDiv').append("<div class='fileinfo' id=file" + filesDone + '></div>');
				var divId = "file" + filesDone;

				createDisplayTable(e.data.retData,divId);
				if(filesDone == 1 ){
					$('#file1').css("display","block");
				}
			}
		
			if(filesDone == filesStarted){
				
				$('#file1').css("display","block");		
				for(var i=0; i<workers.length;i++){
					workers[i].terminate();
				}
				workersEndTime = new Date();
				totalDurationWithWW = workersEndTime - workersStartTime;
				var arrPos = getQueryStringValue("arrPos");
				var testIndex= getQueryStringValue("testIndex");
				var run = getQueryStringValue("run");
				
				setTimeout(function(){window.location = serverUrl + 'recorddnaseqresults.php?duration=' + totalDurationWithWW + '&arrPos=' + arrPos + '&testIndex=' + testIndex + '&run=' + run;}, globalWorkloadTimeout);
			}
			break;
		default:
			break;
	}
}

function errorHandler(e) {
	console.log("error: " + e.message);
}	

function loadXMLDocs(fname)
{
  var strRet = "";

  jQuery.ajax({
    url:  fname,
    success: function(data) {
      strRet = data;
    },
    async:false
  });
  return strRet;
}








/*============================================================================*
* Copyright (C) 2015 BenchmarkXPRT Development Community

* Licensed under the BENCHMARKXPRT DEVELOPMENT COMMUNITY MEMBER LICENSE AGREEMENT (the "License");

* you may not use this file except in compliance with the License.

* You may obtain a copy of the License by contacting Principled Technologies, Inc.

* Unless required by applicable law or agreed to in writing, software

* distributed under the License is distributed on an "AS IS" BASIS,

* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

* See the License for the specific language governing grants and

* restrictions under the License.
*============================================================================*/
/*
functions findPotentialStartsAndStops and findORFsinSeq ported from R code to Javascript. Attributed to "Welcome to a Little Book of R for Bioinformatics!"
 - http://a-little-book-of-r-for-bioinformatics.readthedocs.org/en/latest/
*/
/*
 The Sequence Manipulation Suite. Copyright (C) 2000, 2004 Paul Stothard. This program is free software; you can redistribute it and/or modify it under
 the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.
 This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
 See the GNU General Public License for more details. You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc.,
 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
 
 Above license applies to 
 functions: getGeneticCodeMatchExp, getGeneticCodeMatchResult and getProteinSeq. These are used by the function findProteinsInSequence
 and the regex stdGeneticCode
*/
//  The Standard Code (transl_table=1)
//    AAs  = FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG
//  Starts = ---M---------------M---------------M----------------------------
//  Base1  = TTTTTTTTTTTTTTTTCCCCCCCCCCCCCCCCAAAAAAAAAAAAAAAAGGGGGGGGGGGGGGGG
//  Base2  = TTTTCCCCAAAAGGGGTTTTCCCCAAAAGGGGTTTTCCCCAAAAGGGGTTTTCCCCAAAAGGGG
//  Base3  = TCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAG



//
function process(seqText){
	//remove any spaces in the sequence text
	seqText = seqText.replace(/\s/g, '');
	var len = getLength(seqText);
	var pArr=["/g/ (g)1", "/a/ (a)1", "/t/ (t)1", "/c/ (c)1"];
	//get bases and their distribution
	var seqStats = getStats(pArr,seqText,false);
	
	var ORFArr = findORFsinSeq(seqText);
	
	ORFArr = ORFArr.sort(function (a, b) { 
		return a[2] - b[2];
	});

	var reqQuantileRank = Math.ceil(ORFArr.length * (99/100));
	
	//find the protein sequences in the ORFs
	//seqText = "agttgttagtctacgtggaccgacaagaacagtttcgaatcggaagcttgcttaacgtagttctaacagttttttattagagagcagatctctgatgaacaaccaacggaaaaagacgggtcgaccgtctttcaatatgctgaaacgcgcgagaaaccgcgtgtcaactgtttcacagttggcgaagagattctcaaaaggattgctttcaggccaaggacccatgaaattggtgatggcttttatagcattcctaagatttctagccatacctccaacagcaggaattttggctagatggggctcattcaagaagaatggagcgatcaaagtgttacggggtttcaagaaagaaatctcaaacatgttgaacataatgaacaggaggaaaagatctgtgaccatgctcctcatgctgctgcccacagccctggcgttccatctgaccacccgagggggagagccgcacatgatagttagcaagcaggaaagaggaaaat";
	var proteinSeqs = findProteinsInSequence(seqText,ORFArr,stdGeneticCode,reqQuantileRank);

	var resArr = [];
	resArr[0] = len;
	resArr[1] = seqStats;//bases and distribution
	resArr[2] = ORFArr;
	resArr[3] = proteinSeqs;
	
	return resArr;
}

function getLength(seq){
	return seq.length;
}

//array of patterns to look for, sequence string to search, bool - if true include patterns that are not found in return array
function getStats(patternArr,seqStr,includeAllpatterns){
	var statsArray = [];
	//to do calculate GC content %
	for(var i= 0; i<patternArr.length; i++){
		var mE = patternArr[i].match(/\/[^\/]+\//) + "gi";
		mE = eval(mE);
		var res = seqStr.match(mE);
		var arr = [];
		if(res.length >0){
			arr[0] = res[0];
			arr[1] = res.length;
			statsArray[i]= arr;
		}else{
			if(includeAllpatterns){
				arr[0] = mE;
				arr[1] = 0;
				statsArray[i]= arr;
				
			}
		}
		
	}

	return statsArray;
}
//finds the potential start and stop codons
//Output - an array containing 4 arrays. array 1: list of start position,
//array 2: list of corresponding end positions,
//array 3: list of corresponding length of codon
//array 4: list of corresponding name of codon
function findPotentialStartsAndStops(sequence)
{
   var potentialStartsAndStopsArray = [];
   //Define an array with the sequences of potential start and stop codons
   var codons =["ATG","TAA", "TAG", "TGA"];
  
   var allCodonsArray = [];
   //Find the number of occurrences of each type of potential start or stop codon
   for (var i=0; i<codons.length; i++)
   {
	  var codon = codons[i];
	  var myRe = new RegExp("\\" + codon , "gi"),
	  myArray = [];

	  var myResult = [];

	  while ((myArray = myRe.exec(sequence)) !== null) {
		  var arr = [];
		  arr[0] = myArray.index + 1;
		  arr[1] = codon;
		  myResult.push(arr);
	  }
	  allCodonsArray.push(myResult);
   }

   for(x=0; x<allCodonsArray.length;x++){
	   for(y=0;y<allCodonsArray[x].length;y++){
		   var arrMap = [];
		   var codonName = allCodonsArray[x][y][1];
		   var len = codonName.length;
		   arrMap[0] = allCodonsArray[x][y][0];//start
		   arrMap[1] = allCodonsArray[x][y][0] + (len-1);//end
		   arrMap[2] = len;//width
		   arrMap[3] = codonName;//codon
		   potentialStartsAndStopsArray.push(arrMap);
	   }
   }
   
   potentialStartsAndStopsArray.sort(function(first, second){
	  if (first[0] == second[0])
		  return 0;
	  if (first[0] < second[0])
		  return -1;
	  else
		  return 1; 
  });
 
  return potentialStartsAndStopsArray;
	  ////Find all occurrences of codon "codon" in sequence "sequence"
//        occurrences <- matchPattern(codon, sequence)
//        # Find the start positions of all occurrences of "codon" in sequence "sequence"
//        codonpositions <- attr(occurrences,"start")
//        # Find the total number of potential start and stop codons in sequence "sequence"
//        numoccurrences <- length(codonpositions)
//        if (i == 1)
//        {
//           # Make a copy of vector "codonpositions" called "positions"
//           positions <- codonpositions
//           # Make a vector "types" containing "numoccurrences" copies of "codon"
//           types <- rep(codon, numoccurrences)
//        }
//        else
//        {
//           # Add the vector "codonpositions" to the end of vector "positions":
//           positions   <- append(positions, codonpositions, after=length(positions))
//           # Add the vector "rep(codon, numoccurrences)" to the end of vector "types":
//           types       <- append(types, rep(codon, numoccurrences), after=length(types))
//        }
//     }
  // # Sort the vectors "positions" and "types" in order of position along the input sequence:
//     indices <- order(positions)
//     positions <- positions[indices]
//     types <- types[indices]
//     # Return a list variable including vectors "positions" and "types":
//     mylist <- list(positions,types)
}
//returns protein info from input sequence, along with info on reading frame
function findProteinsInSequence(sequence,startsAndstops,stdGeneticCode,numOfOrfs){
	var gCodeArr = stdGeneticCode.split(/,/);
	var retArr = [];
	startsAndstops = startsAndstops.sort(function (a, b) { 
		return b[2] - a[2];
	});
	var count = startsAndstops.length - numOfOrfs;

	for (var i =0; i<count; i++)
	{
          orfstart = startsAndstops[i][0];
          orfstop = startsAndstops[i][1];
	      var remainder =(orfstart-1) % 3;
		  var protBases= "";
		  var protString="";
		  var readingFrame = -1;
		  var subArr=[];
		  if (remainder == 0) // +1 reading frame
			{
				protBases = sequence.slice( orfstart-2, orfstop-1);
				protString = getProteinSeq(protBases,gCodeArr);
				readingFrame= 1;
			}
			else if (remainder == 1)
			{
			   	protBases = sequence.slice( orfstart-2, orfstop-1);
				protString = getProteinSeq(protBases,gCodeArr);
				readingFrame = 2;
			}
			else if (remainder == 2)
			{
			  	protBases = sequence.slice( orfstart-2, orfstop-1);
				protString = getProteinSeq(protBases,gCodeArr);
				readingFrame = 3;
			}
			subArr[0]= orfstart-1;
			subArr[1]= orfstop;
			subArr[2]= readingFrame;
			subArr[3]= protString;
			retArr.push(subArr);
     }
	 
	 return retArr;
}

//function uses the potentialStartsAndStops
//Output - an array containing 3 arrays. array 1: list of start codons,
//array 2: list of corresponding stop codons,
//array 3: list of corresponding lengths
function findORFsinSeq(sequence)
{
   var resArr = [];
   //Make arrays "positions" and "types" containing information on the positions of ATGs in the sequence:
   var potentialStartsAndstops=findPotentialStartsAndStops(sequence);
   var positions = [];
   var types = [];
   for(i=0;i<potentialStartsAndstops.length;i++){
	   positions.push(potentialStartsAndstops[i][0]);
	   types.push(potentialStartsAndstops[i][3]);
   }
  //Make arrays "orfstarts" and "orfstops" to store the predicted start and stop codons of ORFs
  var orfstartsArr = [];
  var orfstopsArr = [];
  //Make an array "orflengths" to store the lengths of the ORFs
  var orflengthsArr=[];
  //put above arrays into an array with each element representing one ORF
  var orfInfoArr=[];

  // Find the length of array "positions"
  var numpositions = positions.length;
  
  //There must be at least one start codon and one stop codon to have an ORF.
  if (numpositions >= 2){
	  for (i=0;i<numpositions;i++)
	  {
		  var posi = positions[i] + 1;
		  var typei = types[i];

		  var found = 0;
		  while (found == 0)
		  {
			  for (j=i+1;j<=numpositions;j++)//for (j in (i+1):numpositions)
			  {
				   var posj = positions[j] +1;
				   var typej = types[j];
				   var posdiff = posj - posi;
				   var posdiffmod3 = posdiff % 3;
				   //Add in the length of the stop codon
				   var orflength = posj - posi + 3;
				   if (typei == "ATG" && (typej == "TAA" || typej == "TAG" || typej == "TGA") && posdiffmod3 == 0)
				   {
						  // # Check if we have already used the stop codon at posj+2 in an ORF
						  var numorfs = orfstopsArr.length;
						  var usedstop = -1;
						  if (numorfs > 0)
						  {
							for (k=1; k<=numorfs;k++)// for (k in 1:numorfs)
							{
								orfstopk = orfstopsArr[k];
								if (orfstopk == (posj + 2)) { usedstop = 1; }
							}
						  }
						  if (usedstop == -1)
						  {
							 orfstartsArr.push(posi);
							 orfstopsArr.push(posj+2);// # Including the stop codon.
							 var t = posj+2;
							 orflengthsArr.push(orflength);
							 var test= sequence.slice(posi, posj+2);

							// orfstarts = append(orfstarts, posi, after=length(orfstarts))
//							   orfstops = append(orfstops, posj+2, after=length(orfstops))// # Including the stop codon.
//							   orflengths = append(orflengths, orflength, after=length(orflengths))
						  }
						  found = 1;
						  break;
				  }
				   if (j == numpositions) { found = 1; }
				}
	  }
  }
 }
//     # Sort the final ORFs by start position:
//     indices <- order(orfstarts)
//     orfstarts <- orfstarts[indices]
//     orfstops <- orfstops[indices]


//     # Find the lengths of the ORFs that we have
//	  orflengthsArr = [];//orflengths <- numeric()
//     numorfs <- length(orfstarts)
	  numorfs = orfstartsArr.length;

	   if((numorfs == orfstopsArr.length) && (numorfs == orflengthsArr.length)){
		   
		   for(var i= 0; i< numorfs;i++){
			   var arr = [];
			   arr[0] = orfstartsArr[i];
			   arr[1] = orfstopsArr[i];
			   arr[2] = orflengthsArr[i];
			   orfInfoArr.push(arr);
		   }
	   }
	  return orfInfoArr;
}

function getGeneticCodeMatchExp (arrayOfPatterns) {
	var geneticCodeMatchExp = new Array (arrayOfPatterns.length);
	
	for (var j = 0; j < arrayOfPatterns.length; j++)	{
			geneticCodeMatchExp[j] = eval(arrayOfPatterns[j].match(/\/.+\//) + "gi");
	}
	return geneticCodeMatchExp;
}

function getGeneticCodeMatchResult (arrayOfPatterns) {
	var geneticCodeMatchResult = new Array (arrayOfPatterns.length);
	for (var j = 0; j < arrayOfPatterns.length; j++)	{
			geneticCodeMatchResult[j] = (arrayOfPatterns[j].match(/=[a-zA-Z\*]/)).toString();
			geneticCodeMatchResult[j] = geneticCodeMatchResult[j].replace(/=/g,"");			
	}
	return geneticCodeMatchResult;
}

function getProteinSeq(dnaSequence, geneticCodeArr)	{
	var geneticCodeMatchExp = getGeneticCodeMatchExp (geneticCodeArr);
	var geneticCodeMatchResult = getGeneticCodeMatchResult (geneticCodeArr);
	//don't translate if fewer than three bases
	if (dnaSequence.replace(/[^A-Za-z]/g, "").length < 3) {
		return "";
	}
	
	dnaSequence = dnaSequence.replace(/(...)/g, 
                    function (str, p1, offset, s) {
                      	return " " + p1 + " ";
                   }
        );
	
	for (var i = 0; i < geneticCodeMatchExp.length; i++)	{
		dnaSequence = dnaSequence.replace(geneticCodeMatchExp[i], geneticCodeMatchResult[i]);
	}

	dnaSequence = dnaSequence.replace(/\S{3}/g, "X");
	dnaSequence = dnaSequence.replace(/\s\S{1,2}$/, "");
	dnaSequence = dnaSequence.replace(/\s/g, "");
	
	return dnaSequence;
}

