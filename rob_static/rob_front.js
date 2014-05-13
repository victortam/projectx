$(document).ready(function() {

var d = new Date();
var today = d.getFullYear() + "/" + (d.getMonth()+1) + "/" + d.getDate();
var yesterday = d.getFullYear() + "/" + (d.getMonth()+1) + "/" + (d.getDate() - 1);

$("#title").html("Difference in Subscribers Between " + today + " & " + yesterday);





window.onresize = function(event) {
   
    $(".demo-container").css({"width":"50%","height":"50%"});
    $("#placeholder").css({"width":"50%","height":"50%"});
    $("#content").css({"width":"100%","height":"100%"});
    

}

            var bid_count = 0;
            $("#bidform").submit(function() {

                $.post('/bid', {a_name: $("#name").val()}, function(data) {

                    //get time
                    var dt = new Date();
                    var time = dt.getHours() + ":" + dt.getMinutes() + " " + dt.getSeconds() + "s";

                    //username and vote
                    user = data['username'];
                    vote = data['uservote'];

                    //append to table
                    bid_count = bid_count + 1;
                    $("#res").append("<tr id=\"" + bid_count + "\"</tr>");
                    $("#" + bid_count).append("<td>" + user + "<td><td>" + vote + "<td><td>" + time + "</td>");





                    //check if exists

                    //$("#" + data['username']).append("<td>" + data['username'] + "<td>")
                    //$("#" + data['username']).append("<td>" + data['uservote'] + "<td>")


                    //append raw data
                    $( "body" ).append( data['raw'] + "</br>");


                });
                return false ;
            });




get_fb()

function get_fb(){

$.ajax({
    
        type: "POST",
        url: '/histogram',
        success:function(data) {

            var d3 = data['title'];
            var x = data['xaxis'];

            $.plot("#placeholder", [d3], {grid: {
                markings: [
                    {yaxis: { from: 0, to:2100 },color: "#C1E6D9"},
                    {yaxis: { from: -200, to: 0},color: "#FAB3B1"}
                ]},
                
                colors:["#35373b"],
                
                
                xaxis: {
                    ticks:x
                }
                
            }); 
            
            

            
            
            
            
            setTimeout(function(){get_fb();}, 60000);

        }

    });

}










 
});  