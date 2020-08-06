import plotly.express as px

PRIMARY_COLOR = "#34495e"
NUM_SPLITS = 5

COLOR_SCALES = px.colors.named_colorscales()

GOOGLE_ANALYTICS_SCRIPT = """
<script>
(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
})(window,document,'script','https://www.google-analytics.com/analytics.js','ga');

ga('create', 'UA-148444994-1', 'auto');
ga('send', 'pageview');
"""