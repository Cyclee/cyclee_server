<%inherit file="base.mako"/>


<h2>Please log into the site</h2>

%if errors:
<p>${errors}</p>
%endif

%if form.errors:
<p>${form.errors}</p>
%endif

<form action="${request.route_url('login')}" method="POST">
%for field in form:
${field}
%endfor

<input class="btn" type="submit" name="submit" value="Log in" />
</form>