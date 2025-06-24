from dateutil.parser import isoparse

def generate_html(active_rooms, now):
    html_rows = "\n".join([
        f"<tr><td>{r['title']}</td><td>{r['type']}</td><td>{r['lastActivity']}</td><td>{int((now - isoparse(r['lastActivity'])).total_seconds() // (24 * 3600))}</td></tr>"
        for r in active_rooms
    ])
    html_page = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Webex Recent Rooms</title>
    <meta charset='utf-8'>
    <link rel='stylesheet' type='text/css' href='https://cdn.datatables.net/1.13.6/css/jquery.dataTables.min.css'/>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
        tr:nth-child(even) {{ background-color: #f9f9f9; }}
        .dt-search {{ margin-bottom: 10px; }}
        .dataTables_filter {{ margin-bottom: 20px; }}
    </style>
</head>
<body>
    <h2>Webex Recent Rooms (Last 7 Days)</h2>
    <table id='webexRooms'>
        <thead>
            <tr><th>Title</th><th>Type</th><th>Last Activity</th><th>Days Since Last Activity</th></tr>
        </thead>
        <tbody>
            {html_rows}
        </tbody>
    </table>
    <script src='https://code.jquery.com/jquery-3.7.0.min.js'></script>
    <script src='https://cdn.datatables.net/1.13.6/js/jquery.dataTables.min.js'></script>
    <script>
    $(document).ready(function() {{
        $('#webexRooms').DataTable({{
            pageLength: 100,
            searching: true,
            info: true
        }});
    }});
    </script>
</body>
</html>
"""
    return html_page
