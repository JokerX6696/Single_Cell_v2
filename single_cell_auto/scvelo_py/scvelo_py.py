def scvelo_py_run(obj):
    import os
    out = obj.out
    seurat = obj.scvelo_py.input_seurat
    assay = obj.scvelo_py.assay
    core = obj.scvelo_py.core
    loom_dir = obj.scvelo_py.loom_dir
    groupby = obj.scvelo_py.groupby
    reduction = obj.scvelo_py.reduction
    output = obj.scvelo_py.output
    step1 = obj.scvelo_py.step1
    step2 = obj.scvelo_py.step2




    if step2:
        if not os.path.exists(f"{out}/dev_fangying"):
            cmd1=f"cp /public/dev_scRNA/yfang/dev_fangying {out}"
            os.system(cmd1)
        with open(f'{out}/cmd_velo.sh',"w") as f:
            f.write(f"""set -e
module load git 
module load ./dev_fangying 
sctool -i {seurat} -f h5seurat --assay {assay} -j {core} -o {output}  pyscvelo --loom_dir {loom_dir} --groupby {groupby} --reduction {reduction}

""")