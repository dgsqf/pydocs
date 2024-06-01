import glob
import ast
import json
class ProjectReader:
    def __init__(self,folder : str) -> None:
        self.folder = folder
        self.files = glob.glob(f"{folder}/**/**.py",recursive=True)
        pass
    def read_declarations(self):
        decl = {}
        for fn in self.files:
            with open(fn,"r") as f:
                decl[f.name]=[]
                for n in ast.parse(f.read(),type_comments=True).body:
                    if type(n)==ast.FunctionDef or type(n)==ast.AsyncFunctionDef:
                        args=[]
                        for a in n.args.args:
                            if a.annotation == None:
                                args.append({
                                         "name": a.arg,
                                         "type_annotation": None})
                            else:
                                args.append({
                                         "name": a.arg,
                                         "type_annotation": a.annotation.id})
                        if type(n.returns)==ast.Constant:
                          decl[f.name].append({
                            "name": f.name+"."+n.name,
                            "args": args,
                            "return_type_annotation": None
                        })  
                        else:
                            decl[f.name].append({
                            "name": f.name+"."+n.name,
                            "args": args,
                            "return_type_annotation": n.returns.id
                        })
                    if type(n)==ast.ClassDef:
                        
                        args=[]
                        init_function=None
                        functions = []
                        functions_decl = []
                        for fu in n.body:
                            if type(fu)==ast.FunctionDef:
                                
                                if fu.name=="__init__":
                                    init_function=fu
                                else:
                                    functions.append(fu)
                        for a in init_function.args.args:
                            if a.arg=='self':
                                continue
                            if a.annotation == None:
                                args.append({
                                         "name": a.arg,
                                         "type_annotation": None})
                            else:
                                args.append({
                                         "name": a.arg,
                                         "type_annotation": a.annotation.id})
                       
                        for fun in functions:
                            args=[]
                            for a in fun.args.args:
                                if a.annotation == None:
                                    args.append({
                                         "name": a.arg,
                                         "type_annotation": None})
                                else:
                                    args.append({
                                         "name": a.arg,
                                         "type_annotation": a.annotation.id})
                            if type(fun.returns)==ast.Constant:
                                functions_decl.append({
                            "name": f.name+"."+fun.name,
                            "args": args,
                            "return_type_annotation": None
                                })  
                            else:
                                functions_decl.append({
                            "name": f.name+"."+fun.name,
                            "args": args,
                            "return_type_annotation": fun.returns.id
                        })
                        
                        decl[f.name].append({
                            "name": f.name+"."+n.name,
                            "args": args,
                            "functions": functions_decl})
        return(json.dumps(decl))