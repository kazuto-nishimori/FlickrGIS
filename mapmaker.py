"""
Code written by Nathan Wies and Kazuto Nishimori
1/11/20
"""

import folium


m = folium.Map([43,-100], zoom_start=4)
m.save('index.html')

def addMarkers(filename, newfilename):
    oFile = open(filename, 'r') 
    lines = oFile.read()
    oFile.close()
    start = "<body>"
    end = "</body>"
    mapid = ((lines.split(start))[1].split(end)[0]).split('id="')[1].split('" ></div>')[0]
    body = """
    <body>
                <header class = "container">
                    <h1>Flickr GIS Project</h1>
                    <h2>By Nathan Wies and Kazuto Nishimori</h2>
                    <form id="frm1">
                      Radius: <input type="text" name="rad" id="radius" value="1">
                      Number of Pictures: <input type="text" name="pics" id="picture" value="10">
                      <button type="button" onclick="myFunction();">Change</button>
                    </form>
                    <br>
                   
                </header>
                <div class="folium-map" style="width: 80.0%; height: 80.0%; left: 10.0%; top: 10px; bottom: 200px;" id='""" + mapid + """'></div>
                <footer class = "container">
                    <h3>Contact: nwies@u.rochester.edu</h3>
                </footer>
    </body>
    """
    lines = lines.split(start)[0] + body + lines.split(end)[1]


    custom_map = """
<script>
            var lat, lon; 
            var apiurl, picurl, address;
            var rad = parseFloat(1);
            var num = parseFloat(10);
            var count = 0;
            function myFunction() {
              var x = document.getElementById("frm1");
              rad = parseFloat(x.elements[0].value);
              num = parseFloat(x.elements[1].value);
              window.alert("New Markers will now have specified radius of "+rad.toString(10)+" km and will show " +num.toString(10)+ " pictures")
            }
            var arr = ['<div class = "popup">']
            """+ mapid +""".on("click", function(e){
                
                function getAddress(other){
                $.get('https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat='+ e.latlng.lat.toString(10) +'&lon='+e.latlng.lng.toString(10), function(data){
                    address = data.address;
                });
                other(makeMarker);
                }
                
                function doJson(other){
                $.getJSON("https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=ca370d51a054836007519a00ff4ce59e&per_page="+num.toString(10)+"&format=json&nojsoncallback=1&privacy_filter=1& accuracy=16&lat="+e.latlng.lat.toString(10)+"&lon="+e.latlng.lng.toString(10)+"&radius="+rad.toString(10),function(json){
                    if(parseInt(json.photos.total)>0){
                    arr.push("<h3>Total Pictures Found: "+json.photos.total.toString(10)+" at a radius of "+ rad.toString(10) +" km</h3><p><h5>Nearest Address</h5>Road: " + address.road + "<br>City: "+address.city+"<br> Postcode: "+ address.postcode + "<br> Country: " + address.country +"</p><p><h5>Coordinates</h5>Latitude: " + e.latlng.lat.toString(10) + "<br>Longitude: " + e.latlng.lng.toString(10) + "</p><p>Displaying Maximum of " +num.toString(10)+ " pictures</p>");
                    $.each(json.photos.photo,function(i,result){
                    picurl = "https://farm"+result.farm +".staticflickr.com/"+result.server +"/"+result.id+"_"+ result.secret+".jpg";
                    arr.push('<img src="'+picurl+'"/><br>'+result.title+'<br><br>');
                    count = count+1;
                    })
                    }
                    else{
                        arr.push('<p>No Images Found</p>')
                    }
                    other();
                })}
                function makeMarker(){
                arr.push("<div>")
                var mymarker = L.marker(
                    [e.latlng.lat, e.latlng.lng],
                    {}
                ).addTo(""" + mapid + """);
                var allpics = arr.toString();
                allpics = allpics.replace(/,/g, "");
                mymarker.bindPopup(allpics);
                picurl = ""
                arr = ['<div class = "popup">']
                }
                getAddress(doJson);
            })
</script>

<style>
    .popup {
    
       height: 300px;
       width: 300px;
       overflow: auto;
    }
    
    img {
    
      width: 250px;
      height: 250px;
      object-fit: cover;
    }
    
    .container{

        max-width: 960px;
        width: 80%;
        left: 10%;
        margin: auto;
    }
    p {
    
    width: 250px;
    }
</style>
    """


    lines = lines + custom_map


    f= open(newfilename,"w+")
    f.write(lines)
    f.close()

addMarkers("index.html","index.html")
