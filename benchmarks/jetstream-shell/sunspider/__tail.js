var __time_after = JetStream.goodTime();
__data.sum += Math.max(__time_after - __time_before, 1);
__data.n++;
if (__data.n == 20)
{
    // Clean contex after sunspider/tagcloud, 
    // otherwise it will conflict with octane2/typescript 
    if (Object.prototype.toJSONString) {
        delete Array.prototype.toJSONString;
        delete Boolean.prototype.toJSONString;
        delete Date.prototype.toJSONString;
        delete Number.prototype.toJSONString;
        delete Object.prototype.toJSONString;
        delete String.prototype.parseJSON;
        delete String.prototype.toJSONString;
    }
    JetStream.reportResult(__data.sum / __data.n);
}
else
    JetStream.accumulate(__data);