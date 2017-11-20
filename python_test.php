
<html>
    <head><meta charset="UTF-8"></head>
    <body>
        <h1>Execuiting python script example</h1>
        <?php
		$pyscript = 'C:/xampp/htdocs/server/process_img.py';
		$python = 'C:/Python34/python.exe';
		$tmp = shell_exec("$python $pyscript 'name'");
		echo $tmp;
		//not working
		?>

    </body>
</html>