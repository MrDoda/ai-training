import os

def update_html_report(card_html, interactive_graph_data=None, html_file="coloring.html"):
    interactive_section = ""
    if interactive_graph_data:
        interactive_section = f'''
  <div id="cy" style="width:600px; height:400px; margin-top:20px;"></div>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/cytoscape/3.21.1/cytoscape.min.js"></script>
  <script>
    var cy = cytoscape({{
      container: document.getElementById('cy'),
      elements: {interactive_graph_data},
      style: [
        {{
          selector: 'node',
          style: {{
            'background-color': 'data(color)',
            'label': 'data(label)',
            'text-valign': 'center',
            'color': '#fff'
          }}
        }},
        {{
          selector: 'edge',
          style: {{
            'width': 1,
            'line-color': '#ccc'
          }}
        }}
      ],
      layout: {{
        name: 'cose'
      }}
    }});
  </script>
        '''
    if os.path.exists(html_file):
        with open(html_file, "r", encoding="utf-8") as f:
            content = f.read()
        if "</body>" in content:
            content = content.replace("</body>", f"{card_html}\n{interactive_section}\n</body>")
        else:
            content += card_html + interactive_section
    else:
        content = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Graph Coloring Homework - Daniel Král</title>
  <style>
    body {{
      font-family: Arial, sans-serif;
      margin: 20px;
      background-color: #f5f5f5;
    }}
    .card {{
      border: 2px solid #008CBA;
      border-radius: 8px;
      padding: 16px;
      margin-bottom: 20px;
      box-shadow: 2px 2px 12px rgba(0, 140, 186, 0.2);
      background-color: #e0f7fa;
    }}
    .card.failure {{
      border-color: #e53935;
      background-color: #ffebee;
    }}
    h1 {{
      color: #0077b6;
    }}
    .card h2 {{
      margin-top: 0;
    }}
    @media print {{
      body {{
        background: none;
      }}
    }}
  </style>
</head>
<body>
  <h1>Graph Coloring Homework - Daniel Král</h1>
  {card_html}
  {interactive_section}
</body>
</html>
"""
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"HTML report updated: {html_file}")
