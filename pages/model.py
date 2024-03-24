import streamlit as st
import pygltflib
import os
import tempfile

def modify_texture(glb_file_path, texture_file_path):
    # Load the GLB model
    gltf = pygltflib.GLTF2().load(glb_file_path)

    # Find the texture to replace
    texture_index = 0  # Assuming you want to replace the first texture
    texture = gltf.textures[texture_index]

    # Replace the texture with the new one
    texture.source = texture_file_path

    # Save the modified GLB model
    gltf.save(output_glb_file_path)

if __name__ == "__main__":
    st.title("Modify GLB Model Texture")

    glb_file = st.file_uploader("Upload GLB Model")
    texture_file = st.file_uploader("Upload Texture File")

    if glb_file and texture_file:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_glb_path = os.path.join(temp_dir, glb_file.name)
            temp_texture_path = os.path.join(temp_dir, texture_file.name)

            with open(temp_glb_path, "wb") as f:
                f.write(glb_file.read())
            with open(temp_texture_path, "wb") as f:
                f.write(texture_file.read())

            try:
                output_glb_file_path = "./data/modified_model.glb"
                modify_texture(temp_glb_path, temp_texture_path)
                st.success("Texture modified successfully! Output: modified_model.glb")
            except Exception as e:
                st.error(f"Error: {e}")
