import os.path

ALLOWED_CODE_EXTENSIONS = {
    # General-purpose programming languages
    '.c', '.cpp', '.cmm', '.h', '.hpp', '.cc', '.cxx', '.hxx', '.java', '.scala',
    '.py', '.pyc', '.pyo', '.pyd', '.pyw', '.pyx', '.r', '.rb', '.php',
    '.pl', '.pm', '.tcl', '.sh', '.bash', '.zsh', '.fish', '.bat', '.cmd',
    '.ps1', '.awk', '.asm', '.csh', '.cs', '.css', '.html', '.htm', '.xml',
    '.json', '.yaml', '.yml', '.ini', '.cfg', '.conf', '.toml',

    # Assembly
    '.asm', '.s',

    # Batch files
    '.bat', '.cmd', '.ps1',

    # Crystal
    '.cr',

    # CUDA
    '.cu', '.cuh',

    # COBOL
    '.cob', '.cbl',

    # Clojure
    '.clj', '.cljs', '.cljc',

    # Configuration files
    '.ini', '.cfg', '.conf', '.toml', '.yaml', '.yml', '.properties',

    # Compiled files
    '.o', '.obj', '.exe', '.dll', '.class', '.jar', '.so', '.lib', '.a',

    # Database query languages
    '.sql', '.sqlite', '.db', '.dbf',

    # Dart
    '.dart',

    # Dockerfile
    'Dockerfile',

    # Elixir
    '.ex', '.exs',

    # Erlang
    '.erl',

    # Elm
    '.elm',

    # F#
    '.fs', '.fsx', '.fsi',

    # Fortran
    '.f', '.f90', '.f95', '.f03', '.f08',

    # Gradle
    '.gradle',

    # Groovy
    '.groovy',

    # GraphQL
    '.graphql',

    # Haxe
    '.hx',

    # Haskell
    '.hs', '.lhs',

    # J
    '.ijs',

    # Julia
    '.jl',

    # JSON
    '.json',

    # Jupyter Notebooks
    '.ipynb',

    # Kotlin
    '.kt', '.kts',

    # Lua
    '.lua',

    # Lisp
    '.lisp', '.cl', '.el',

    # Linden Scripting Language
    '.lsl',

    # Linker Scripts
    '.ld', '.lds',

    # LaTeX
    '.tex', '.bib',

    # MATLAB
    '.m',

    # MAKEFILE
    '.mk',

    # Markup languages
    '.xml', '.html', '.htm', '.rst', '.adoc', '.md',

    # Objective-C
    '.m', '.mm',

    # OCaml
    '.ml', '.mli',

    # OpenCL
    '.cl',

    # Pascal
    '.pas',

    # Perl
    '.pl', '.pm',

    # PowerShell
    '.ps1',

    # Prolog
    '.pl',

    # PureScript
    '.purs',

    # Puppet
    '.pp',

    # Racket
    '.rkt',

    # ReasonML
    '.re', '.rei',

    # Ruby
    '.rb',

    # Rust
    '.rs',

    # Scala
    '.scala',

    # Shell scripts
    '.sh', '.bash', '.zsh', '.fish', '.oil',

    # Scheme
    '.scm',

    # Swift
    '.swift',

    # TOML
    '.toml',

    # TypeScript
    '.ts', '.tsx',

    # Terraform
    '.tf', '.hcl',

    # Verilog
    '.v', '.sv',

    # Visual Basic
    '.vb',

    # VHDL
    '.vhd', '.vhdl',

    # Vue.js
    '.vue',

    # Web development
    '.js', '.ts', '.jsx', '.tsx', '.html', '.css', '.scss', '.less', '.php',

    # Zig
    '.zig',
}
CODE_FILENAMES = {"MAKEFILE"}
CODE_EXTENSIONS = {c.split(os.path.extsep)[-1].upper() for c in ALLOWED_CODE_EXTENSIONS}
