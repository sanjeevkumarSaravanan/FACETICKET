<html lang="en">
  <head>
    <meta name="description" content="Vali is a responsive and free admin theme built with Bootstrap 4, SASS and PUG.js. It's fully customizable and modular.">
    <!-- Twitter meta-->
    <meta property="twitter:card" content="summary_large_image">
    <meta property="twitter:site" content="@pratikborsadiya">
    <meta property="twitter:creator" content="@pratikborsadiya">
    <!-- Open Graph Meta-->
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="Vali Admin">
    <meta property="og:title" content="Vali - Free Bootstrap 4 admin theme">
    <meta property="og:url" content="http://pratikborsadiya.in/blog/vali-admin">
    <meta property="og:image" content="http://pratikborsadiya.in/blog/vali-admin/hero-social.png">
    <meta property="og:description" content="Vali is a responsive and free admin theme built with Bootstrap 4, SASS and PUG.js. It's fully customizable and modular.">
    <title></title>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- Main CSS-->
    <link rel="stylesheet" type="text/css" href="../static/css/main.css">
    <!-- Font-icon css-->
    <link rel="stylesheet" type="text/css" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">


<script language="javascript">
function validate()
{
	
	if(document.form1.regno.value=="")
	{
	alert("Enter the Register No.");
	document.form1.regno.focus();
	return false;
	}
	if(document.form1.name.value=="")
	{
	alert("Enter the Name");
	document.form1.name.focus();
	return false;
	}
	if(document.form1.gender.selectedIndex==0)
	{
	alert("Select the Gender");
	document.form1.gender.focus();
	return false;
	}
	if(document.form1.dob.value=="")
	{
	alert("Enter the Date of Birth");
	document.form1.dob.focus();
	return false;
	}
	if(document.form1.mobile.value=="")
	{
	alert("Enter the Mobile No.");
	document.form1.mobile.focus();
	return false;
	}
	if(isNaN(document.form1.mobile.value))
	{
	alert("Invalid Mobile No.");
	document.form1.mobile.select();
	return false;
	}
	if(document.form1.mobile.value.length!=10)
	{
	alert("Mobile No. must be 10 digits!");
	document.form1.mobile.select();
	return false;
	}
	
	
	if(document.form1.email.value=="")
	{
	alert("Enter the Email");
	document.form1.email.focus();
	return false;
	}
	if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(document.form1.email.value))  
	{
	
	}
	else
	{
	alert("Invalid E-mail!");
	document.form1.email.select();
	return false;
	}
	
	if(document.form1.address.value=="")
	{
	alert("Enter the Address");
	document.form1.address.focus();
	return false;
	}
	
	if(document.form1.aadhar.value=="")
	{
	alert("Enter the Aadhar No.");
	document.form1.aadhar.focus();
	return false;
	}
	if(document.form1.dept.selectedIndex==0)
	{
	alert("Select the Department");
	document.form1.dept.focus();
	return false;
	}
	if(document.form1.year.value=="")
	{
	alert("Enter the Batch Year");
	document.form1.year.focus();
	return false;
	}
	
return true;
}
</script>


  </head>
  <body class="app sidebar-mini rtl">
    <!-- Navbar-->
    <header class="app-header"><a class="app-header__logo" href="">Admin</a>
      <!-- Sidebar toggle button--><a class="app-sidebar__toggle" href="#" data-toggle="sidebar" aria-label="Hide Sidebar"></a>
      <!-- Navbar Right Menu-->
      <ul class="app-nav">
        <li class="app-search">
         <!-- <input class="app-search__input" type="search" placeholder="Search">
          <button class="app-search__button"><i class="fa fa-search"></i></button>-->
        </li>
        <!--Notification Menu-->
        
        <!-- User Menu-->
     	<li class="dropdown"><a class="app-nav__item" href="#" data-toggle="dropdown" aria-label="Open Profile Menu"><i class="fa fa-user fa-lg"></i></a>
          <ul class="dropdown-menu settings-menu dropdown-menu-right">
            <li><a class="dropdown-item" href="/logout"><i class="fa fa-sign-out fa-lg"></i> Logout</a></li>
          </ul>
        </li>
      </ul>
    </header>
    <!-- Sidebar menu-->
    <div class="app-sidebar__overlay" data-toggle="sidebar"></div>
    <aside class="app-sidebar">
      <div class="app-sidebar__user">
        <div>
          <p class="app-sidebar__user-name">Menu</p>
          <p class="app-sidebar__user-designation"></p>
        </div>
      </div>
      <ul class="app-menu">
        	<li><a class="app-menu__item" href="/admin"><i class="app-menu__icon fa fa-dashboard"></i><span class="app-menu__label">Dashboard</span></a></li>
        <li class="treeview"><a class="app-menu__item" href="#" data-toggle="treeview"><i class="app-menu__icon fa fa-laptop"></i><span class="app-menu__label">UI Elements</span><i class="treeview-indicator fa fa-angle-right"></i></a>
          <ul class="treeview-menu">
            <li><a class="treeview-item" href="/add_dept"><i class="icon fa fa-circle-o"></i> Add Department</a></li>
            <li><a class="treeview-item" href="/add_staff"><i class="icon fa fa-circle-o"></i>Add Staff</a></li>
            <li><a class="treeview-item" href="/add_student"><i class="icon fa fa-circle-o"></i> Add Student</a></li>
            
          </ul>
        </li>
        <li><a class="app-menu__item" href="/view_staff"><i class="app-menu__icon fa fa-pie-chart"></i><span class="app-menu__label">Staff</span></a></li>

        <li class="treeview"><a class="app-menu__item" href="#" data-toggle="treeview"><i class="app-menu__icon fa fa-edit"></i><span class="app-menu__label">Exam</span><i class="treeview-indicator fa fa-angle-right"></i></a>
          <ul class="treeview-menu">
            <li><a class="treeview-item" href="/add_exam"><i class="icon fa fa-circle-o"></i> Add Exam Schedule</a></li>
            <li><a class="treeview-item" href="/add_hall"><i class="icon fa fa-circle-o"></i> Add Exam Hall</a></li>
           
          </ul>
        </li>
     
      </ul>
    </aside>
    <main class="app-content">
      <div class="app-title">
        <div>
          <h1><i class="fa fa-edit"></i> Add Students</h1>
          <p></p>
        </div>
        <ul class="app-breadcrumb breadcrumb">
          <li class="breadcrumb-item"><i class="fa fa-home fa-lg"></i></li>
        
          <li class="breadcrumb-item"><a href="/admin">Home</a></li>
        </ul>
      </div>
      <div class="row">
        <div class="col-md-12">
          <div class="tile">
            <div class="row">
              <div class="col-lg-6">
                <form name="form1" method="post">
					<h3>Staff Information</h3>
								{% if msg=="success" %}
				  <span style="color:#009933">Staff Information Added...</span>
				  <iframe src="http://iotcloud.co.in/testmail/testmail1.php?message={{mess}}&email={{email}}&subject=Staff Info" width="5" height="5" frameborder="0"></iframe>
				  <script>
