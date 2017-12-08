<?php
require('vendor/autoload.php');
// this will simply read AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY from env vars
$s3 = Aws\S3\S3Client::factory(array(
			'signature' => 'v4',
			'version' => 'latest',
			'region'  => 'us-east-2'));

$bucket = getenv('S3_BUCKET')?: die('No "S3_BUCKET" config var in found in env!'); //S3_BUCKET --> BUCKET

if($_SERVER['REQUEST_METHOD'] == 'POST' && isset($_POST['test_var']) ) {
    try {
        //echo "Uploading..";
        $test = $_POST['test_var'];
        echo "success: ".$test;
        $objects = $s3->getIterator('ListObjects', array(
            'Bucket' => $bucket
        ));

        foreach ($objects as $object) {
            //echo $object['Key'] . "\n";
            arr[] = $object['Key'];
        }

        print_r(array_values($arr));
        echo " S3"; // "success S3

 } catch(Exception $e) {
         echo "Upload error";
        //<p>Upload error :(</p>

 } }

?>