def generate_card_html(timestamp, params, results, image_filename):
    card_class = "card" if results.get("status", False) else "card failure"
    card_html = f"""
  <div class="{card_class}">
    <h2>Run at {timestamp}</h2>
    <p><strong>Parameters:</strong></p>
    <ul>
      <li>Colors attempted: {params.get("colors")}</li>
      <li>Steps allowed: {params.get("steps")}</li>
      <li>Random walk probability: {params.get("random")}</li>
      <li>Min hill climbing streak: {params.get("min_hill_climb")}</li>
    </ul>
    <p><strong>Results:</strong></p>
    <ul>
      <li>Elapsed time: {results.get("elapsed_time"):.2f} seconds</li>
      <li>Final conflicts: {results.get("final_conflicts")}</li>
      <li>Status: {"Valid coloring" if results.get("status") else "Invalid coloring"}</li>
    </ul>
    <img src="{image_filename}" style="max-width:400px; display:block; margin-top:10px;">
  </div>
    """
    return card_html
