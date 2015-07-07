/*
 Copyright (C) 2007 Apple Inc.  All rights reserved.

 Redistribution and use in source and binary forms, with or without
 modification, are permitted provided that the following conditions
 are met:
 1. Redistributions of source code must retain the above copyright
    notice, this list of conditions and the following disclaimer.
 2. Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in the
    documentation and/or other materials provided with the distribution.

 THIS SOFTWARE IS PROVIDED BY APPLE COMPUTER, INC. ``AS IS'' AND ANY
 EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
 PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL APPLE COMPUTER, INC. OR
 CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
 EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
 PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
 PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
 OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE. 
*/

/* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  */

/*
 * AES Cipher function: encrypt 'input' with Rijndael algorithm
 *
 *   takes   byte-array 'input' (16 bytes)
 *           2D byte-array key schedule 'w' (Nr+1 x Nb bytes)
 *
 *   applies Nr rounds (10/12/14) using key schedule w for 'add round key' stage
 *
 *   returns byte-array encrypted value (16 bytes)
 */
function Cipher(input, w) {    
    var Nb = 4;               
    var Nr = w.length / Nb - 1; 
    var state = [[], [], [], []];  
   
    for (var i = 0; i < 4 * Nb; i++) {
        state[i % 4][Math.floor(i / 4)] = input[i];
    }

    AddRoundKey(state, w, 0, Nb);
   
    for (var round = 1; round < Nr; round++) {             
        SubBytes(state, Nb);
        ShiftRows(state, Nb);
        MixColumns(state, Nb);
        AddRoundKey(state, w, round, Nb);
    }
    
    SubBytes(state, Nb);
    ShiftRows(state, Nb);
    AddRoundKey(state, w, Nr, Nb);

    var output = new Array(4 * Nb);  
    for (var i = 0; i < 4 * Nb; i++) {
        output[i] = state[i % 4][Math.floor(i / 4)];
    }
    return output;
}


function SubBytes(s, Nb) {    
    for (var r = 0; r < 4; r++)
        for (var c = 0; c < Nb; c++)
            s[r][c] = Sbox[s[r][c]]; 
   
}


function ShiftRows(s, Nb) {   
    var t = [];
    for (var r = 1; r < 4; r++) {
        for (var c = 0; c < 4; c++)
            t[c] = s[r][(c + r) % Nb];  
        for (var c = 0; c < 4; c++)
            s[r][c] = t[c];         

    }         
   
}


function MixColumns(s, Nb) {  
    for (var c = 0; c < Nb; c++) {
    	var a0 = s[0][c];
    	var b0 = a0 & 0x80 ? a0 << 1 ^ 0x011b : a0 << 1;
    	var a1 = s[1][c];
    	var b1 = a1 & 0x80 ? a1 << 1 ^ 0x011b : a1 << 1;
    	var a2 = s[2][c];
    	var b2 = a2 & 0x80 ? a2 << 1 ^ 0x011b : a2 << 1;
    	var a3 = s[3][c];
    	var b3 = a3 & 0x80 ? a3 << 1 ^ 0x011b : a3 << 1;
    
        s[0][c] = b0 ^ a1 ^ b1 ^ a2 ^ a3; 
        s[1][c] = a0 ^ b1 ^ a2 ^ b2 ^ a3; 
        s[2][c] = a0 ^ a1 ^ b2 ^ a3 ^ b3; 
        s[3][c] = a0 ^ b0 ^ a1 ^ a2 ^ b3; 
    }
   
}

function AddRoundKey(state, w, rnd, Nb) {  // xor Round Key into state S [§5.1.4]
    for (var r = 0; r < 4; r++)
        for (var c = 0; c < Nb; c++)
            state[r][c] ^= w[rnd * 4 + c][r];
    
}


