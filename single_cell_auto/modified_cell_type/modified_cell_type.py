def modified_cell_type_run(obj):
    out = obj.out
    seurat = obj.modified_cell_type.input
    output = obj.modified_cell_type.output
    updata = obj.modified_cell_type.updata
    if updata:
        bl = 'T'
    else:
        bl = 'F'
    newcelltype_file = obj.modified_cell_type.newcelltype_file
    Modified_col = obj.modified_cell_type.Modified_col
    reduct = obj.modified_cell_type.reduct
    newcelltype_file_type = obj.modified_cell_type.newcelltype_file_type
    if newcelltype_file_type == 'tsv':
        fgf = 'F'
    elif newcelltype_file_type == 'csv':
        fgf = 'T'
    else:
        print('细胞文件名后缀只能是 tsv 或 csv，请检查 config 文件中 newcelltype_file_type 参数！')
        exit(1)
    with open(f'{out}/cmd_modified_cell_type.sh',"w") as f:
        f.write(f"""set -e
module purge && module load OESingleCell/3.0.d
Rscript /public/scRNA_works/pipeline/oesinglecell3/exec/sctool \\
-i {seurat} \\
-f h5seurat \\
-o {output} \\
-d h5seurat \\
--update {bl} \\
--assay RNA \\
--dataslot counts,data,scale.data  \\
changecelltype \\
-c {newcelltype_file} \\
-C {Modified_col} \\
--palette customecol2 \\
--reduct {reduct} \\
-b {fgf}
                """)
