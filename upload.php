<?php
require('vendor/autoload.php');
// this will simply read AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY from env vars
$s3 = Aws\S3\S3Client::factory(array(
			'signature' => 'v4',
			'version' => 'latest',
			'region'  => 'us-east-2'));

$bucket = getenv('S3_BUCKET')?: die('No "S3_BUCKET" config var in found in env!'); //S3_BUCKET --> BUCKET
echo isset($_FILES['userfile']);
echo $_FILES['userfile']['error'] == UPLOAD_ERR_OK;
echo is_uploaded_file($_FILES['userfile']['tmp_name']);

if($_SERVER['REQUEST_METHOD'] == 'POST' && isset($_FILES['userfile']) && $_FILES['userfile']['error'] == UPLOAD_ERR_OK && is_uploaded_file($_FILES['userfile']['tmp_name'])) {
    // FIXME: add more validation, e.g. using ext/fileinfo
    try {
        echo "Uploading..";
        $upload = $s3->upload($bucket, $_FILES['userfile']['name'], fopen($_FILES['userfile']['tmp_name'], 'rb'), 'public-read');
        echo "Upload successful!";
        //echo $upload->get('ObjectURL')
?>
        <p>Upload <a href="<?=htmlspecialchars($upload->get('ObjectURL'))?>">successful</a> :)</p>
<?php } catch(Exception $e) {
         echo "Upload error!";?>
        <p>Upload error :(</p>
<?php } }

?>