function KeyExpansion(key) {  
    var Nb = 4;            
    var Nk = key.length / 4 
    var Nr = Nk + 6;       

    var w = new Array(Nb * (Nr + 1));
    var temp = new Array(4);

    for (var i = 0; i < Nk; i++) {
        var r = [key[4 * i], key[4 * i + 1], key[4 * i + 2], key[4 * i + 3]];
        w[i] = r;
    }

    for (var i = Nk; i < (Nb * (Nr + 1)) ; i++) {
        w[i] = new Array(4);
        for (var t = 0; t < 4; t++) temp[t] = w[i - 1][t];
        if (i % Nk == 0) {
            temp = SubWord(RotWord(temp));
            for (var t = 0; t < 4; t++) temp[t] ^= Rcon[i / Nk][t];
        } else if (Nk > 6 && i % Nk == 4) {
            temp = SubWord(temp);
        }
        for (var t = 0; t < 4; t++) w[i][t] = w[i - Nk][t] ^ temp[t];
    }

    return w;
}

function SubWord(w) {    
    for (var i = 0; i < 4; i++) w[i] = Sbox[w[i]];
    return w;
}

function RotWord(w) {    
    w[4] = w[0];
    for (var i = 0; i < 4; i++) w[i] = w[i + 1];
    return w;
}


// Sbox is pre-computed multiplicative inverse in GF(2^8) used in SubBytes and KeyExpansion [§5.1.1]
var Sbox = [0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
             0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
             0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
             0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
             0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
             0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
             0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
             0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
             0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
             0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
             0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
             0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
             0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
             0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
             0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
             0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16];

// Rcon is Round Constant used for the Key Expansion [1st col is 2^(r-1) in GF(2^8)] [§5.2]
var Rcon = [[0x00, 0x00, 0x00, 0x00],
             [0x01, 0x00, 0x00, 0x00],
             [0x02, 0x00, 0x00, 0x00],
             [0x04, 0x00, 0x00, 0x00],
             [0x08, 0x00, 0x00, 0x00],
             [0x10, 0x00, 0x00, 0x00],
             [0x20, 0x00, 0x00, 0x00],
             [0x40, 0x00, 0x00, 0x00],
             [0x80, 0x00, 0x00, 0x00],
             [0x1b, 0x00, 0x00, 0x00],
             [0x36, 0x00, 0x00, 0x00]];


/* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  */

/* 
 * Use AES to encrypt 'plaintext' with 'password' using 'nBits' key, in 'Counter' mode of operation
 *                           - see http://csrc.nist.gov/publications/nistpubs/800-38a/sp800-38a.pdf
 *   for each block
 *   - outputblock = cipher(counter, key)
 *   - cipherblock = plaintext xor outputblock
 */
function AESEncryptCtr(plaintext, password, nBits) {
    if (!(nBits == 128 || nBits == 192 || nBits == 256)) return '';  // standard allows 128/192/256 bit keys

    // for this example script, generate the key by applying Cipher to 1st 16/24/32 chars of password; 
    // for real-world applications, a more secure approach would be to hash the password e.g. with SHA-1
    var nBytes = nBits / 8;  
    var pwBytes = new Array(nBytes);
    for (var i = 0; i < nBytes; i++)
        pwBytes[i] = password.charCodeAt(i) & 0xff;
    var key = Cipher(pwBytes, KeyExpansion(pwBytes));
    key = key.concat(key.slice(0, nBytes - 16));  // key is now 16/24/32 bytes long

    // initialise counter block (NIST SP800-38A §B.2): millisecond time-stamp for nonce in 1st 8 bytes,
    // block counter in 2nd 8 bytes
    var blockSize = 16;  // block size fixed at 16 bytes / 128 bits (Nb=4) for AES
    var counterBlock = new Array(blockSize);  // block size fixed at 16 bytes / 128 bits (Nb=4) for AES
    var nonce = (new Date()).getTime();  // milliseconds since 1-Jan-1970

    // encode nonce in two stages to cater for JavaScript 32-bit limit on bitwise ops
    for (var i = 0; i < 4; i++) {
        counterBlock[i] = (nonce >>> i * 8) & 0xff;
        counterBlock[i + 4] = (nonce / 0x100000000 >>> i * 8) & 0xff;
    }
    

    // generate key schedule - an expansion of the key into distinct Key Rounds for each round
    var keySchedule = KeyExpansion(key);

    var blockCount = Math.ceil(plaintext.length / blockSize);
    var ciphertext = new Array(blockCount);  // ciphertext as array of strings

    for (var b = 0; b < blockCount; b++) {

        for (var c = 0; c < 4; c++) {
        	counterBlock[15 - c] = (b >>> c * 8) & 0xff;
        	counterBlock[15 - c - 4] = (b / 0x100000000 >>> c * 8)
        }
        var cipherCntr = Cipher(counterBlock, keySchedule);  // -- encrypt counter block --

        // calculate length of final block:
        var blockLength = b < blockCount - 1 ? blockSize : (plaintext.length - 1) % blockSize + 1;

        var ct = '';
        for (var i = 0; i < blockLength; i++) {  // -- xor plaintext with ciphered counter byte-by-byte --
            var plaintextByte = plaintext.charCodeAt(b * blockSize + i);
            var cipherByte = plaintextByte ^ cipherCntr[i];
            ct += String.fromCharCode(cipherByte);
        }


        ciphertext[b] = escCtrlChars(ct);  // escape troublesome characters in ciphertext
    }

    // convert the nonce to a string to go on the front of the ciphertext
    var ctrTxt = '';
    for (var i = 0; i < 8; i++) ctrTxt += String.fromCharCode(counterBlock[i]);
    ctrTxt = escCtrlChars(ctrTxt);

    // use '-' to separate blocks, use Array.join to concatenate arrays of strings for efficiency
    return ctrTxt + '-' + ciphertext.join('-');
}


