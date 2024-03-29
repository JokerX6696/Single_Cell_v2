def cellchat_run(obj):
    rds = obj.cellchat.rds
    species=obj.cellchat.species
    col = obj.cellchat.col  # 用来进行通讯分析的metadata列名
    group_need = obj.cellchat.group_need
    group_type = obj.cellchat.group_type
    group_list = obj.cellchat.group_list
    out = obj.cellchat.out
    part = obj.cellchat.part
    part_name = obj.cellchat.part_name
    part_list = obj.cellchat.part_list
    out_sc = obj.out
    
    if part:
        for p in part_list:
            script_out = "cmd_cellchat_" + part_name + "_" + str(p) + ".sh"
            with open(f"{out_sc}/{script_out}","w") as f:
                f.write(f"""set -e
module load OESingleCell/3.0.d
Rscript /public/scRNA_works/pipeline/scRNA-seq_further_analysis/CellChat_v1.6.1.R \\
-i {rds} \\
-f rds \\
-s {species}  \\
-c {col} \\
""")
                if group_need:
                    group_vs = "+".join(group_list)
                    f.write(f"-g {group_type}  \\\n-d {group_vs} \\\n")
                f.write(f"-q {part_name} \\\n-u {p} \\\n")
                f.write(f"-o {out}\n")
    else:
        script_out = "cmd_cellchat.sh"
        with open(f"{out_sc}/{script_out}","w") as f:
            f.write(f"""set -e
module load OESingleCell/3.0.d
Rscript /public/scRNA_works/pipeline/scRNA-seq_further_analysis/CellChat_v1.6.1.R \\
-i {rds} \\
-f rds \\
-s {species}  \\
-c {col} \\
""")
            if group_need:
                group_vs = "+".join(group_list)
                f.write(f"-g {group_type}  \\\n-d {group_vs} \\\n")
            f.write(f"-o {out}\n")