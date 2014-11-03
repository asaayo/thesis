<?php
//contains DB connection stuff
require "phplib/db.php";
//required for twilio (SMS service) to function
require "twilio-php-master/Services/Twilio.php";
//account information for twilio
$AccountSid = "AC169d5a950282cc349f94af7987f21c67";
$AuthToken = "61e010b9fb2fcd0b6b4acd5faf9b0dd2";
$client = new Services_Twilio($AccountSid, $AuthToken);
//used for debugging, appends to the web page 
var_dump($_POST);
//restaurant name
$name = $_POST['name'];
//restaurant phone number, not used currently
//usable to create unique table in the database for
//managing different restaurants
$no = $_POST['number'];
//google maps identifier for the restaurant
$id = $_POST['identifier'];
//user's phone number, used to send text message
$userno = $_POST['user'];
//"MY" phone number
$twiliono = "484-240-4354";
//creates the actual sms request and sends it off 
$sms = $client->account->messages->sendMessage($twiliono, $userno, "Reservation request for $name, confirm? (reply with C or c)");
//make sure they're not already in the table
$mysqli->query("DELETE * FROM temp t WHERE t.username=$userno");
//inserts info into temp table awaiting confirmation
$time = date('H:i:s');
$mysqli->query("INSERT INTO temp (username)VALUES ($userno)");
$mysqli->close();
?>
