import importlib
import pathlib

# Descobre dinamicamente todos os arquivos .py dentro da pasta models
models_path = pathlib.Path(__file__).parent

for model_file in models_path.glob("*.py"):
    if model_file.name.startswith("_") or model_file.name == "__init__.py":
        continue
    module_name = f"models.{model_file.stem}"
    importlib.import_module(module_name)