/* 
 * Use AES to decrypt 'ciphertext' with 'password' using 'nBits' key, in Counter mode of operation
 *
 *   for each block
 *   - outputblock = cipher(counter, key)
 *   - cipherblock = plaintext xor outputblock
 */
function AESDecryptCtr(ciphertext, password, nBits) {
    if (!(nBits == 128 || nBits == 192 || nBits == 256)) return '';  // standard allows 128/192/256 bit keys

    var nBytes = nBits / 8;  // no bytes in key
    var pwBytes = new Array(nBytes);
    for (var i = 0; i < nBytes; i++) pwBytes[i] = password.charCodeAt(i) & 0xff;
    
    var pwKeySchedule = KeyExpansion(pwBytes);
    
    
    
    var key = Cipher(pwBytes, pwKeySchedule);
    
    key = key.concat(key.slice(0, nBytes - 16));  // key is now 16/24/32 bytes long
    
    var keySchedule = KeyExpansion(key);
    
//    ciphertext = ciphertext.split('-');  // split ciphertext into array of block-length strings 
    
    // recover nonce from 1st element of ciphertext
    var blockSize = 16;  // block size fixed at 16 bytes / 128 bits (Nb=4) for AES
    var counterBlock = new Array(blockSize);
    var ctrTxt = unescCtrlChars(ciphertext[0]);
    
    
    for (var i = 0; i < 8; i++) {
        counterBlock[i] = ctrTxt.charCodeAt(i);
    }
    
    var plaintext = new Array(ciphertext.length - 1);

    for (var b = 1; b < ciphertext.length; b++) {
        // set counter (block #) in last 8 bytes of counter block (leaving nonce in 1st 8 bytes)
        for (var c = 0; c < 4; c++) {
            counterBlock[15 - c] = ((b - 1) >>> c * 8) & 0xff;
            counterBlock[15 - c - 4] = ((b / 0x100000000 - 1) >>> c * 8) & 0xff;
        }
        var cipherCntr = Cipher(counterBlock, keySchedule);  // encrypt counter block//////////////Cipher again
        
        ciphertext[b] = unescCtrlChars(ciphertext[b]);
        
        var pt = '';
        for (var i = 0; i < ciphertext[b].length; i++) {
            // -- xor plaintext with ciphered counter byte-by-byte --
            var ciphertextByte = ciphertext[b].charCodeAt(i);
            var plaintextByte = ciphertextByte ^ cipherCntr[i];
            pt += String.fromCharCode(plaintextByte);
        }
        // pt is now plaintext for this block

        plaintext[b - 1] = pt;  // b-1 'cos no initial nonce block in plaintext
    }

    return plaintext.join('');
}

/* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  */

