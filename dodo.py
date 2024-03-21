"""
Run or update the project. This file uses the `doit` Python package. It works
like a Makefile, but is Python-based
"""

import sys
import os
sys.path.insert(1, "./src/")


import config
from pathlib import Path
from doit.tools import run_once
import platform

OUTPUT_DIR = Path(config.OUTPUT_DIR)
DATA_DIR = Path(config.DATA_DIR)

# fmt: off
## Helper functions for automatic execution of Jupyter notebooks
def jupyter_execute_notebook(notebook):
    return f"jupyter nbconvert --execute --to notebook --ClearMetadataPreprocessor.enabled=True --inplace ./src/{notebook}.ipynb"
def jupyter_to_html(notebook, output_dir=OUTPUT_DIR):
    return f"jupyter nbconvert --to html --output-dir={output_dir} ./src/{notebook}.ipynb"
def jupyter_to_md(notebook, output_dir=OUTPUT_DIR):
    """Requires jupytext"""
    return f"jupytext --to markdown --output-dir={output_dir} ./src/{notebook}.ipynb"
def jupyter_to_python(notebook, build_dir):
    """Convert a notebook to a python script"""
    return f"jupyter nbconvert --to python ./src/{notebook}.ipynb --output _{notebook}.py --output-dir {build_dir}"
def jupyter_clear_output(notebook):
    return f"jupyter nbconvert --ClearOutputPreprocessor.enabled=True --ClearMetadataPreprocessor.enabled=True --inplace ./src/{notebook}.ipynb"
# fmt: on


def get_os():
    os_name = platform.system()
    if os_name == "Windows":
        return "windows"
    elif os_name == "Darwin":
        return "nix"
    elif os_name == "Linux":
        return "nix"
    else:
        return "unknown"


os_type = get_os()


def copy_notebook_to_folder(notebook_stem, origin_folder, destination_folder):
    origin_path = Path(origin_folder) / f"{notebook_stem}.ipynb"
    destination_folder = Path(destination_folder)
    destination_folder.mkdir(parents=True, exist_ok=True)
    destination_path = destination_folder / f"_{notebook_stem}.ipynb"
    if os_type == "nix":
        command = f"cp {origin_path} {destination_path}"
    else:
        command = f"copy  {origin_path} {destination_path}"
    return command


def task_load_raw():
    tasks = {
        'zero_coupon': {
            'script': 'load_zero_coupon',
            'target': 'fed_yield_curve.parquet'
        },
        'bbg': {
            'script': 'load_bbg_data',
            'target': ['bbg_data.parquet', 'bbg_future_data.parquet', 'bbg_maturity_data.parquet']
        }
    }

    for task_name, task_info in tasks.items():
        if isinstance(task_info['target'], list):
            targets = [DATA_DIR / "pulled" / task_name / target for target in task_info['target']]
        else:
            targets = [DATA_DIR / "pulled" / task_name / task_info['target']]

        yield {
            'name': task_name,
            'actions': [f'ipython ./src/{task_info["script"]}.py'],
            'targets': targets,
            'file_dep': [f'./src/{task_info["script"]}.py'],
            'clean': True,
        }


def task_clean_data():
    return {
        'actions': ['ipython ./src/clean_data.py'],
        'targets': [
            DATA_DIR / "pulled" / "clean_one_y_zc_paper.parquet",
            DATA_DIR / "pulled" / "clean_bbg_curr_data.parquet",
            DATA_DIR / "pulled" / "clean_bbg_paper_data.parquet",
            DATA_DIR / "pulled" / "clean_one_y_zc_curr.parquet",
            # Add more target files as needed
        ],
        'file_dep': [
            './src/clean_data.py',
            DATA_DIR / "pulled" / "fed_yield_curve.parquet",
            DATA_DIR / "pulled" / "bbg_data.parquet",
            DATA_DIR / "pulled" / "bbg_future_data.parquet",
            DATA_DIR / "pulled" / "bbg_maturity_data.parquet",
            # Add more file dependencies as needed
        ],
        'clean': True,
    }


def task_create_tables():
    return {
        'actions': [
            'ipython ./src/create_tables.py',
            'ipython ./src/create_tables_curr.py',
        ],
        'targets': [
            OUTPUT_DIR / "table_1.tex",
            OUTPUT_DIR / "table_2.tex",
            OUTPUT_DIR / "table_1_curr.tex",
            OUTPUT_DIR / "table_2_curr.tex",
            # Add more target files as needed
        ],
        'file_dep': [
            './src/create_tables.py',
            './src/create_tables_curr.py',
            DATA_DIR / "pulled" / "clean_one_y_zc_curr.parquet",
            DATA_DIR / "pulled" / "clean_bbg_paper_data.parquet",
            DATA_DIR / "pulled" / "clean_one_y_zc_paper.parquet",
            DATA_DIR / "pulled" / "clean_bbg_curr_data.parquet",
            # Add more file dependencies as needed
        ],
        'clean': True,
    }


