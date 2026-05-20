import os

workspace_dir = r"d:\deadshot file\computer_thesisZone_\finland 1"

def replace_in_file(filepath, replacements):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    modified = content
    for target, replacement in replacements.items():
        modified = modified.replace(target, replacement)
        
    if modified != content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(modified)
        print(f"Updated {os.path.basename(filepath)}")
    else:
        print(f"No changes needed for {os.path.basename(filepath)}")

replacements = {
    "thesis_figures": "pipeline_figures",
    "thesis_tables": "pipeline_tables",
    "thesis_results_chapter.txt": "results_chapter.txt",
    "thesis_discussion_chapter.txt": "discussion_chapter.txt"
}

replace_in_file(os.path.join(workspace_dir, "pipeline_analysis.py"), replacements)
replace_in_file(os.path.join(workspace_dir, "generate_report_doc.py"), replacements)
print("Finished updates.")
