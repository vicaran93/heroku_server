<?php
require('vendor/autoload.php');
// this will simply read AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY from env vars
$s3 = Aws\S3\S3Client::factory(array(
			'signature' => 'v4',
			'version' => 'latest',
			'region'  => 'us-east-2'));

$bucket = getenv('S3_BUCKET')?: die('No "S3_BUCKET" config var in found in env! We cannot access  server database!'); //S3_BUCKET --> BUCKET in local server

if($_SERVER['REQUEST_METHOD'] == 'POST' && isset($_FILES['userfile']) && $_FILES['userfile']['error'] == UPLOAD_ERR_OK && is_uploaded_file($_FILES['userfile']['tmp_name'])) {
    try {
        // get filename
        $file_name = $_FILES['userfile']['name'];
        echo "Image received:  " . $file_name."\n" ;

	$result = shell_exec("python main_for_tm.py " . escapeshellarg($file_name));
	if (empty($result)) {
		$testing = '$result is either 0, empty, or not set at all';
		echo $testing."<br>";
	}
	else{
	 echo $result;
	}

 } catch(Exception $e) {
         echo "Error detected";

 } }
 else {
    echo "Error detected: Either no a POST request, POST req. didn't have file passed as 'userfile', there was an error uploading it (S_FILES['userfile']['error']), or the file is uploaded already";
 }

?>
