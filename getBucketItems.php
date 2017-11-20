<?php

// Include the AWS SDK using the Composer autoloader.
require 'vendor/autoload.php';
// this will simply read AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY from env vars
$s3 = Aws\S3\S3Client::factory(array(
			'signature' => 'v4',
			'version' => 'latest',
			'region'  => 'us-east-2'));

$bucket = getenv('BUCKET')?: die('No "BUCKET" config var in found in env!'); //S3_BUCKET --> BUCKET

// Use the high-level iterators (returns ALL of your objects).
try {
    $objects = $s3->getIterator('ListObjects', array(
        'Bucket' => $bucket
    ));

    echo "Keys retrieved!\n";
    foreach ($objects as $object) {
        echo $object['Key'] . "\n";
        // Display the object in the browser
        //header("Content-Type: {$object['ContentType']}");
        //echo $object['Body'];
    }
} catch (S3Exception $e) {
    echo $e->getMessage() . "\n";
}