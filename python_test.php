
<html>
    <head><meta charset="UTF-8"></head>
    <body>
        <h1>Execuiting python script example</h1>
        <?php
		//$pyscript = 'C:/xampp/htdocs/server/process_img.py';
		//$python = 'C:/Python34/python.exe';
		//$tmp = shell_exec("$python $pyscript 'name'");
		//not working

		echo is_callable('shell_exec');
        content = "name_from_python";
		$result = shell_exec('python process_img.py ' . escapeshellarg($content));
        if (empty($result)) {
            echo '$result is either 0, empty, or not set at all';
        }
        else{
            echo $result;
        }
		?>

    </body>
</html>