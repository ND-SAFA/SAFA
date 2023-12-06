ALLOWED_CODE_EXTENSIONS = [".c", ".cc", ".h", ".cpp", ".hpp", ".cs", ".xaml", ".csproj",
                           ".py", ".java", ".swift", ".vb", ".sh", ".go", ".php", ".asm",
                           ".rb", ".sql",
                           ".js", ".ts", ".html", "htm", ".jsx", ".tsx", ".css", ".scss", ".vue"]
CODE_EXTENSIONS = [c[1:].upper() for c in ALLOWED_CODE_EXTENSIONS]
