from ProjectReader import ProjectReader

pr = ProjectReader("src")
print(pr.files)
with open("project_schema.json","w") as f:
    f.write(pr.read_declarations())