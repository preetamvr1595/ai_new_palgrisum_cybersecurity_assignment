import os

root_dir = "f:/new_palgrisum_ai"

# Directory definitions
directories = [
    # Frontend
    "frontend/src/app",
    "frontend/src/components/ui",
    "frontend/src/components/forms",
    "frontend/src/components/dashboard",
    "frontend/src/components/navbar",
    "frontend/src/components/footer",
    "frontend/src/components/charts",
    "frontend/src/components/modals",
    "frontend/src/components/tables",
    "frontend/src/components/file_upload",
    "frontend/src/features/auth",
    "frontend/src/features/ai_detector",
    "frontend/src/features/humanizer",
    "frontend/src/features/paraphraser",
    "frontend/src/features/grammar",
    "frontend/src/features/plagiarism",
    "frontend/src/features/citations",
    "frontend/src/features/research",
    "frontend/src/features/billing",
    "frontend/src/hooks",
    "frontend/src/services",
    "frontend/src/lib",
    "frontend/src/layouts",
    "frontend/src/pages",
    "frontend/src/styles",
    "frontend/src/constants",
    "frontend/src/types",
    "frontend/src/utils",
    
    # Backend
    "backend/app/api/v1/auth",
    "backend/app/api/v1/users",
    "backend/app/api/v1/documents",
    "backend/app/api/v1/ai_detector",
    "backend/app/api/v1/humanizer",
    "backend/app/api/v1/paraphraser",
    "backend/app/api/v1/grammar",
    "backend/app/api/v1/plagiarism",
    "backend/app/api/v1/citations",
    "backend/app/api/v1/research",
    "backend/app/api/v1/billing",
    "backend/app/core",
    "backend/app/models",
    "backend/app/schemas",
    "backend/app/services",
    "backend/app/repositories",
    "backend/app/middleware",
    "backend/app/utils",
    "backend/app/workers",
    "backend/app/tasks",
    "backend/app/tests",
    
    # AI Models
    "ai_models/detector",
    "ai_models/humanizer",
    "ai_models/paraphraser",
    "ai_models/grammar",
    "ai_models/plagiarism",
    "ai_models/embeddings",
    "ai_models/evaluation",
    
    # Datasets
    "datasets/raw",
    "datasets/processed",
    "datasets/training",
    "datasets/validation",
    "datasets/testing",
    "datasets/benchmark",
    
    # Infrastructure
    "infrastructure/docker",
    "infrastructure/monitoring",
    "infrastructure/nginx",
    "infrastructure/ssl",
    "infrastructure/backups",
    
    # Root level
    "docs",
    "scripts",
    "tests",
    "docker",
    ".github/workflows"
]

# Create directories and .gitkeep files
for d in directories:
    dir_path = os.path.join(root_dir, d)
    os.makedirs(dir_path, exist_ok=True)
    with open(os.path.join(dir_path, ".gitkeep"), "w") as f:
        pass

# Create specific Python files for backend/core
backend_core_files = [
    "config.py",
    "database.py",
    "security.py",
    "logging.py",
    "cache.py",
    "constants.py"
]

for f_name in backend_core_files:
    file_path = os.path.join(root_dir, "backend/app/core", f_name)
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            f.write("# Placeholder for " + f_name + "\n")

print("Scaffolding complete.")
