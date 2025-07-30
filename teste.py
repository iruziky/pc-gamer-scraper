import sys
import rnet  # Tente importar aqui também

print("--- Diagnóstico de Ambiente do VS Code ---")
print(f"Versão do Python: {sys.version}")
print(f"Caminho do Executável: {sys.executable}")
print("\n--- Caminhos de Busca (sys.path) ---")
for path in sys.path:
    print(path)

print(f"\n--- Localização da lib rnet ---")
print(f"rnet encontrada em: {rnet.__file__}")