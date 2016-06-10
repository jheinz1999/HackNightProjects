function isSeniorCenterOpen() {

	/* variables for time */

	var time = new Date();

	var day = time.getDay();
	var hour = time.getHours();
	var minute = time.getMinutes();

	/* flag to keep track of whether it's open or not */

	var open;

	if (day == 0 || day == 6) // Senior center is closed Sat/Sun
		open = 0;

	else if (hour >= 8) { // Opens at 830

		if (hour == 8 && minute < 30) // if it's past 8 but before 830, it's closed.
			open = 0;

		else {

			if (day >= 1 && day <= 3) { // Mon-Wed

				if (hour <= 21) // Closes at 9
					open = 1;

				else
					open = 0;

			}

			else if (day == 4 || day == 5) { // Thurs/fri

				if (hour <= 17) // Closes at 5
					open = 1;

				else
					open = 0;

			}

		}

	}

	else
		open = 0;

	if (open == 1) // Senior center is open
		document.getElementById("response").innerHTML = "Yes.";

	else
		document.getElementById("response").innerHTML = "Nope.";

}
