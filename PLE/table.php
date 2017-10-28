<html>
<head>
  <meta http-equiv="content-type" content="text/html" charset="utf-8"></meta>
  <script src="sorttable.js" type="text/javascript"></script>
  <link rel="stylesheet" type="text/css" href="table.css">
</head>
<div class="container">
  <div class="left">
  <img class="resize" src="wildflare_ubi.png" alt="wildflare">
  <p> WILDFLARE </p>
  </div>
  <div class="right">
  <input type="text" id="myInput" onkeyup="myFunction()" placeholder="Search...">
  </div>
</div>
  <table id="table1" class="sortable responstable">
    <tr>
      <th>Situation</th>
      <th><span>District</span></th>
      <th>Poster Name</th>
      <th>Publication</th>
      <th>Media</th>
      <th>Date</th>
    </tr>
    
     <?php
      $con=mysqli_connect("localhost","root","","wildfire");
      // Check connection
      if (mysqli_connect_errno()){
        echo "Failed to connect to MySQL: " . mysqli_connect_error();
      }

      $result = mysqli_query($con,"SELECT * FROM wildfire");

      while($row = mysqli_fetch_array($result))
      {
        echo "<tr>";
        echo "<td>" . $row['situation'] . "</td>";
        echo "<td>" . $row['district'] . "</td>";
        echo "<td><a href='". $row['user_url'] . "'>". $row['poster'] . "</a></td>";
        echo "<td><a id='publink' href='". $row['publication_url']."'>" .$row['publication']."</a></td>";
        echo "<td><a href='".$row['media'] ."'>". $row['media'] . "</a></td>";
        echo "<td>" . $row['date'] . "</td>";
        echo "</tr>";
      }
      echo "</table>";

      mysqli_close($con);
  ?>

  </table>
  <script>
function myFunction() {
  // Declare variables 
  var input, filter, table, tr, td, i;
  input = document.getElementById("myInput");
  filter = input.value.toUpperCase();
  table = document.getElementById("table1");
  tr = table.getElementsByTagName("tr");

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[0];
    td1 = tr[i].getElementsByTagName("td")[1];
    td2 = tr[i].getElementsByTagName("td")[2];
    td3 = tr[i].getElementsByTagName("td")[3];
    td4 = tr[i].getElementsByTagName("td")[4];
    td5 = tr[i].getElementsByTagName("td")[5];
    if (td &&td1 && td2 && td3 && td4 && td5) {
      if (td.innerHTML.toUpperCase().indexOf(filter) > -1 || td1.innerHTML.toUpperCase().indexOf(filter) > -1 || td2.innerHTML.toUpperCase().indexOf(filter) > -1 || td3.innerHTML.toUpperCase().indexOf(filter) > -1 || td4.innerHTML.toUpperCase().indexOf(filter) > -1 || td5.innerHTML.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    } 
  }
}
</script>
</html>