//Using setTimeout to execute a function after 5 seconds.
setTimeout(function () {
   //Redirect with JavaScript
   window.location.href= '/view_staff';
}, 4000);
</script>

				  {% endif %}
				  {% if msg=="fail" %}
				  <span style="color:#FF0000">Already Exist!</span>
				  {% endif %}
                                    <form class="form-valide" action="" name="form1" method="post">
                                        <div class="form-group row">
                                            <label class="col-lg-4 col-form-label" for="val-username">Staff Type
                                            </label>
                                            <div class="col-lg-6">
                                                <select class="form-control" name="stype">
												<option>HOD</option>
												<option>Staff</option>
												</select>
                                            </div>
                                        </div>
										<div class="form-group row">
                                            <label class="col-lg-4 col-form-label" for="val-username">Name 
                                            </label>
                                            <div class="col-lg-6">
                                                <input type="text" class="form-control" name="name" placeholder="">
                                            </div>
                                        </div>
                                        
										<div class="form-group row">
                                            <label class="col-lg-4 col-form-label" for="val-username">Mobile No. 
                                            </label>
                                            <div class="col-lg-6">
                                                <input type="text" class="form-control" name="mobile" maxlength="10" placeholder="">
                                            </div>
                                        </div>
										<div class="form-group row">
                                            <label class="col-lg-4 col-form-label" for="val-username">Email 
                                            </label>
                                            <div class="col-lg-6">
                                                <input type="text" class="form-control" name="email" placeholder="">
                                            </div>
                                        </div>
										<div class="form-group row">
                                            <label class="col-lg-4 col-form-label" for="val-username">Location
                                            </label>
                                            <div class="col-lg-6">
                                                <input type="text" class="form-control" name="location" placeholder="">
                                            </div>
                                        </div>
									
										<div class="form-group row">
                                            <label class="col-lg-4 col-form-label" for="val-username">Department 
                                            </label>
                                            <div class="col-lg-6">
                                                <select class="form-control" name="dept">
												<option value="">-Department-</option>
												{% for ds in value1 %}
												<option>{{ds[1]}}</option>
												{% endfor %}
												</select>
                                            </div>
                                        </div>
										<div class="form-group row">
                                            <label class="col-lg-4 col-form-label" for="val-username">Staff ID 
                                            </label>
                                            <div class="col-lg-6">
                                                <input type="text" class="form-control" name="uname" placeholder="">
                                            </div>
                                        </div>
										<div class="form-group row">
                                            <label class="col-lg-4 col-form-label" for="val-username">Password 
                                            </label>
                                            <div class="col-lg-6">
                                                <input type="password" class="form-control" name="pass" placeholder="">
                                            </div>
                                        </div>
										
                                        <div class="form-group row">
                                            <div class="col-lg-8 ml-auto">
                                                <button type="submit" class="btn btn-primary" onClick="return validate()">Submit</button>
                                            </div>
                                        </div>
                                    </form>
              </div>
           
		   
            </div>
         
          </div>
        </div>
      </div>
    </main>
    <!-- Essential javascripts for application to work-->
    <script src="../static/js/jquery-3.2.1.min.js"></script>
    <script src="../static/js/popper.min.js"></script>
    <script src="../static/js/bootstrap.min.js"></script>
    <script src="../static/js/main.js"></script>
    <!-- The javascript plugin to display page loading on top-->
    <script src="../static/js/plugins/pace.min.js"></script>
    <!-- Page specific javascripts-->
    <!-- Google analytics script-->
    <script type="text/javascript">
      if(document.location.hostname == 'pratikborsadiya.in') {
      	(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
      	(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
      	m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
      	})(window,document,'script','//www.google-analytics.com/analytics.js','ga');
      	ga('create', 'UA-72504830-1', 'auto');
      	ga('send', 'pageview');
      }
    </script>
  </body>
</html>