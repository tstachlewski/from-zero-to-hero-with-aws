<!DOCTYPE html>
<html lang="en">

    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
        <title>Simple PHP App</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="assets/css/bootstrap.min.css" rel="stylesheet">
        <style>body {margin-top: 40px; background-color: #333;}</style>
        <link href="assets/css/bootstrap-responsive.min.css" rel="stylesheet">
        <!--[if lt IE 9]><script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script><![endif]-->
    </head>

    <body>
        <div class="container">
            <div class="hero-unit">


                <img src="assets/images/unicorn.jpg" valign="center">

                <h1>This is my docker! Yeah!</h1>
                

                <?php

                  $hostname = getenv('HOSTNAME');
                  if (isset($hostname)) {
                      $color = hexdec( substr(sha1($hostname), 0, 10));
                      $color = substr($color, 0, 6);
                  }
                  
                  $metadata_uri = getenv('ECS_CONTAINER_METADATA_URI');
                  if (isset($user_id)) {
                      $metadata = file_get_contents($metadata_uri . '/task');
                      $obj = json_decode($metadata);
                      $taskARN = $obj->{'TaskARN'};
                      $color = substr($taskARN,-10,6);
                  }
                  
                ?>

            </div>
        </div>

        <script src="assets/js/bootstrap.min.js"></script>
        
        <?php echo '<script type="text/javascript">document.body.style.background = "#' . $color . '" </script>';  ?>
        
    </body>

</html>
