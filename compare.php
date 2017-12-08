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
        echo "Image received:  " . $file_name." ";

	$file = $_FILES['userfile'];
	
        $website = "https://s3.us-east-2.amazonaws.com/access-lh18-bucket/";

	//$upload = $s3->upload($bucket, $_FILES['userfile']['name'], fopen($_FILES['userfile']['tmp_name'], 'rb'), 'public-read');
	
	$full_name = $website.$file_name;
        $objects = $s3->getIterator('ListObjects', array(
            'Bucket' => $bucket
        ));

	$string = "";	

        foreach ($objects as $object) {
		$string = $string.$object['Key']." ";
	}
	
	$result = shell_exec("python test.py " . escapeshellarg($string));
	if (empty($result)) {
		$testing = '$result is either 0, empty, or not set at all';
		echo $testing."<br>";
	}
	else{
	 echo $result."<br>";
	}

	//	echo "Images in server: ";
	//	print_r(array_values($arr));

	//	echo "Testing Python program";

	//	$content = "name_from_python";
		//$result = shell_exec('python process_img.py ' . escapeshellarg($content)." ".escapeshellarg($file);

 } catch(Exception $e) {
         echo "Error detected";

 } }
 else {
    echo "Error detected: Either no a POST request, POST req. didn't have file passed as 'userfile', there was an error uploading it (S_FILES['userfile']['error']), or the file is uploaded already";
 }

?>
