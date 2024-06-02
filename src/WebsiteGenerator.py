import json

schema = json.load(open("project_schema.json","r"))
for file in schema:
    with open("website/"+str(file).replace("\\",".")+".html","w") as htmlf:
        final_html = ""
        for item in schema[file]:
            print(item)
            html = f"<h1>{item['name']}</h1><p>{item['docstring']}</p>"
            for a in item['args']:
                html+=f"<p>{a['name']} : {a['type_annotation']}</p>"
            final_html+=html
        htmlf.write(final_html)