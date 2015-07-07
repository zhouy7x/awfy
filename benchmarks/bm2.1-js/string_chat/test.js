/**
 * Javascript String Chat
 *
 * String Chat test will simulate simple chat: each message is checked and if it contains "bad words",
 * script will remove word from message before accepting it. After each run counter is increased by one.
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
    testName : 'Javascript String Chat',
    testVersion : '2.1',
    compareScore : 91210.6,
    isConformity : 0 // Not false but zero because this value is sent through POST which stringify values
};

var modifiedMessages = [];
var test = {
    messages: [
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        "Mauris condimentum nisl vitae nisl elementum, sit amet posuere lectus porta.",
        "Pellentesque sit amet elit non velit congue adipiscing et eget justo.",
        "Donec at nunc adipiscing, commodo orci sed, rutrum augue.",
        "Fusce volutpat dui in leo sollicitudin, a consequat augue lobortis.",
        "Mauris lobortis nisi a felis volutpat, vel fermentum lectus elementum.",
        "Curabitur ac lectus non massa aliquet fermentum suscipit vel neque.",
        "Duis accumsan mi vel metus consequat, et posuere arcu tincidunt.",
        "Etiam ut nisi condimentum, blandit turpis a, porta turpis.",
        "Donec congue lectus at facilisis malesuada.",
        "Aliquam vel mauris at erat luctus blandit ut vitae libero.",
        "Pellentesque suscipit elit eget sem feugiat, a dictum erat congue.",
        "Morbi posuere ipsum eu magna dictum, quis pulvinar quam mattis.",
        "Fusce mattis dui sed luctus tincidunt.",
        "Nulla lobortis velit in nibh porttitor consequat.",
        "Curabitur feugiat erat ut magna tristique, in gravida risus sodales.",
        "Suspendisse tempor augue sed nibh tincidunt scelerisque.",
        "Pellentesque sodales lectus nec justo placerat, et ultricies quam elementum.",
        "Maecenas vehicula augue non lectus sagittis vulputate.",
        "Donec eu mauris at libero convallis semper eleifend id sem.",
        "Curabitur vestibulum erat eget semper vehicula.",
        "Curabitur placerat erat at dignissim molestie.",
        "Ut pharetra sapien non justo commodo vehicula.",
        "Donec pretium nulla nec dui sollicitudin imperdiet.",
        "In auctor justo id fermentum gravida.",
        "Vivamus vitae elit quis libero dictum vehicula at ac purus.",
        "Donec in urna sit amet lectus hendrerit sagittis ac nec diam.",
        "Etiam vehicula erat vel rutrum sodales.",
        "Morbi scelerisque ipsum a urna iaculis pretium.",
        "Mauris et enim eleifend, mollis ligula pellentesque, tempor velit.",
        "Maecenas in elit eget augue mattis posuere vitae eu neque.",
        "In accumsan dolor ac ultrices lobortis.",
        "Quisque non massa et arcu elementum mattis.",
        "Aliquam tincidunt purus at felis scelerisque, feugiat mollis eros congue.",
        "Vestibulum quis tellus ut orci lobortis porttitor.",
        "Morbi nec purus vel justo porttitor adipiscing.",
        "Donec ac ipsum interdum, vehicula ante non, iaculis felis.",
        "Proin vitae odio sed ligula hendrerit varius eu sodales orci.",
        "Nulla suscipit lectus a quam scelerisque fringilla.",
        "Phasellus ullamcorper turpis ac nunc aliquam, at adipiscing dolor lobortis.",
        "Aliquam aliquam massa eu ullamcorper malesuada."
    ],

    bannedWords: ["orem","vestibu","usce","aliquam","donec","phasellus","tinci","mauris","lobortis","vitae"],

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
        modifiedMessages[loopCount] = [];

        // Remove swearing.
        for (var i = 0; i < this.messages.length; i++) {
            // Replace only if messages length modulated with i+1 = 0
            if (this.messages.length % (i+1) == 0)
            {
                counter++;
                for (var k = 0; k < this.bannedWords.length; k++) {
                    modifiedMessages[loopCount].push(this.messages[i].replace(this.bannedWords[k]));
                }
            }
        }

        if (isFinal)
        {
            var elapsed = benchmark.elapsedTime();
            var finalScore = counter / elapsed * 1000;
            //benchmark.submitResult(finalScore, guide, {elapsedTime: elapsed, operations: counter, ops: finalScore});
            print("string_chat: elapsedTime: " + elapsed + " operations: " + counter + " score: " + finalScore);
        }

    }
};