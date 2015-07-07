/**
 * Javascript Array Weighted
 *
 * Weighted Array test will create array variables that contain countries sorted by their first letter. After this script
 * will start to push, slice, join, concat and pop arrays. After each run counter is increased by one.
 *
 * Test is  mainly imported from old Browsermark.
 *
 * To determine internal score, script will use operations/second (ops): counter / elapsed time in milliseconds x 1000
 * Final score is calculated with formula 1000 x (ops / compare).
 *
 * @version 2.1
 * @author Jouni Tuovinen <jouni.tuovinen@rightware.com>
 * @copyright 2012 Rightware
 **/

// Default guide for benchmark.js
var guide = {
    isDoable : true, // Always doable
    operations : null,
    time : 4000,
    internalCounter : false,
    testName : 'Javascript Array Weighted',
    testVersion : '2.1',
    compareScore : 112454.5,
    isConformity : 0 // Not false but zero because this value is sent through POST which stringify values
};

// predefined list of countries
var countries =
[
    "Afghanistan,Albania,Algeria,Andorra,Angola,Antarctica,Antigua and Barbuda,Argentina,Armenia,Australia,Austria,Azerbaijan",
    "Bahamas,Bahrain,Bangladesh,Barbados,Belarus,Belgium,Belize,Benin,Bermuda,Bhutan,Bolivia,Bosnia and Herzegovina,Botswana,Brazil,Brunei,Bulgaria,Burkina Faso,Burma,Burundi",
    "Cambodia,Cameroon,Canada,Cape Verde,Central African Republic,Chad,Chile,China,Colombia,Comoros,Congo, Democratic Republic,Congo, Republic of the,Costa Rica,Cote d'Ivoire,Croatia,Cuba,Cyprus,Czech Republic",
    "Denmark,Djibouti,Dominica,Dominican Republic",
    "East Timor,Ecuador,Egypt,El Salvador,Equatorial Guinea,Eritrea,Estonia,Ethiopia",
    "Fiji,Finland,France",
    "Gabon,Gambia,Georgia,Germany,Ghana,Greece,Greenland,Grenada,Guatemala,Guinea,Guinea-Bissau,Guyana",
    "Haiti,Honduras,Hong Kong,Hungary",
    "Iceland,India,Indonesia,Iran,Iraq,Ireland,Israel,Italy",
    "Jamaica,Japan,Jordan",
    "Kazakhstan,Kenya,Kiribati,Korea, North,Korea, South,Kuwait,Kyrgyzstan",
    "Laos,Latvia,Lebanon,Lesotho,Liberia,Libya,Liechtenstein,Lithuania,Luxembourg",
    "Macedonia,Madagascar,Malawi,Malaysia,Maldives,Mali,Malta,Marshall Islands,Mauritania,Mauritius,Mexico,Micronesia,Moldova,Mongolia,Morocco,Monaco,Mozambique",
    "Namibia,Nauru,Nepal,Netherlands,New Zealand,Nicaragua,Niger,Nigeria,Norway",
    "Oman,Pakistan,Panama,Papua New Guinea,Paraguay,Peru,Philippines,Poland,Portugal",
    "Qatar",
    "Romania,Russia,Rwanda",
    "Samoa,San Marino, Sao Tome,Saudi Arabia,Senegal,Serbia and Montenegro,Seychelles,Sierra Leone,Singapore,Slovakia,Slovenia,Solomon Islands,Somalia,South Africa,Spain,Sri Lanka,Sudan,Suriname,Swaziland,Sweden,Switzerland,Syria",
    "Taiwan,Tajikistan,Tanzania,Thailand,Togo,Tonga,Trinidad and Tobago,Tunisia,Turkey,Turkmenistan",
    "Uganda,Ukraine,United Arab Emirates,United Kingdom,United States,Uruguay,Uzbekistan",
    "Vanuatu,Venezuela,Vietnam",
    "Yemen",
    "Zambia,Zimbabwe"
];

var test = {
    init : function()
    {
        // Save test but not asynchronous, before continue test must be saved to prevent mismatch error
        /*$.ajax(
        {
            url: '/ajax/set_test',
            async: false,
            type: 'POST',
            data:
            {
                test_name: guide.testName,
                test_version: guide.testVersion
            }
        });*/

        return guide;

    },
    run : function(isFinal, loopCount)
    {
        // loopCount simulate character, example 7 = G
        var i = loopCount % countries.length;

        // Get Countries
        var row = countries[i];
        var selectedCountries = row.split(",");

        // Loop through each selected country
        var predictCountry2 = [];
        var predictCountry3 = [];
        var selectedCountry = '';
        selectedCountries.forEach(function()
        {
            // Shift first element from array
            selectedCountry = selectedCountries.shift();

            // Get country two first and three first chars
            c2 = selectedCountry.slice(0, 2);
            c3 = selectedCountry.slice(0, 3);

            // Ensure value do not exist in predict array
            if (predictCountry2.indexOf(c2) == -1)
            {
                predictCountry2.push(c2);
            }
            if (predictCountry3.indexOf(c3) == -1)
            {
                predictCountry3.push(c3);
            }

            // Finally push country back
            selectedCountries.push(selectedCountry);
        });

        // Concat predict arrays
        var predictCountry = predictCountry2.concat(predictCountry3);

        // Sort predict array
        predictCountry.sort();

        // Simulate next character, again with loopCount
        var nextIndex = loopCount % predictCountry.length;

        // Loop through each selected country
        var reversedCountries = selectedCountries.reverse();

        var returnCountry = '';
        reversedCountries.forEach(function()
        {
            // Pop last element from array
            selectedCountry = reversedCountries.pop().split("");

            // If selected country first n letters are same as in predictCountry[nextIndex]
            var count = predictCountry[nextIndex].length;
            var chars = selectedCountry.splice(0, count).join("");
            if (chars == predictCountry[nextIndex].toString())
            {
                returnCountry = chars + selectedCountry.join("");
            }
        });

        // Operations count increase with +13 because loop contains total of 14 operations
        counter += 13;

        if (isFinal)
        {
            var elapsed = benchmark.elapsedTime();
            var finalScore = counter / elapsed * 1000;
            //benchmark.submitResult(finalScore, guide, {elapsedTime: elapsed, operations: counter, ops: finalScore});
            print("array_weighted: elapsedTime: " + elapsed + " operations: " + counter + " score: " + finalScore);
}

    }
};