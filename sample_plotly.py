import plotly.express as px

fig =px.scatter(x=range(10), y=range(10))
fig.write_html("/var/www/tmp/git_repo/chart_analytics/charts/sample/path/to/file.html")