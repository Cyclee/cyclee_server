<%inherit file="base.mako"/>

<%block name="header">
    <link 
       rel="stylesheet" 
       href="${request.static_url('cyclee_server:static/css/jquery.mobile-1.1.1.min.css')}" />

    <script 
       data-main="${request.static_url('cyclee_server:static/js/main.js')}"
       src="${request.static_url('cyclee_server:static/js/libs/require-jquery.js')}">
    </script>
</%block>



<div id="application" data-role="page">

  <div data-role="header">
    <h1>Cyclee Dashboard</h1>
  </div>
  
  <div data-role="content">	
    
  </div>

</div>
