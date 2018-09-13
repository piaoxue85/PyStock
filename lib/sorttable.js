<style>

i {
    border: solid black;
    border-width: 0 3px 3px 0;
    display: inline-block;
    padding: 3px;
}

.right {
    transform: rotate(-45deg);
    -webkit-transform: rotate(-45deg);
}

.left {
    transform: rotate(135deg);
    -webkit-transform: rotate(135deg);
}

.up {
    transform: rotate(-135deg);
    -webkit-transform: rotate(-135deg);
}

.down {
    transform: rotate(45deg);
    -webkit-transform: rotate(45deg);
}

table, th, td {
   border: 1px solid black;
}

</style>

<script>

/*14 Feb 2018 
For highlighting cell and text
*/

var sorted = 0;
var hbgcolor = "#003366"
var hfontcolor = "#FFFFFF"


var dbgcolor = ""
var dfontcolor = ""

function colorCol(t,c) {

	var table, rows;

	table = document.getElementById("tbl" + t);

	rows = table.getElementsByTagName("TR");

	for (i = 1; i < (rows.length); i++) 

	{

		x = rows[i].getElementsByTagName("TD")[c];

		if (x.bgColor == "")


		{

			x.bgColor= hbgcolor;

			x.style.color = hfontcolor

		}

		else
			
		{

			x.bgColor= dbgcolor;

			x.style.color = dfontcolor		

		}

	}

}

function sumCol(t,c) {
	var table, rows, tot;
	table = document.getElementById("tbl" + t);
	rows = table.getElementsByTagName("TR");
	
	tot = 0
	
	for (i = 1; i < (rows.length); i++) 
	{
		x = rows[i].getElementsByTagName("TD")[c];
		
		if (rows[i].bgColor == "" && x.bgColor == "")
		{
			tot = tot + 0;
		}
		else			
		{
			valx = x.innerHTML.toLowerCase();
			valx = Number(valx);
			tot = tot + valx;
		}
	}
	
	alert("Total " + tot);
}

function hideCol(t,c) {
	var table, rows, tot;
	table = document.getElementById("tbl" + t);
	rows = table.getElementsByTagName("TR");
	
	x = rows[0].getElementsByTagName("TH")[c];
	
	x.style.display = "none";
	
	for (i = 1; i < (rows.length); i++) 
	{
		x = rows[i].getElementsByTagName("TD")[c];
		
		x.style.display = "none";
	}
	

}

function color(row) {
        if (row.bgColor == ""){
            row.bgColor= hbgcolor;
			row.style.color = hfontcolor
        }
        else{
			row.bgColor= dbgcolor;
			row.style.color = dfontcolor		
        }
}



function sortTable(t,c) {

  var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;

  table = document.getElementById("tbl" + t);

  switching = true;

  // Set the sorting direction to ascending:

  dir = "asc"; 
  
  if(sorted != c)
  {
      rows = table.getElementsByTagName("TR");
	  
	  for (i = 1; i < (rows.length); i++) 
	  {
		      x = rows[i].getElementsByTagName("TD")[sorted];

	  }
  }
  
  sorted = c

  /* Make a loop that will continue until

  no switching has been done: */

  while (switching) {

    // Start by saying: no switching is done:

    switching = false;

    rows = table.getElementsByTagName("TR");

    /* Loop through all table rows (except the

    first, which contains table headers): */

    for (i = 1; i < (rows.length - 1); i++) {

      // Start by saying there should be no switching:

      shouldSwitch = false;

      /* Get the two elements you want to compare,

      one from current row and one from the next: */

      x = rows[i].getElementsByTagName("TD")[c];

      y = rows[i + 1].getElementsByTagName("TD")[c];

      /* Check if the two rows should switch place,

      based on the direction, asc or desc: */
	  
	  valx = x.innerHTML.toLowerCase()
	  valy = y.innerHTML.toLowerCase()

	  if (isNaN(valx) == false)
	  {
			valx = Number(valx)
	  }

	  if (isNaN(valy) == false)
	  {
			valy = Number(valy)
	  }	  

      if (dir == "asc") {
        if (valx > valy) {
          // If so, mark as a switch and break the loop:
          shouldSwitch= true;
          break;
        }
      } else if (dir == "desc") {

        if (valx < valy) {
          // If so, mark as a switch and break the loop:
          shouldSwitch= true;
          break;
        }

      }

    }

    if (shouldSwitch) {

      /* If a switch has been marked, make the switch

      and mark that a switch has been done: */

      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);

      switching = true;

      // Each time a switch is done, increase this count by 1:

      switchcount ++; 

    } else {

      /* If no switching has been done AND the direction is "asc",

      set the direction to "desc" and run the while loop again. */

      if (switchcount == 0 && dir == "asc") {

        dir = "desc";

        switching = true;

      }

    }

  }

}

</script>