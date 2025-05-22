import os
import subprocess
import multiprocessing
from pathlib import Path

def run_command(cmd):
    """增强版命令执行"""
    print(f"\n[EXEC] {cmd}")
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True,
        check=False
    )
    
    if result.returncode != 0:
        print(f"[ERROR] Return code: {result.returncode}")
        print(f"[STDERR] {result.stderr.strip()}")
        return False
    
    print(f"[SUCCESS] {cmd.split()[0]}")
    return True

def run_openmvg_pipeline(image_dir, session_id):
    """优化后的3D重建流程"""
    base = Path(f"app/static/{session_id}")
    matches_dir = base / "matches"
    recon_dir = base / "reconstruction_sequential"
    mvs_dir = base / "openMVS"

    print("new create:"+ session_id)
    # 创建目录结构
    for d in [matches_dir, recon_dir, mvs_dir]:
        d.mkdir(parents=True, exist_ok=True)

    threads = max(1, multiprocessing.cpu_count() - 1)
    sensor_db = "/opt/openMVG/src/openMVG/exif/sensor_width_database/sensor_width_camera_database.txt"

    cmds = [
        # 1. OpenMVG SfM
        f"openMVG_main_SfMInit_ImageListing -i {image_dir} -o {matches_dir} -d {sensor_db} -f 4000",
        f"openMVG_main_ComputeFeatures -i {matches_dir}/sfm_data.json -o {matches_dir}/ --describerMethod SIFT --describerPreset HIGH",
        f"openMVG_main_PairGenerator -i {matches_dir}/sfm_data.json -o {matches_dir}/pairs.bin",
        f"openMVG_main_ComputeMatches -i {matches_dir}/sfm_data.json -p {matches_dir}/pairs.bin -o {matches_dir}/matches.putative.bin",
        f"openMVG_main_GeometricFilter -i {matches_dir}/sfm_data.json -m {matches_dir}/matches.putative.bin -g f -o {matches_dir}/matches.f.bin",
        f"openMVG_main_SfM -s INCREMENTAL -i {matches_dir}/sfm_data.json -m {matches_dir} -o {recon_dir}",

        # 2. Convert to OpenMVS
        f"openMVG_main_openMVG2openMVS -i {recon_dir}/sfm_data.bin -d {recon_dir}/undistorted_images -o {mvs_dir}/scene.mvs",
        
        f"rm -rf /reconstruction_sequential",
        f"mkdir /reconstruction_sequential && cp -rf {recon_dir}/undistorted_images /reconstruction_sequential",

        # 3. OpenMVS Pipeline
        f"DensifyPointCloud {mvs_dir}/scene.mvs -o {mvs_dir}/scene_dense.mvs --resolution-level 1 --max-threads {threads}",
        
        f"rm -rf /app/app/static/reconstruction_sequential",
        f"mkdir /app/app/static/reconstruction_sequential && cp -rf {recon_dir}/undistorted_images /app/app/static/reconstruction_sequential",

        f"ReconstructMesh {mvs_dir}/scene_dense.mvs -p {mvs_dir}/scene_dense.ply -o {mvs_dir}/scene_mesh.mvs",
        #f"RefineMesh {mvs_dir}/scene_dense.mvs -m {mvs_dir}/scene_dense.ply -o {mvs_dir}/scene_dense_mesh_refine.mvs --scales 1 --max-face-area 16",
        #f"TextureMesh {mvs_dir}/scene_dense.mvs -m {mvs_dir}scene_dense_mesh_refine.ply -o {mvs_dir}/scene_dense_mesh_refine_texture.mvs",
        
        # 4. Export
        #f"InterfaceOBJ {mvs_dir}/scene_texture.mvs --output-file {mvs_dir}/scene_texture.obj"
        #f"InterfaceOBJ {mvs_dir}/scene_texture.mvs --output-file {mvs_dir}/scene_texture.obj"
    ]

    # 分步执行
    for idx, cmd in enumerate(cmds, 1):
        print(f"\n=== Step {idx}/{len(cmds)} ===")
        if not run_command(cmd):
            return None

    # 返回标准化路径
    obj_path = mvs_dir / "scene_mesh.ply"
    return str(obj_path) if obj_path.exists() else None