function escCtrlChars(str) {  // escape control chars which might cause problems handling ciphertext
    return str.replace(/[\0\t\n\v\f\r\xa0'"!-]/g, function (c) { return '!' + c.charCodeAt(0) + '!'; });
}  // \xa0 to cater for bug in Firefox; include '-' to leave it free for use as a block marker

function unescCtrlChars(str) {  // unescape potentially problematic control characters
    return str.replace(/!\d\d?\d?!/g, function (c) { return String.fromCharCode(c.slice(1, -1)); });
}
/* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  */

/*
 * if escCtrlChars()/unescCtrlChars() still gives problems, use encodeBase64()/decodeBase64() instead
 */
var b64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";

function encodeBase64(str) {  // http://tools.ietf.org/html/rfc4648
    var o1, o2, o3, h1, h2, h3, h4, bits, i = 0, enc = '';

    str = encodeUTF8(str);  // encode multi-byte chars into UTF-8 for byte-array

    do {  // pack three octets into four hexets
        o1 = str.charCodeAt(i++);
        o2 = str.charCodeAt(i++);
        o3 = str.charCodeAt(i++);

        bits = o1 << 16 | o2 << 8 | o3;

        h1 = bits >> 18 & 0x3f;
        h2 = bits >> 12 & 0x3f;
        h3 = bits >> 6 & 0x3f;
        h4 = bits & 0x3f;

        // end of string? index to '=' in b64
        if (isNaN(o3)) h4 = 64;
        if (isNaN(o2)) h3 = 64;

        // use hexets to index into b64, and append result to encoded string
        enc += b64.charAt(h1) + b64.charAt(h2) + b64.charAt(h3) + b64.charAt(h4);
    } while (i < str.length);

    return enc;
}

function decodeBase64(str) {
    var o1, o2, o3, h1, h2, h3, h4, bits, i = 0, enc = '';

    do {  // unpack four hexets into three octets using index points in b64
        h1 = b64.indexOf(str.charAt(i++));
        h2 = b64.indexOf(str.charAt(i++));
        h3 = b64.indexOf(str.charAt(i++));
        h4 = b64.indexOf(str.charAt(i++));

        bits = h1 << 18 | h2 << 12 | h3 << 6 | h4;

        o1 = bits >> 16 & 0xff;
        o2 = bits >> 8 & 0xff;
        o3 = bits & 0xff;

        if (h3 == 64) enc += String.fromCharCode(o1);
        else if (h4 == 64) enc += String.fromCharCode(o1, o2);
        else enc += String.fromCharCode(o1, o2, o3);
    } while (i < str.length);

    return decodeUTF8(enc);  // decode UTF-8 byte-array back to Unicode
}

function encodeUTF8(str) {  // encode multi-byte string into utf-8 multiple single-byte characters 
    str = str.replace(
        /[\u0080-\u07ff]/g,  // U+0080 - U+07FF = 2-byte chars
        function (c) {
            var cc = c.charCodeAt(0);
            return String.fromCharCode(0xc0 | cc >> 6, 0x80 | cc & 0x3f);
        }
      );
    str = str.replace(
        /[\u0800-\uffff]/g,  // U+0800 - U+FFFF = 3-byte chars
        function (c) {
            var cc = c.charCodeAt(0);
            return String.fromCharCode(0xe0 | cc >> 12, 0x80 | cc >> 6 & 0x3F, 0x80 | cc & 0x3f);
        }
      );
    return str;
}

function decodeUTF8(str) {  // decode utf-8 encoded string back into multi-byte characters
    str = str.replace(
        /[\u00c0-\u00df][\u0080-\u00bf]/g,                 // 2-byte chars
        function (c) {
            var cc = (c.charCodeAt(0) & 0x1f) << 6 | c.charCodeAt(1) & 0x3f;
            return String.fromCharCode(cc);
        }
      );
    str = str.replace(
        /[\u00e0-\u00ef][\u0080-\u00bf][\u0080-\u00bf]/g,  // 3-byte chars
        function (c) {
            var cc = (c.charCodeAt(0) & 0x0f) << 12 | (c.charCodeAt(1) & 0x3f << 6) | c.charCodeAt(2) & 0x3f;
            return String.fromCharCode(cc);
        }
      );
    return str;
}


function byteArrayToHexStr(b) {  // convert byte array to hex string for displaying test vectors
    var s = '';
    for (var i = 0; i < b.length; i++) s += b[i].toString(16) + ' ';
    return s;
}

/* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  */





/*
* Copyright (C) 2012 HDXPRT Development Community
*
* Licensed under the HDXPRT DEVELOPMENT COMMUNITY MEMBER LICENSE AGREEMENT (the "License");
* you may not use this file except in compliance with the License.
*
* You may obtain a copy of the License by contacting Principled Technologies, Inc.
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
*
* See the License for the specific language governing grants and
* restrictions under the License.
*/

var displayNumperpage = 12;
var tagCloudDsipNum = 50;
var minFontSize = 0.7;
var maxFontSize = 2.5;
var password = "xprt secure notes key!";

/* if (!Modernizr.localstorage) {
	// no native support for HTML5 storage :(
	// window.localStorage is available!
	alert("HTML5 localstorage is not supported by this browser.");
} else {
	// window.localStorage is available!
}*/


/* var m_names = new Array("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug",
		"Sep", "Oct", "Nov", "Dec"); */

function showNotesForDisplay(displayOption, encr) {
//	$('#search').val('');
//	var notesDB;
//	notesDB = new localStorageDB("TouchXPRT_Notes");
	//get the note count
/*	var noteCount = parseInt(localStorage["noteCount"]);
	if (!noteCount) {
		noteCount = 0;
	} */
/*	var notesDetails;
	if (displayOption == 'p1') {
		$("#select-choice-1").prop('selectedIndex', 1);
		notesDetails = notesDB.query("notes", {
			priority : "P1"
		});
	} else if (displayOption == 'new') {
		$("#select-choice-1").prop('selectedIndex', 2);
		var d = new Date();
		var todaysDate = (d.getMonth() + 1) + '/' + d.getDate() + '/'
				+ d.getFullYear();
		todaysDate = "12/01/2012";
		notesDetails = notesDB.query("notes", function(row) { // the callback function is applied to every row in the table			
			if (row.date == todaysDate) { // if it returns true, the row is selected
				return true;
			} else {
				return false;
			}
		});
	} else if (displayOption == 'today') {
		$("#select-choice-1").prop('selectedIndex', 3);
		var d = new Date();
		var todaysDate = (d.getMonth() + 1) + '/' + d.getDate() + '/'
				+ d.getFullYear();
		notesDetails = notesDB.query("notes", function(row) { // the callback function is applied to every row in the table			
			if (row.date == todaysDate) { // if it returns true, the row is selected
				return true;
			} else {
				return false;
			}
		});
	} else {
		notesDetails = notesDB.query("notes");
		
	} */
	var decrypted = [];
	for ( var i = 0; i < encr.length; i++) {
		//console.log(JSON.stringify(notesDetails[i].content));
		decrypted[i] = AESDecryptCtr(encr, password, 256);
		//decrypted[i] = CryptoJS.AES.decrypt(notesDetails[i].content, password,{ format: JsonFormatter }).toString(CryptoJS.enc.Utf8);
		//console.log(decrypted[i].toString(CryptoJS.enc.Utf8));
	}
//	$("#noteCount").html(notesDetails.length + " Notes");
//	$("#noteCount").css("margin", "1em");
//	$("#notesList").html("");
/*	for ( var i = 0; i < displayNumperpage; i++) {
		//$("#notesList").css("border", "2px solid red");	
		var d = new Date(notesDetails[i].date);
		var curr_date = d.getDate();
		var curr_month = d.getMonth();
		var curr_year = d.getFullYear();
		var notesText = "<div class=note id=note" + notesDetails[i].id
				+ "><span class=noteHeader>" + curr_date + " "
				+ m_names[curr_month] + " " + curr_year + "  |  "
				+ notesDetails[i].priority
				+ "</span></br><span class=noteText>" + decrypted[i];
		+"</span></div>";
		$("#notesList").append(notesText).add().css("border",
				"2px solid #6698b5");
		if (notesDetails[i].priority == 'P1') {
			$("#note" + notesDetails[i].id).removeClass("note").addClass(
					"P1note");
		}
		if (notesDetails[i].priority == 'P2') {
			$("#note" + notesDetails[i].id).removeClass("note").addClass(
					"P2note");
		}
		if (notesDetails[i].priority == 'P6') {
			$("#note" + notesDetails[i].id).removeClass("note").addClass(
					"P6note");
		}
	}*/
	createCloud(decrypted);
	return;
}
function syncNotes() {
//	var jqxhr = $.getJSON(
//			"notes.json",
//			function(data) {
				var startTimeSync = new Date().getTime();
//				var hash = CryptoJS.MD5(JSON.stringify(data));
//				localStorage["noteCount"] = data.notes.length;
				// Initialise. If the database doesn't exist, it is created
//				var notesDB;
//				notesDB = new localStorageDB("TouchXPRT_Notes", 'localStorage');

				// Check if the database was just created. Useful for initial database setup
/*				if (notesDB.isNew()) {

					notesDB.createTable("notes", [ "id", "title", "date",
							"priority", "content" ]);
				}
*/
                                var content = new Array("Send party invites for son's birthday.",
                                                        "Jury duty scheduled for July 13th. Reply by EOW",
                                                        "Call caterers",
                                                        "Pickup Dry-Cleaning on Friday for the weekend party. Purchase wine.");
				var i = 0;
				var encryptedArr = [];
				for (i = 0; i < content.length; i++) {
					encryptedArr[i] = AESEncryptCtr(content[i],
							password, 256);
//					encryptedArr[i] = CryptoJS.AES.encrypt(data.notes[i].content,
//							password,{ format: JsonFormatter }).toString();
					//console.log(encryptedArr[i]);
				}
				
				for (i = 0; i < encryptedArr.length; i++) {
/*					notesDB.insert("notes", {
						id : data.notes[i].id,
						title : data.notes[i].title,
						date : data.notes[i].date,
						priority : data.notes[i].priority,
						content : encryptedArr[i]
					}); */
				}
				
//				notesDB.commit();
				
				
				showNotesForDisplay('all', encryptedArr);
				var endTimeSync = new Date().getTime();
				var syncTime = endTimeSync - startTimeSync;
				//$("#notesTimer").html(
				//		(endTimeSync - startTimeSync) + " ms to display");
//				var arrPos = getQueryStringValue("arrPos");
//				var testIndex= getQueryStringValue("testIndex");
//				var run = getQueryStringValue("run");
				//alert("loadtime:" + syncTime );
//				setTimeout(function(){window.location = serverUrl + 'recordlocstoragenotesresults.php?loadtime=' + syncTime + '&arrPos=' + arrPos + '&testIndex=' + testIndex + '&run=' + run;}, globalWorkloadTimeout);

//			}).error(function() {
//		alert("error");
//	});

}

/*function makeCloud2(tags,minCount, minSize, max, delim) {
	//console.log("tags:" + tags);
    var taglinks = [];
    var maxSeen = 0;
    var fontSize = max;
    var divCloud = document.createElement("div");
    var link = null;
  
	divCloud.id = "tag-cloud";
	tags.sort(SortByNum);
	
  
	   for (var i = 0; i<tagCloudDsipNum; i++) {
	
		  if (tags[i].n > minCount) {
			  //console.log("tags[i].w:" + tags[i].w + " tags[i].n:" + tags[i].n);
			  if (tags[i].n > maxSeen) {
				  maxSeen = tags[i].n;
			  }
	
			  //fontSize = tags[i].n;
//	
//			  link = document.createElement("a");
//			  link.rel = "tag";
//			  link.innerHTML = tags[i].w;
//			  link.href = tags[i].w + ".html";
//			  link.fontSize = fontSize;
//	
//			  taglinks.push(link);
		  }
	  }
	  for (var i = 0; i<tagCloudDsipNum; i++) {
	
		  if (tags[i].n > minCount) {
			 
			  //weight = (Math.log(tags[i].n)-Math.log(minSize))/(Math.log(maxSeen)-Math.log(minSize));
//    		  fontSizeOfCurrentTag = minFontSize + Math.round((maxFontSize-minFontSize)*weight);
//			  fontSize = fontSizeOfCurrentTag;
//			  console.log("fontSize:" + fontSize);
			   fontSize = tags[i].n;
			  
			  link = document.createElement("a");
			  link.rel = "tag";
			  link.innerHTML = tags[i].w;
			  link.href = tags[i].w + ".html";
			  link.fontSize = fontSize;
	
			  taglinks.push(link);
		  }
	  }
	//var compSize = (Math.round((((maxSeen - minSize) / (maxSeen - minCount)) + minSize) * 15,0)/10);
	
	var compSizeIncrements = Math.round((maxSeen/10),0);

    for (var i in taglinks) {
        
		var fSize = taglinks[i].fontSize ;
		
		if (fSize < (compSizeIncrements)) {
			 taglinks[i].className = "tag1";
        }
		if (fSize >= (compSizeIncrements) && fSize < (compSizeIncrements * 2)) {
			 taglinks[i].className = "tag2";
        }
		if (fSize >= (compSizeIncrements * 2) && fSize < (compSizeIncrements * 3)) {
			 taglinks[i].className = "tag3";
        }
		if (fSize >= (compSizeIncrements * 3) && fSize < (compSizeIncrements * 4)) {
			 taglinks[i].className = "tag4";
        }
		if (fSize >= (compSizeIncrements * 4) && fSize < (compSizeIncrements * 5)) {
			 taglinks[i].className = "tag5";
        }
		if (fSize >= (compSizeIncrements * 5) && fSize < (compSizeIncrements * 6)) {
			 taglinks[i].className = "tag6";
        }
		 if (fSize >= compSizeIncrements * 6 && fSize < (compSizeIncrements * 7)) {
			 taglinks[i].className = "tag7";
        }
		if (fSize >= (compSizeIncrements * 7) && fSize < (compSizeIncrements * 8)) {

			 taglinks[i].className = "tag8";
        }
		if (fSize >= (compSizeIncrements * 8) && fSize < (compSizeIncrements * 9)) {

			 taglinks[i].className = "tag9";
        }
		if (fSize >= (compSizeIncrements * 9) && fSize < (compSizeIncrements * 10)) {

			 taglinks[i].className = "tag10";
        }
		if (fSize >= (compSizeIncrements * 10)) {
	
			 taglinks[i].className = "tag11";
        }
		

	    divCloud.appendChild(taglinks[i]);
        if (delim) {
            divCloud.appendChild(document.createTextNode(delim))
        }
    }
    return divCloud;
} */

function SortByNum(x,y) {
    return (y.n - x.n); 
  }

function createCloud(notesArr){
	  var wordsJson = [];
	  var allWordsString = new Array();
	  var totalLength = 0;
	  //console.log("notesArr:" + notesArr);
	  
	  for(var i=0;i < notesArr.length;i++){
			  var outString = notesArr[i].replace(/[`~!@#$%^&*()_|+\-=?;:'",.<>\{\}\[\]\\\/]/gi,'');
			  outString = outString.replace(/ the | in | of | an | by | for | and | on | a | that | have | it /gi, ' ');
			  var wordsArr = outString.split(' ');
			  var len = wordsArr.length;
			
			for(var j = 0; j< wordsArr.length; j++) { 
				totalLength++;
				allWordsString[totalLength] = wordsArr[j];
			}
		  }
		  allWordsString.sort();

		  var word = allWordsString[0];
		  var nextWord = "";
		  var numOfWords = 1;
		  for(var x=1; x < allWordsString.length; x++){
			  nextWord = allWordsString[x];
			  if (word != 'null' && nextWord != 'null') {
				if(word == nextWord){
					numOfWords++;
				}else{
					wordsJson.push({w: word, n: numOfWords});
					numOfWords = 1;
					word = nextWord;
				}
		  }
		}
		 // console.log(JSON.stringify(wordsJson));
/*		 var tagsDiv = document.getElementById('divTags');
		  if (tagsDiv) {
			  var cloud = makeCloud2(wordsJson, 0, 1, 1, ' ');
			  tagsDiv.appendChild(cloud);
		  } */
	}

var syncNotesStartTime = new Date();

for (var count_i = 0; count_i < 10000; ++count_i)
    syncNotes();

var syncNotesEndTime = new Date();
var syncNotesTime = syncNotesEndTime - syncNotesStartTime;

print(syncNotesTime);  
