<%inherit file="base.mako"/>

<%block name="header">
    <script 
       data-main="${request.static_url('cyclee_server:static/js/main.js')}"
       src="${request.static_url('cyclee_server:static/js/require-jquery.js')}">
    </script>
</%block>

<div id="application">
</div>