def task_summary_stats():
    return {
        'actions': [
            'ipython ./src/create_summary_stats.py',
        ],
        'targets': [
            OUTPUT_DIR / "summary_stats.tex",
            # Add more target files as needed
        ],
        'file_dep': [
            './src/create_summary_stats.py',
            DATA_DIR / "pulled" / "clean_one_y_zc_curr.parquet",
            DATA_DIR / "pulled" / "clean_bbg_paper_data.parquet",
            DATA_DIR / "pulled" / "clean_one_y_zc_paper.parquet",
            DATA_DIR / "pulled" / "clean_bbg_curr_data.parquet",
            # Add more file dependencies as needed
        ],
        'clean': True,
    }

def task_compile_latex():
    """Compile LaTeX file into PDF."""
    return {
        'actions': ['pdflatex -output-directory=./reports ./reports/project_report.tex'],
        'file_dep': ['./output/table_1.tex', './output/table_2.tex', 
                     './output/table_1_curr.tex', './output/table_2_curr.tex', 
                     './output/summary_stats.tex'],
        'targets': ['./reports/project_report.pdf'],
        'clean': True,
    }


def task_clean_aux_files():
    """Clean auxiliary files generated by LaTeX."""
    aux_extensions = ['.aux', '.log', '.out', '.toc', '.lof', '.lot']
    aux_files = [f'./reports/project_report{ext}' for ext in aux_extensions]

    return {
        'actions': [(lambda file=file: os.remove(file)) for file in aux_files if os.path.exists(file)],
        'clean': True,
    }
    

# def task_convert_notebooks_to_scripts():
#     """Preps the notebooks for presentation format.
#     Execute notebooks with summary stats and plots and remove metadata.
#     """
#     build_dir = Path(OUTPUT_DIR)
#     build_dir.mkdir(parents=True, exist_ok=True)

#     notebooks = [
#         "01_example_notebook.ipynb",
#         "02_interactive_plot_example.ipynb",
#     ]
#     file_dep = [Path("./src") / file for file in notebooks]
#     stems = [notebook.split(".")[0] for notebook in notebooks]
#     targets = [build_dir / f"_{stem}.py" for stem in stems]

#     actions = [
#         # *[jupyter_execute_notebook(notebook) for notebook in notebooks_to_run],
#         # *[jupyter_to_html(notebook) for notebook in notebooks_to_run],
#         *[jupyter_clear_output(notebook) for notebook in stems],
#         *[jupyter_to_python(notebook, build_dir) for notebook in stems],
#     ]
#     return {
#         "actions": actions,
#         "targets": targets,
#         "task_dep": [],
#         "file_dep": file_dep,
#         "clean": True,
#     }


# def task_run_notebooks():
#     """Preps the notebooks for presentation format.
#     Execute notebooks with summary stats and plots and remove metadata.
#     """
#     notebooks = [
#         "01_example_notebook.ipynb",
#         "02_interactive_plot_example.ipynb",
#     ]
#     stems = [notebook.split(".")[0] for notebook in notebooks]

#     file_dep = [
#         # 'load_other_data.py',
#         *[Path(OUTPUT_DIR) / f"_{stem}.py" for stem in stems],
#     ]

#     targets = [
#         ## 01_example_notebook.ipynb output
#         OUTPUT_DIR / "sine_graph.png",
#         ## Notebooks converted to HTML
#         *[OUTPUT_DIR / f"{stem}.html" for stem in stems],
#     ]

#     actions = [
#         *[jupyter_execute_notebook(notebook) for notebook in stems],
#         *[jupyter_to_html(notebook) for notebook in stems],
#         *[copy_notebook_to_folder(notebook, Path("./src"), "./docs/_notebook_build/") for notebook in stems],
#         *[jupyter_clear_output(notebook) for notebook in stems],
#         # *[jupyter_to_python(notebook, build_dir) for notebook in notebooks_to_run],
#     ]
#     return {
#         "actions": actions,
#         "targets": targets,
#         "task_dep": [],
#         "file_dep": file_dep,
#         "clean": True,
#     }




# def task_compile_latex_docs():
#     """Compile the LaTeX documents to PDFs"""
#     file_dep = [
#         "./reports/report_example.tex",
#         "./reports/slides_example.tex",
#         "./src/example_plot.py",
#         "./src/example_table.py",
#     ]
#     file_output = [
#         "./reports/report_example.pdf",
#         "./reports/slides_example.pdf",
#     ]
#     targets = [file for file in file_output]

#     return {
#         "actions": [
#             "latexmk -xelatex -cd ./reports/report_example.tex",  # Compile
#             "latexmk -xelatex -c -cd ./reports/report_example.tex",  # Clean
#             "latexmk -xelatex -cd ./reports/slides_example.tex",  # Compile
#             "latexmk -xelatex -c -cd ./reports/slides_example.tex",  # Clean
#             # "latexmk -CA -cd ../reports/",
#         ],
#         "targets": targets,
#         "file_dep": file_dep,
#         "clean": True,
#     }


