const request = require("request")
const proc = require("process")

var altitude="47"
var latitude="-90"
var longitude="120"
var year="2018"

var twobyte = function(val){
	if(val<10){
		num = "0" + val.toString()
	} else {
		num = val.toString()
	}
	return num
}

request.get("http://cosmicrays.amentum.space/api/calculate_dose_rate?altitude="
    + altitude +"&latitude=" + latitude + "&longitude="+ longitude + "&year="
    + year + "&month=" + twobyte(proc.argv[3]) + "&day="+ twobyte(proc.argv[4]) + "&particle=" + proc.argv[2],
        
    function(error, response, body){
		const obj_body = JSON.parse(body) // json 轉 js object
        console.log(year+"-"+twobyte(proc.argv[3])+"-"+twobyte(proc.argv[4])+":", obj_body['dose rate'].value, obj_body['dose rate'].units)
        //console.log(response['headers'])
        }
)